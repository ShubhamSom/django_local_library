from django.shortcuts import render


# Create your views here.

def home_page(request_type):
    return render(request_type, 'index.htm')
