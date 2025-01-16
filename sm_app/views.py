from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic import CreateView

from .models import Post, Like, Repost
from .forms import TopicForm, EntryForm, PostForm, CommentForm
from users.models import User

# Create your views here.

def index(request):
    """The home page for Learning Log"""
    us = request.user
    following = us.following.all()
    reposts = Post.objects.select_related('repost_set').filter(user__in=following)
    posts = (Post.objects.filter(user__in=following) | reposts).distinct().order_by('date_added')
    return render(request, 'sm_app/index.html', {'posts': posts})



@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'sm_app/profiles.html', context)


@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'sm_app/topic.html', context)

@login_required()
def handle_like(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.like_set.filter(user=request.user).count() > 0:
        post.likeCount -= 1
        post.like_set.filter(user=request.user).delete()
        post.save()
    else:
        post.likeCount += 1
        like = Like()
        like.user = request.user
        like.post = post
        like.save()
        post.save()
    return redirect('sm_app:index')
@login_required()
def handle_follow(request, user_id):
    usr  = User.objects.get(id=user_id)
    # unfollow
    if request.user.following.contains(usr):
        request.user.following_count -= 1
        request.user.following.remove(usr)
        usr.followers.remove(request.user)
        usr.follower_count -= 1
    else:
        request.user.following_count += 1
        request.user.following.add(usr)
        usr.followers.add(request.user)
        usr.follower_count += 1
    usr.save()
    request.user.save()
    return redirect('sm_app:profiles')
@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        # No data submitted; create a blank form
        form = TopicForm()
    else:
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('sm_app:topics')
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'sm_app/new_topic.html', context)


@login_required
def new_post(request):
    """Add a new post"""
    if request.method != 'POST':
        # No data submitted, create a blank form.
        form = PostForm()
    else:
        # POST data submitted; process data.
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('sm_app:index')

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'sm_app/new_post.html', context)


@login_required
def edit_post(request, entry_id):
    """Edit an existing post"""
    post = Post.objects.get(id=entry_id)
    check_post_owner(post, request)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry
        form = EntryForm(instance=post)
    else:
        # POST data submitted, process data
        form = EntryForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('sm_app:topic', topic_id=topic.id)
    context = {'post': post, 'topic': topic, 'form': form}
    return render(request, 'sm_app/edit_post.html', context)


def check_post_owner(post, request):
    """Make sure the post belongs to the current user."""
    if post.user != request.user:
        raise Http404


@login_required

def profiles(request):
    """Show all user profiles"""
    profiles = User.objects.all().exclude(id=request.user.id)
    context = {'profiles': profiles}
    return render(request, 'sm_app/profiles.html', context)

@login_required()
def handle_repost(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.repost_set.filter(user=request.user).count() == 0:
        post.repostCount += 1
        repost = Repost()
        repost.user = request.user
        repost.post = post
        repost.save()
        post.save()
    return redirect('sm_app:index')


def handle_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method != 'POST':
        # No data submitted, create a blank form.
        form = CommentForm()
    else:
        # POST data submitted; process data.
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            post.commentCount += 1
            comment.save()
            post.save()
            return redirect('sm_app:index')

    # Display a blank or invalid form.
    context = {'post': post, 'form': form}
    return render(request, 'sm_app/add_comment.html', context)



