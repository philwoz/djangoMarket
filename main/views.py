from django.shortcuts import render, redirect
from main.models import Item
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.

def homepage(request):
    return render(request, template_name='main/home.html')


def itemspage(request):
    if request.method == 'GET':
        items = Item.objects.all().filter(owner=None)
        return render(request, template_name='main/items.html', context={'items': items})
    if request.method == 'POST':
        purchase_item = request.POST.get('purchased-item')
        if purchase_item:
            purchased_item_object = Item.objects.get(name=purchase_item)
            purchased_item_object.owner = request.user
            purchased_item_object.save()
            messages.success(request, f'Congratulations you now own this {purchased_item_object.name}')
        return redirect('items')

def myitemspage(request):

    if request.method == 'GET':
        # user = request.user
        items = Item.objects.all().filter(owner=request.user)
        return render(request, template_name='main/myitemspage.html', context={'items': items})

    if request.method == 'POST':
        sold_item = request.POST.get('sold-item')
        if sold_item:
            sold_item_object = Item.objects.get(name=sold_item)
            sold_item_object.owner = None
            sold_item_object.save()
            messages.success(request, f'Success you sold {sold_item_object.name} back to the market')
            return redirect('myitemspage')

def loginpage(request):
    if request.method == 'GET':
        return render(request, template_name='main/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'You are logged in as {user.username} !')
            return redirect('items')
        else:
            messages.error(request, 'Combination of username and password is wrong')
            return redirect('login')

def registerpage(request):
    if request.method == 'GET':
        return render(request, template_name='main/register.html')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'You have successfully created a new account!. Logged in as {user.username}')
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect('register')



def logoutpage(request):
    logout(request)
    messages.success(request, f'You have logged out!')
    return redirect('home')