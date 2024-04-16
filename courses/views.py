from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the courses index.")

def welcome(request, year):
    return HttpResponse("Welcome to " + str(year))

# Class-based views
class TestView(View):
    def get(seft , request):
        return HttpResponse("Test View")

    def post(seft , request):
        pass