"""
Admin ui common utilities.
"""

import types
from fnmatch import fnmatch

from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.importlib import import_module


def get_admin_site(context=None, request=None):
    dashboard_cls = getattr(
        settings,
        'ADMIN_TOOLS_INDEX_DASHBOARD',
        'admin_tools.dashboard.DefaultIndexDashboard'
    )
    
    if type(dashboard_cls) is types.DictType:
        if context:
            curr_url = context.get('request').META['PATH_INFO']
        else:
            curr_url = request.META['PATH_INFO']
        
        for key in dashboard_cls:
            mod, inst = key.rsplit('.', 1)
            admin_url = reverse('%s:index' % inst)
            if curr_url.startswith(admin_url):
                mod = import_module(mod)
                return getattr(mod, inst)
    else:
        return admin.site


def get_admin_site_name(context):
    return get_admin_site(context).name


def get_avail_models(request):
    """ Returns (model, perm,) for all models user can possibly see """
    items = []
    
    admin_site = get_admin_site(request=request)
    
    for model, model_admin in admin_site._registry.items():
        perms = model_admin.get_model_perms(request)
        if True not in perms.values():
            continue
        items.append((model, perms,))
    return items


def filter_models(request, models, exclude):
    """ Returns (model, perm,) for all models that match
        models/exclude patterns and are visible by current user.
    """
    items = get_avail_models(request)
    included = []
    full_name = lambda model: '%s.%s' % (model.__module__, model.__name__)

    # I beleive that that implemented
    # O(len(patterns)*len(matched_patterns)*len(all_models))
    # algorythm is fine for model lists because they are small and admin
    # performance is not a bottleneck. If it is not the case then the code
    # should be optimized.

    if len(models) == 0:
        included = items
    else:
        for pattern in models:
            for item in items:
                model, perms = item
                if fnmatch(full_name(model), pattern) and item not in included:
                    included.append(item)

    result = included[:]
    for pattern in exclude:
        for item in included:
            model, perms = item
            if fnmatch(full_name(model), pattern):
                result.remove(item)
    return result


class AppListElementMixin(object):
    """
    Mixin class used by both the AppListDashboardModule and the
    AppListMenuItem (to honor the DRY concept).
    """
    def _check_perms(self, request, model, model_admin):
        mod = '%s.%s' % (model.__module__, model.__name__)
        
        if type(self).__name__ == 'ModelListDashboardModule':
            if len(self.models):
                found = False
                for pattern in self.models:
                    if mod.startswith(pattern):
                        found = True
                if not found:
                    return False
        
        elif type(self).__name__ == 'AppListDashboardModule':
            if len(self.apps):
                found = False
                for pattern in self.apps:
                    if mod.startswith(pattern):
                        found = True
                if not found:
                    return False
        
        # check that the user has module perms
        if not request.user.has_module_perms(model._meta.app_label):
            return False

        # check whether user has any perm for this module
        perms = model_admin.get_model_perms(request)
        if True not in perms.values():
            return False
        return perms
    
    def _visible_models(self, request):
        # compatibility layer: generate models/exclude patterns
        # from include_list/exclude_list args
        included = self.models[:]
        included.extend([elem+"*" for elem in self.include_list])

        excluded = self.exclude[:]
        excluded.extend([elem+"*" for elem in self.exclude_list])
        if self.exclude_list and not included:
            included = ["*"]
        return filter_models(request, included, excluded)


    def _get_admin_change_url(self, model, context):
        """
        Returns the admin change url.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_changelist' % (get_admin_site_name(context),
                                                app_label,
                                                model.__name__.lower()))


    def _get_admin_add_url(self, model, context):
        """
        Returns the admin add url.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_add' % (get_admin_site_name(context),
                                            app_label,
                                            model.__name__.lower()))


def get_media_url():
    """
    Returns the django admin tools media URL.
    """
    return getattr(
        settings,
        'ADMIN_TOOLS_MEDIA_URL',
        getattr(settings, 'STATIC_URL', settings.MEDIA_URL)
    ).rstrip('/')
