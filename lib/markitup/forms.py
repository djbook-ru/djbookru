class MarkdownEditorMixin(object):

    class Media:
        css = {
            'all': (
                'markitup/skins/simple/style.css',
                'markitup/sets/markdown_without_priview/style.css'
            )
        }
        js = [
            'markitup/django_jquery.js',
            'markitup/sets/markdown_without_priview/set.js',
            'markitup/jquery.markitup.js',
            'markitup/markitup_init.js'
        ]
