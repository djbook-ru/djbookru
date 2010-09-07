from django.test import TestCase
from django.core.urlresolvers import reverse

class TestClass(TestCase):
    
    def test_views(self):
        response = self.client.get(reverse("main:index"))
        self.failUnlessEqual(response.status_code, 200)
        
        response = self.client.get("/about/")
        self.failUnlessEqual(response.status_code, 200)
        
        response = self.client.get("/hosting/")
        self.failUnlessEqual(response.status_code, 200)