from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from .forms import UpdateFullNameForm 
from django.contrib.auth.forms import PasswordChangeForm 
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        post_id = request.POST.get('post_id')
        content = request.POST.get('comment_content', '').strip()
        if post_id and content:
            post = get_object_or_404(Post, id=post_id)
            Comment.objects.create(post=post, author=request.user, content=content)
            return redirect('index')

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    user = request.user
    
    if request.method == 'POST':
        if 'update_name' in request.POST:
            name_form = UpdateFullNameForm(request.POST)
            password_form = PasswordChangeForm(user)
            if name_form.is_valid():
                full_name = name_form.cleaned_data['full_name'].strip()
                names = full_name.split(' ', 1)
                user.first_name = names[0]
                user.last_name = names[1] if len(names) > 1 else ''
                user.save()
                messages.success(request, "Change saved.")
                return redirect('profile')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            name_form = UpdateFullNameForm(initial={'full_name': f"{user.first_name} {user.last_name}"})
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  
                messages.success(request, "Change saved.")
                return redirect('profile')
    else:
        name_form = UpdateFullNameForm(initial={'full_name': f"{user.first_name} {user.last_name}"})
        password_form = PasswordChangeForm(user)
        
    posts = Post.objects.filter(author=request.user).order_by('-created_at')

    return render(request, 'profile.html', {
        'name_form': name_form,
        'password_form': password_form,
        'posts': posts,
    })

    return render(request, 'profile.html', context)

@login_required
def new_post(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Post.objects.create(author=request.user, content=content)
    return redirect('profile')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            post.content = content
            post.save()
    return redirect('profile')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
    return redirect('profile')