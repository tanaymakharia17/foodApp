from django.http import HttpResponse


def home(request):
    # return "hello"
    print("hello")
    return HttpResponse("Hello to home page")