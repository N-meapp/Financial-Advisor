from django.shortcuts import render


def index(request):
    return render(request,'home.html')  # adjust template path

def register(request):
    return render(request,'registration.html')
 



