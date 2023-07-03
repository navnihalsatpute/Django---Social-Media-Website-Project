from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

@login_required(login_url='login')
def details(request):
    user_profile  = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('profileimg') == None:
            profileimg = user_profile.profileimg

        if request.FILES.get('profileimg') != None:
            profileimg = request.FILES.get('profileimg')
        
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = profileimg
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        messages.info(request, 'Changes Saved')
        return redirect('details')

    return render(request, 'details.html', {'user_profile': user_profile})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already in use')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email already in use')
            return redirect('signup') 
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)

            #creating a profile object for the new user
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            return redirect('details')
    else:
        return render(request, 'signup.html')
    
def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user= auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')

@login_required(login_url='login')    
def logout(request):
    auth.logout(request)
    return redirect('login')
