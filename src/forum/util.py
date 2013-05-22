from HTMLParser import HTMLParser
from django.template.defaultfilters import urlize as django_urlize


class ExcludeTagsHTMLParser(HTMLParser):
        """
        Class for html parsing with excluding specified tags.
        """

        def __init__(self, func, tags=('a', 'code')):
            HTMLParser.__init__(self)
            self.func = func
            self.is_ignored = False
            self.tags = tags
            self.html = []

        def handle_starttag(self, tag, attrs):
            self.html.append('<%s%s>' % (tag, self.__html_attrs(attrs)))
            if tag in self.tags:
                self.is_ignored = True

        def handle_data(self, data):
            if not self.is_ignored:
                data = self.func(data)
            self.html.append(data)

        def handle_startendtag(self, tag, attrs):
            self.html.append('<%s%s/>' % (tag, self.__html_attrs(attrs)))

        def handle_endtag(self, tag):
            self.is_ignored = False
            self.html.append('</%s>' % (tag))

        def handle_entityref(self, name):
            self.html.append('&%s;' % name)

        def handle_charref(self, name):
            self.html.append('&#%s;' % name)

        def unescape(self, s):
            #we don't need unescape data (without this possible XSS-attack)
            return s

        def __html_attrs(self, attrs):
            _attrs = ''
            if attrs:
                _attrs = ' %s' % (' '.join([('%s="%s"' % (k, v)) for k, v in attrs]))
            return _attrs

        def feed(self, data):
            HTMLParser.feed(self, data)
            self.html = ''.join(self.html)


def urlize(data):
    """
    Urlize plain text links in the HTML contents.

    Do not urlize content of A and CODE tags.
    """

    parser = ExcludeTagsHTMLParser(django_urlize)
    parser.feed(data)
    urlized_html = parser.html
    parser.close()
    return urlized_html
