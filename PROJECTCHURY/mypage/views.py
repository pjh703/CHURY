from django.shortcuts import render

# Create your views here.

def LibraryView(request):
    return render(request, "mypage/library.html")
