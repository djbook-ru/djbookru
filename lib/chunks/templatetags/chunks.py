from django import template
from django.db import models
from django.core.cache import cache
from django.conf import settings

register = template.Library()

Chunk = models.get_model('chunks', 'chunk')
CACHE_PREFIX = "chunk_"
CHANKS_LIST_NAME = getattr(settings, "CHANKS_LIST_NAME", "chunks_list")

def do_get_chunk(parser, token):
    # split_contents() knows not to split quoted strings.
    tokens = token.split_contents()
    if len(tokens) < 2 or len(tokens) > 5:
        raise template.TemplateSyntaxError, "%r tag should have either 2 or 3 or 5 arguments" % (tokens[0],)
    if len(tokens) == 2:
        tag_name, key = tokens
        cache_time = 0
        variable = None
    if len(tokens) == 3:
        tag_name, key, cache_time = tokens
        variable = None
    if len(tokens) == 5:
        tag_name, key, cache_time, not_used, variable = tokens
    # Check to see if the key is properly double/single quoted
    if not (key[0] == key[-1] and key[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    # Send key without quotes and caching time
    return ChunkNode(key[1:-1], cache_time, variable)
    
class ChunkNode(template.Node):
    def __init__(self, key, cache_time=0, variable_name=None):
        self.key = key
        self.cache_time = cache_time
        self.variable_name = variable_name
    
    def render(self, context):
        try:
            cache_key = CACHE_PREFIX + self.key
            c = cache.get(cache_key)
            if c is None:
                c = Chunk.objects.get(key=self.key)
                cache.set(cache_key, c, int(self.cache_time))
            content = c.content
        except Chunk.DoesNotExist:
            c = Chunk(key=self.key, content=self.key)
            c.save()
            content = ''
         
        context.dicts[0][CHANKS_LIST_NAME] = context.get(CHANKS_LIST_NAME, {})
        context.dicts[0][CHANKS_LIST_NAME][c.pk] = c.key
        
        if self.variable_name:
            context[self.variable_name] = content
            return ''
        return content
        
register.tag('chunk', do_get_chunk)
