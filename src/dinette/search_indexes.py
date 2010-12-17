from haystack import indexes
from haystack import site

from dinette.models import Ftopics, Reply

class TopicIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    subject = indexes.CharField(model_attr="subject")
    message = indexes.CharField(model_attr="message")
    
class ReplyIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    message = indexes.CharField(model_attr="message")
    
site.register(Ftopics, TopicIndex)
site.register(Reply, ReplyIndex)
