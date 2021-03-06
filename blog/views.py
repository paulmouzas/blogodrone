from django.shortcuts import render, redirect
from django.http import Http404
from blog.models import Entry, Comment, UserProfile
from .forms import (LoginForm, SignupForm, PostForm, CommentForm,
        UpdateEmailForm, UpdateAboutForm)
from .utils import DivErrorList
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    entries_list = Entry.objects.all().order_by('-pub_date')
    paginator = Paginator(entries_list, 5)  # Show 5 entries per page
    entries = request.GET.get('page')
    try:
        entries = paginator.page(entries)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)

    dates = Entry.get_dates()
    context = { 'dates': dates, 'entries': entries}
    return render(request, 'blog/index.html', context)


def detail(request, entry_id):
    if request.method == "POST":
        form = CommentForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            author = request.user
            text = request.POST['text']
            entry = entry = Entry.objects.get(pk=entry_id)
            pub_date = timezone.now()
            comment = Comment(author=author,
                              entry=entry,
                              text=text,
                              pub_date=pub_date)
            comment.save()

    dates = Entry.get_dates()
    form = CommentForm()

    try:
        entry = Entry.objects.get(pk=entry_id)
    except Entry.DoesNotExist:
        raise Http404
    comments = Comment.objects.filter(entry=entry)
    context = {'entry': entry, 'dates': dates,
               'comments': comments, 'form': form}
    return render(request, 'blog/detail.html', context)

def login(request):
    if request.user.is_authenticated():
        return redirect('index')

    if request.method == "POST":
        form = LoginForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            user = form.login(request)
            if user:
                auth_login(request, user)
                return redirect('index')
    else:
        form = LoginForm()

    dates = Entry.get_dates()
    context = {'dates': dates, 'form': form}

    return render(request, 'blog/login_form.html', context)


def new_post(request):
    if not request.user.is_authenticated():
        return redirect('login')
    if request.method == "POST":
        form = PostForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            title = request.POST['title']
            post = request.POST['post']
            p = Entry(author=request.user,
                      title=title,
                      post=post,
                      pub_date=timezone.now())
            p.save()
            entry_id = p.pk
            return redirect('detail', entry_id=entry_id)
    else:
        form = PostForm

    dates = Entry.get_dates()
    context = {'dates': dates, 'form': form}

    return render(request, 'blog/new_post.html', context)


def signup(request):
    dates = Entry.get_dates()
    if request.method == "POST":
        form = SignupForm(request.POST, error_class=DivErrorList)

        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            User.objects.create_user(username=username,
                                     email=email,
                                     password=password)
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            auth_login(request, new_user)

            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html', {
                           'form': form,
                           'dates': dates})


def month(request, year, month):
    dates = get_dates()
    month_entry_list = Entry.objects.filter(pub_date__year=year,
                                            pub_date__month=month).order_by('-pub_date')  # NOQA
    return render(request, 'blog/list_post_by_month.html', {
        'month_entry_list': month_entry_list,
        'dates': dates
    })


def user_profile(request, username):

    dates = Entry.get_dates()
    logged_in_user = request.user

    try:
        instance = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

    try:
        user_profile = UserProfile.objects.get(user=instance)
    except ObjectDoesNotExist:
        user_profile = None

    context = {'view_user': instance,
               'user_profile': user_profile,
               'logged_in_user': logged_in_user,
               'dates': dates}

    return render(request, 'blog/user_profile.html', context)


def edit_user_profile(request):
    user = request.user
    if not user.is_authenticated():
        return redirect('login')

    try:
        about = UserProfile.objects.get(user=user).about
    except UserProfile.DoesNotExist:
        about = UserProfile.objects.create(user=user)

    dates = Entry.get_dates()

    update_email_form = UpdateEmailForm()
    update_about_form = UpdateAboutForm(initial={'about': about})

    return render(request, 'blog/edit_profile.html', {
                           'update_email_form': update_email_form,
                           'user': user,
                           'dates': dates,
                           'update_about_form': update_about_form})


def update_email(request):
    if request.method == "POST":
        update_email_form = UpdateEmailForm(request.POST, instance=request.user)
        if update_email_form.is_valid():
            update_email_form.save()
            return redirect('edit_user_profile')


def update_about(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)
    if request.method == "POST":
        update_about_form = UpdateAboutForm(data=request.POST,
                                            instance=user_profile,
                                            error_class=DivErrorList)
        update_about_form.save()
        return redirect(user_profile)
