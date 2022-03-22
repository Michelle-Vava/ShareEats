from django.test import TestCase, Client

# Testing Django views
# is it loading the correct URl call?
# Does it return the correct status code?
# Compare the data point return by the View
# Is it rendered by the correct Template
"""
Run the command : python manage.py test
The Django Test Client : python class that acts a s a dummy browser
Allows you to test your views
Available at django.test.Client
With that ShareEats can:
 - Simulate GET and POST requests
 - See the chain of redirects 
 - Check out rendered Templates with context
Not intended to be a replacement of Selenium
Testing client does not require the Web server to be running
"""


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        # self.user = User.objects.create(username='alex', password='2421djfes')
        # self.buyer = BuyerInfo.objects.create(firstname='alex', lastname='peters', business_phone_number='9023188172',
        # logged_in= login_sample_user(self.client)

    def test_home_page(self):
        response = self.client.get('http://127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)

    # def login_sample_user(client):
    #     logged_in = client.post(reverse('users:login'),
    #                             data={
    #                                 'username': 'test44@gmail.com',
    #                                 'password': 'rsfslsd',
    #                             })
    #     return logged_in
