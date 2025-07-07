from django.shortcuts import render


def index(request):
    return render(request,'home.html')  # adjust template path

def register(request):
    return render(request,'registration.html')

def blog(request):
    return render(request,'blog.html')
 
def investor(request):
    return render(request,'investing insights.html')

def contact(request):
    return render(request,'contact.html')
