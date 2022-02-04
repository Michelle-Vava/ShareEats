from django.shortcuts import render
from django.views import generic
"""
"""


# Create your views here.

# home view
# renders the view for the home page
def home(request):
    return render(request, 'api/home.html')

# TODO : To add all the remain views
