from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post

# Create your views here.
def home(request):
    return render(request, 'home/home.html')
def contact(request):
    if request.method == "POST":
        # print('We are using post')
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        content = request.POST['content']
        print(name, phone, email, content)
        if len(name) < 2 or len(phone) < 10 or len(email) < 5 or len(content) < 4:
            messages.error(request, 'Please fill the form correctly.')
        else:
            contact = Contact(name=name, phone=phone, email=email, content=content)
            contact.save()
            messages.success(request, 'Your form has been submitted.')
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query) > 50 or len(query) < 2:
        allPosts = []
        messages.warning(request, 'Please make sure your search keywords are in range of 2-50.')
    else:

        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    params = {'allPosts':allPosts, 'query':query}
    return render(request, 'home/search.html', params)

def signUp(request):
    # Fetching data from user
    if request.method == "POST":
        signusername = request.POST['signusername']
        fname = request.POST['fname']
        lname = request.POST['lname']
        signemail = request.POST['signemail']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Checking validations
        if len(signusername) > 10: 
            messages.error(request, 'Please make sure your username length is less than 10.')
            return redirect('home')
        if not signusername.isalnum(): 
            messages.error(request, 'username can only have numbers and alphabets.')
            return redirect('home')
        if password1 != password2: 
            messages.error(request, 'Passwords do not match.')
            return redirect('home')


        # Creating a user
        myuser = User.objects.create_user(signusername, signemail, password1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your account has been created.')
        return redirect('home')

    else:
        return HttpResponse("404 - Not found.")   

def userlogin(request):
    if request.method == "POST":
        loginUsername = request.POST['loginUsername']
        loginPassword = request.POST['loginPassword']

        user = authenticate(username=loginUsername, password=loginPassword)
        if user is not None:
            login(request,user)
            messages.success(request, 'Successfully logged in.')
            return redirect('home')
        
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('home')
    
    else:
        return HttpResponse("404 - Not found")

def userlogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')