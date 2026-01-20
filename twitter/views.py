from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Post, User, Comment, Notification
from .forms import CustomUserCreationForm, UserUpdateForm, PostForm

@login_required
def home(request):
    # Otimização: traz o autor, o post original (se for RT) e pre-carrega likes e comentários
    followed_users = request.user.following.all()
    posts = Post.objects.filter(
        Q(author__in=followed_users) | Q(author=request.user)
    ).distinct().select_related('author', 'repost_of', 'repost_of__author').prefetch_related('likes', 'comments__author')

    # request.FILES é obrigatório para imagens e vídeos
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('home')
    
    return render(request, 'twitter/home.html', {'posts': posts, 'form': form})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
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
    posts = Post.objects.filter(author=view_user).select_related('author', 'repost_of').prefetch_related('likes', 'comments')
    return render(request, 'twitter/profile.html', {'view_user': view_user, 'posts': posts})

@login_required
def edit_profile(request):
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile', username=request.user.username)
    return render(request, 'twitter/edit_profile.html', {'form': form})

@login_required
def password_change_custom(request):
    """Troca a senha, desloga e manda para a tela de login limpa"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            logout(request)
            messages.success(request, 'Senha alterada! Entre com suas novas credenciais.')
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    liked = False
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        if post.author != request.user:
            Notification.objects.create(to_user=post.author, from_user=request.user, notification_type='L', post=post)
    
    # Suporte a AJAX (Não recarrega a página)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': post.likes.count()})
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def retweet(request, post_id):
    original_post = get_object_or_404(Post, id=post_id)
    # Sempre retuita o post original de verdade
    source_post = original_post.repost_of if original_post.repost_of else original_post
    
    # Lógica de RETWEET ÚNICO (Toggle)
    existing_rt = Post.objects.filter(author=request.user, repost_of=source_post).first()
    
    retweeted = False
    if existing_rt:
        existing_rt.delete()
        retweeted = False
    else:
        new_rt = Post.objects.create(author=request.user, repost_of=source_post)
        retweeted = True
        if source_post.author != request.user:
            Notification.objects.create(to_user=source_post.author, from_user=request.user, notification_type='R', post=new_rt)

    # Suporte a AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'retweeted': retweeted, 'count': source_post.reposts.count()})
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    if content:
        Comment.objects.create(post=post, author=request.user, content=content)
        if post.author != request.user:
            Notification.objects.create(to_user=post.author, from_user=request.user, notification_type='C', post=post)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def follow_unfollow(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user:
        if target_user in request.user.following.all():
            request.user.following.remove(target_user)
        else:
            request.user.following.add(target_user)
            Notification.objects.create(to_user=target_user, from_user=request.user, notification_type='F')
    return redirect('profile', username=username)

@login_required
def notifications(request):
    notifs = request.user.notifications.all()
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'twitter/notifications.html', {'notifications': notifs})

@login_required
def delete_post(request, post_id):
    # Garante que só o autor pode deletar o post ou o retweet
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

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