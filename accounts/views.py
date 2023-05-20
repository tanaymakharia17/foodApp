from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages
def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        context = {}
        if form.is_valid():
            # create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False) # or form.save()
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account have been registered successfully")
            return redirect('registerUser')
        else:
            print(form.errors)
            messages.error(request, "Your account is not created, Please try again!")
            return render(request, 'accounts/registerUser.html', context={'form':form})
            # return HttpResponse('error')

        

    form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/registerUser.html', context)
    return HttpResponse('hello')