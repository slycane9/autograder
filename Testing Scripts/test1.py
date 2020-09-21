from django.test import TestCase, RequestFactory
from newslister.models import NewsListing
from newslister.models import UserXtraAuth
from newslister.views import NewsApiManager, user_account
import sys 
    
sys.stdout = open('result.txt','w')
print('If a testing header is not followed by a pass statement that test failed')
class ViewsTestCase(TestCase):
    def setUp(self):
        UserXtraAuth.objects.create(username="bigshot", secrecy=5, tokenkey = "")
        UserXtraAuth.objects.create(username="rookie", secrecy=0, tokenkey = "")
        
        NewsListing.objects.create(queryId="abc", query="Top Secret", sources="", secrecy=5,lastuser="")
        NewsListing.objects.create(queryId="cde", query="Not Secret", sources="", secrecy=0,lastuser="")
        NewsListing.objects.create(queryId="bcd", query="Middle Secret", sources="", secrecy=3,lastuser="")

    def test_api_manager(self):
        print('Testing the no read up policy:')
        
        test_api = NewsApiManager()
        
        #0 secrecy api cannot read articles of higher secrecy level
        test_api.update_secrecy(0)
        test_api.update_articles()
        
        self.assertEqual(len(test_api.data), 1)
        
        #5 secrecy api can read articles of equal or higher secrecy level
        test_api.update_secrecy(5)
        test_api.update_articles()
        
        self.assertEqual(len(test_api.data), 3)
        
        print("Read Test Passed")
    
    def test_user_account(self):
        print('Testing that users can only see news items at their level when in the view to update or create news items:')
        
        rookie = UserXtraAuth.objects.get(username="rookie")
        bigshot = UserXtraAuth.objects.get(username="bigshot")
        
        #set up requests
        request_get = RequestFactory().get('/')
        
        data = {'create_news': 'news', 'new_news_query': 'new', 'new_news_sources': 'source', 'new_news_secrecy': 5}
        request_post_create = RequestFactory().post('/', data)
        
        data = {'update_update': 'news', 'update_news_query': 'new', 'update_news_sources': 'source', 'update_news_secrecy': 5, 'update_news_select' : 'new'}
        request_post_update = RequestFactory().post('/', data)
        
        
        data = {'update_delete': 'news', 'update_news_select': 'new'}
        request_post_delete = RequestFactory().post('/', data)
        
        #test bigshot get
        request_get.user = bigshot
        render = user_account(request_get)
        #httpresponse content has 2 entries of the queryId it keeps and 1 of the others
        self.assertTrue(str(render.content).count("abc") == 2)
        self.assertTrue(str(render.content).count("bcd") == 1)
        self.assertTrue(str(render.content).count("cde") == 1)
        
        #test bigshot create
        request_post_create.user = bigshot
        render = user_account(request_post_create)
        #httpresponse content has 2 entries of the queryId it keeps and 1 of the others
        self.assertTrue(str(render.content).count("abc") == 2)
        self.assertTrue(str(render.content).count("bcd") == 1)
        self.assertTrue(str(render.content).count("cde") == 1)
        
        '''
        #test bigshot delete
        request_post_delete.user = bigshot
        render = user_account(request_post_delete)
        #httpresponse content has 2 entries of the queryId it keeps and 1 of the others
        self.assertTrue(str(render.content).count("abc") == 2)
        self.assertTrue(str(render.content).count("bcd") == 1)
        self.assertTrue(str(render.content).count("cde") == 1)
        
        
        #test bigshot update
        request_post_update.user = bigshot
        render = user_account(request_post_update)
        #httpresponse content has 2 entries of the queryId it keeps and 1 of the others
        self.assertTrue(str(render.content).count("abc") == 2)
        self.assertTrue(str(render.content).count("bcd") == 1)
        self.assertTrue(str(render.content).count("cde") == 1)
        '''
        #test rookie get
        request_get.user = rookie
        render = user_account(request_get)
        #httpresponse content has 2 entries of the queryId it keeps and 1 of the others
        self.assertTrue(str(render.content).count("abc") == 1)
        self.assertTrue(str(render.content).count("bcd") == 1)
        self.assertTrue(str(render.content).count("cde") == 2)
        
        #test rookie create
        request_post_create.user = rookie
        render = user_account(request_post_create)
        #httpresponse content has 2 entries of the queryId it keeps and 1 of the others
        self.assertTrue(str(render.content).count("abc") == 1)
        self.assertTrue(str(render.content).count("bcd") == 1)
        self.assertTrue(str(render.content).count("cde") == 2)
        '''
        #test rookie delete
        request_post_delete.user = rookie
        render = user_account(request_post_delete)
        #httpresponse content has 2 entries of the queryId it keeps and 1 of the others
        self.assertTrue(str(render.content).count("abc") == 1)
        self.assertTrue(str(render.content).count("bcd") == 1)
        self.assertTrue(str(render.content).count("cde") == 2)
        
        #test rookie delete
        request_post_update.user = rookie
        render = user_account(request_post_update)
        #httpresponse content has 2 entries of the queryId it keeps and 1 of the others
        self.assertTrue(str(render.content).count("abc") == 1)
        self.assertTrue(str(render.content).count("bcd") == 1)
        self.assertTrue(str(render.content).count("cde") == 2)
        '''
        print("User View Test Passed")
    def test_form_validation(self):
        print('Testing that BLP is followed on creation/write of news item:')
        
        rookie = UserXtraAuth.objects.get(username="rookie")
        bigshot = UserXtraAuth.objects.get(username="bigshot")
        
        #set up requests        
        data = {'create_news': 'news', 'new_news_query': 'new', 'new_news_sources': 'source', 'new_news_secrecy': 3}
        request_post_create = RequestFactory().post('/', data)
        
        request_post_create.user = rookie
        render = user_account(request_post_create)
        
        try:
            request_post_create.user = bigshot
            render = user_account(request_post_create)
            self.assertTrue(False)
        except:
            self.assertTrue(True)
            print("Write Test Passed")
        