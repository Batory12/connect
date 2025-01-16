from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Post
from .forms import TopicForm, EntryForm, PostForm
from users.models import User

# Create your views here.

def index(request):
    """The home page for Learning Log"""
    us = request.user
    following = us.following.all()
    posts = Post.objects.filter(user__in=following).order_by('date_added')
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