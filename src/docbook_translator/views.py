from django.views.generic.simple import direct_to_template
from lxml import etree
from docbook_translator.parser import get_test_list_from_chapter

def parser(request):
    f = request.FILES.get(u'f')
    if f:
        tree = etree.parse(f)
        root = tree.getroot()
        texts = get_test_list_from_chapter(root) 
    else:
        texts = [] 
    context = {
        'texts': texts
    }
    return direct_to_template(request, 'docbook_translator/parser.html', context)