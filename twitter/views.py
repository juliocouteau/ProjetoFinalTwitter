from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Post, User, Comment
from .forms import CustomUserCreationForm, UserUpdateForm, PostForm

@login_required
def home(request):
    followed_users = request.user.following.all()
    posts = Post.objects.filter(author__in=followed_users | User.objects.filter(id=request.user.id)).distinct()
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('home')
    return render(request, 'twitter/home.html', {'posts': posts, 'form': form})

def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request, username):
    view_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=view_user)
    return render(request, 'twitter/profile.html', {'view_user': view_user, 'posts': posts})

@login_required
def edit_profile(request):
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile', username=request.user.username)
    return render(request, 'twitter/edit_profile.html', {'form': form})

@login_required
def follow_unfollow(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user:
        if target_user in request.user.following.all():
            request.user.following.remove(target_user)
        else:
            request.user.following.add(target_user)
    return redirect('profile', username=username)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    if content:
        Comment.objects.create(post=post, author=request.user, content=content)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('home')

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    results = User.objects.filter(username__icontains=query).exclude(id=request.user.id) if query else []
    return render(request, 'twitter/search.html', {'results': results, 'query': query})

@login_required
def followers_list(request, username):
    view_user = get_object_or_404(User, username=username)
    return render(request, 'twitter/user_list.html', {'title': 'Seguidores', 'users': view_user.followers.all()})

@login_required
def following_list(request, username):
    view_user = get_object_or_404(User, username=username)
    return render(request, 'twitter/user_list.html', {'title': 'Seguindo', 'users': view_user.following.all()})