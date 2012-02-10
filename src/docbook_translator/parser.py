# -*- coding: utf-8 -*-
from lxml import etree

class TextElement(object):
    
    def __init__(self, el, el_type=None, path=[]):
        
        self.path = '/'.join(path)
        
        if isinstance(el, (unicode, str)):
            self.text = el
            self.type = el_type
        else:
            self.type = el.tag
            self.path = '/'.join(get_path(el))
            
            if el.tag == 'title':
                self.text = el.text
            else:
                tag_len = len(el.tag)+2
                self.text = etree.tounicode(el, with_tail=False)[tag_len:-(tag_len+1)]
            
        self.text = self.text.strip()
        
    def __unicode__(self):
        return self.text
    
    def __nonzero__(self):
        return bool(self.text)
    
def has_el(iterator):
    '''
    Проверяет содержит ли итератор элемент
    '''
    try:
        iterator.next()
        return True
    except StopIteration:
        return False

def get_path(el):
    path = [item.tag for item in el.iterancestors()]
    path.reverse()
    return path

def get_first_lvl_paragrafs(el):
    '''
    Возвращает список параграфов, который являються параграфами-потомками первого уровня для элемента
    Тоесть для: <para id=1><para id=2><para id=3></para></para></para>, если передать
    <para id=1>, вернет <para id=2>, но не <para id=3>.
    '''
    el_path_len = len(get_path(el))+1
    para_list = []
    for item in el.iter('para'):
        if not 'para' in get_path(item)[el_path_len:]:
            para_list.append(item)
    if el.tag == 'para':
        para_list = para_list[1:]
    return para_list

def get_containing_el(el, para):
    containing_el = para
    
    for item in para.iterancestors():
        if item == el:
            break
        else:
            containing_el = item
    return containing_el

def get_text_berween_tags(parent, first_el, second_el):
    output = []
    
    if first_el == second_el:
        return ''
    
    for item in second_el.itersiblings(preceding=True):
        if item == second_el:
            continue
        if item == first_el:
            break
        output.append(etree.tounicode(item))
        
    if first_el is None: 
        output.append(parent.text)
    else:
        output.append(first_el.tail)
    output.reverse()

    return ''.join(output)

def get_tail_with_nodes(el):
    output = [el.tail]
    for item in el.itersiblings():
        if item == el:
            continue        
        output.append(etree.tounicode(item))
    return ''.join(output)

def get_previous_title(el):
    prev_el = el.getprevious()
    if prev_el is not None and prev_el.tag == 'title':
        return prev_el

def get_text_list(el):
    text_list = []
    para_list = get_first_lvl_paragrafs(el)
    
    last_cheked_containing_el = None

    for para in para_list:
        containing_el = get_containing_el(el, para)
        t = get_text_berween_tags(el, last_cheked_containing_el, containing_el)
        text_list.append(TextElement(t, last_cheked_containing_el is None and 'start_para' or 'text', get_path(el)))
        last_cheked_containing_el = containing_el
        if not has_el(para.iterdescendants('para')):
            #параграф не содержит другие параграфы, тоесть его содержимое можно 
            #включать в списко текстовых елементов
            title = get_previous_title(para)
            if title is not None:
                text_list.append(TextElement(title))   
            text_list.append(TextElement(para))
        else:
            text_list.extend(get_text_list(para))

    text_list.append(TextElement(get_tail_with_nodes(last_cheked_containing_el), 'end_para', get_path(el)))
    
    return text_list

def get_text_list_from_chapter(chapter):
    text_list = []
    para_list = get_first_lvl_paragrafs(chapter)    
    
    for para in para_list:
        if not has_el(para.iterdescendants('para')):
            title = get_previous_title(para)
            if title is not None:
                text_list.append(TextElement(title))            
            text_list.append(TextElement(para))
        else:      
            text_list.extend(get_text_list(para))
    
    output = []
    for item in text_list:
        item and output.append(item)
            
    return output



