from django.test import TestCase, RequestFactory
from newslister.models import NewsListing
from newslister.models import UserXtraAuth
from newslister.views import NewsApiManager, user_account
from django.core.exceptions import ValidationError
import sys 
    
#sys.stdout = open('result.txt','w')
#print('If a testing header is not followed by a pass statement that test failed')



class ViewsTestCase(TestCase):
    def setUp(self):
        UserXtraAuth.objects.create(username="bigshot", secrecy=5, tokenkey = "")
        UserXtraAuth.objects.create(username="rookie", secrecy=0, tokenkey = "")
        
        NewsListing.objects.create(queryId="abc", query="Top Secret", sources="", secrecy=5,lastuser="")
        NewsListing.objects.create(queryId="cde", query="Not Secret", sources="", secrecy=0,lastuser="")
        NewsListing.objects.create(queryId="bcd", query="Middle Secret", sources="", secrecy=3,lastuser="")
        
        self.all_passed = True

    def test_api_manager(self):
        print("Testing the no read up policy:")
        
        try:
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
            
        except AssertionError:
            print("Read Test Failed")
            self.all_passed = False
    
    def test_user_account(self):
        print("Testing that users can only see news items at their level when in the view to update or create news items:")
        
        rookie = UserXtraAuth.objects.get(username="rookie")
        bigshot = UserXtraAuth.objects.get(username="bigshot")
        
        #set up requests
        request_get = RequestFactory().get('/')
        
        data = {'create_news': 'news', 'new_news_query': 'new', 'new_news_sources': 'source', 'new_news_secrecy': 5}
        request_post_create = RequestFactory().post('/', data)
        
        data = {'update_update': 'news', 'update_news_query': 'new', 'update_news_sources': 'source', 'update_news_secrecy': 5, 'update_news_select' : NewsListing.objects.get(queryId="abc").id}
        request_post_update = RequestFactory().post('/', data)
        
        
        data = {'update_delete': 'news', 'update_news_select': NewsListing.objects.get(queryId="abc").id}
        request_post_delete = RequestFactory().post('/', data)
        
        try:
            #test bigshot get
            request_get.user = bigshot
            render = user_account(request_get)
            
            self.assertTrue(str(render.content).count("abc") == 1)
            self.assertTrue(str(render.content).count("bcd") == 0)
            self.assertTrue(str(render.content).count("cde") == 0)
            
            #test bigshot create
            request_post_create.user = bigshot
            render = user_account(request_post_create)
            
            self.assertTrue(str(render.content).count("abc") == 1)
            self.assertTrue(str(render.content).count("bcd") == 0)
            self.assertTrue(str(render.content).count("cde") == 0)
            
            
            #test bigshot delete
            request_post_delete.user = bigshot
            render = user_account(request_post_delete)
            
            self.assertTrue(str(render.content).count("abc") == 1)
            self.assertTrue(str(render.content).count("bcd") == 0)
            self.assertTrue(str(render.content).count("cde") == 0)
            
            
            #test bigshot update
            request_post_update.user = bigshot
            render = user_account(request_post_update)
            
            self.assertTrue(str(render.content).count("abc") == 1)
            self.assertTrue(str(render.content).count("bcd") == 0)
            self.assertTrue(str(render.content).count("cde") == 0)
            
            #test rookie get
            request_get.user = rookie
            render = user_account(request_get)
            
            self.assertTrue(str(render.content).count("abc") == 0)
            self.assertTrue(str(render.content).count("bcd") == 0)
            self.assertTrue(str(render.content).count("cde") == 1)
            
            #test rookie create
            request_post_create.user = rookie
            render = user_account(request_post_create)
            
            self.assertTrue(str(render.content).count("abc") == 0)
            self.assertTrue(str(render.content).count("bcd") == 0)
            self.assertTrue(str(render.content).count("cde") == 1)
            
            #test rookie delete
            request_post_delete.user = rookie
            render = user_account(request_post_delete)
            
            self.assertTrue(str(render.content).count("abc") == 0)
            self.assertTrue(str(render.content).count("bcd") == 0)
            self.assertTrue(str(render.content).count("cde") == 1)
            
            #test rookie update
            request_post_update.user = rookie
            render = user_account(request_post_update)
            
            self.assertTrue(str(render.content).count("abc") == 0)
            self.assertTrue(str(render.content).count("bcd") == 0)
            self.assertTrue(str(render.content).count("cde") == 1)
            
            print("User View Test Passed")
        except AssertionError:
            print("User View Test Failed")
            self.all_passed = False
        
    def test_form_validation(self):
        print("Testing that BLP is followed on creation/update/delete of news item:")
        
        rookie = UserXtraAuth.objects.get(username="rookie")
        bigshot = UserXtraAuth.objects.get(username="bigshot")
        
        #set up requests        
        data = {'create_news': 'news', 'new_news_query': 'new', 'new_news_sources': 'source', 'new_news_secrecy': 3}
        request_post_create = RequestFactory().post('/', data)
        
        data = {'update_update': 'news', 'update_news_query': 'new', 'update_news_sources': 'source', 'update_news_secrecy': 3, 'update_news_select' : NewsListing.objects.get(queryId="bcd").id}
        request_post_update = RequestFactory().post('/', data)
        
        data = {'update_update': 'news', 'update_news_query': 'new', 'update_news_sources': 'source', 'update_news_secrecy': 1, 'update_news_select' : NewsListing.objects.get(queryId="abc").id}
        request_post_update2 = RequestFactory().post('/', data)
        
        
        data = {'update_delete': 'news', 'update_news_select': NewsListing.objects.get(queryId="bcd").id}
        request_post_delete = RequestFactory().post('/', data)
        
        # attempt to write down  (5->3) and fail
        try:
            request_post_create.user = bigshot
            render = user_account(request_post_create)
            self.all_passed = False
            print("Write Test Failed")
        except Exception as e:
            print(e)
            print("Write Test Passed")
            
        # attempt to update at an item at a different security level (5->3)
        try:
            request_post_update.user = bigshot
            render = user_account(request_post_update)
            self.all_passed = False
            print("Update Test Failed")
        except Exception as e:
            print(e)
            print("Update Test Passed")
            
        # attempt to update the security level of an item to be lower (5->1)
        try:
            request_post_update2.user = bigshot
            render = user_account(request_post_update2)
            self.all_passed = False
            print("Update Test Failed")
        except Exception as e:
            print(e)
            print("Update Test Passed")
            
        # attempt to delete at a different security level (5->3) and fail
        try:
            request_post_delete.user = bigshot
            render = user_account(request_post_delete)
            self.all_passed = False
            print("Delete Test Failed")
        except Exception as e:
            print(e)
            print("Delete Test Passed")