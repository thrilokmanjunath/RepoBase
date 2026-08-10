from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
def signup_view(request):
 if request.method == 'POST':
   form = UserCreationForm (request.POST)
   if form.is_valid():
    user = form.save()
    login(request, user)
    return redirect('home')
 else:
  form = UserCreationForm()
 return render(request,'repos/signup.html',{'form':form})


def login_view(request):
 if request.method =='POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
       user = form.get_user()
       login(request,user)
       return redirect('home')
 else:
       form = AuthenticationForm()
 return render(request,'repos/login.html',{'form':form})
 
 
def logout_view(request):
  logout(request)
  return redirect('login')
 

def home_view(request):
  return render(request,'repos/home.html')

def repo_detail_view(request, repo_id):
  return render(request, 'repos/repo_detail.html', {'repo_id': repo_id})