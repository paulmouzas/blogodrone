from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from blog.models import Entry, LoginForm, SignupForm, PostForm, Comment, CommentForm, UpdateEmailForm, UpdateAboutForm, UserProfile
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.utils.safestring import mark_safe
from django.forms.util import ErrorList


class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
       if not self: return u''
       return mark_safe(u'<div>%s</div>' % ''.join([u'<div class="alert alert-danger">%s</div>' % e for e in self]))

def filter_datetime_by_month(seq):
    """ Takes in a list of datetime objects and returns list
    of datetimes with no month that is the same """

    seen = set()
    unique_datetimes = []
    for date in seq:
        if (date.month, date.year) not in seen:
            unique_datetimes.append(date)
            seen.add((date.month, date.year))
    return unique_datetimes


def index(request):
    entries_list = Entry.objects.all().order_by('-pub_date')
    paginator = Paginator(entries_list, 5) # Show 5 entries per page
    entries = request.GET.get('page')
    try:
        entries = paginator.page(entries)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)
    #latest_entry_list = entries[:5]
    template = loader.get_template('blog/index.html')
    dates = filter_datetime_by_month([entry.pub_date for entry in entries_list])
    context = RequestContext(request, {
        'entries': entries,
        'dates': dates
    })
    return HttpResponse(template.render(context))

def detail(request, entry_id):
    if request.method == "POST":
        form = CommentForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            author = request.user
            text = request.POST['text']
            entry = entry = Entry.objects.get(pk=entry_id)
            pub_date = timezone.now()
            comment = Comment(author=author, entry=entry, text=text,
                    pub_date=pub_date)
            comment.save()

    entries_list = Entry.objects.all().order_by('-pub_date')
    dates = filter_datetime_by_month([entry.pub_date for entry in entries_list])
    form = CommentForm()


    try:
        entry = Entry.objects.get(pk=entry_id)
    except Entry.DoesNotExist:
        raise Http404
    comments = Comment.objects.filter(entry=entry)
    return render(request, 'blog/detail.html', {'entry': entry,
                                                'dates': dates,
						'comments': comments,
                                                'form': form,
                                               })

def login(request):
    if request.user.is_authenticated():
        return redirect('index')
    entries_list = Entry.objects.all().order_by('-pub_date')
    dates = filter_datetime_by_month([entry.pub_date for entry in entries_list])
    if request.method == "POST":
        form = LoginForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = form.login(request)
            if user:
                auth_login(request, user)
                return HttpResponseRedirect('/blog/')
    else:
        form = LoginForm()

    return render(request, 'blog/login_form.html', {
        'form': form,
        'dates': dates
    })

def new_post(request):
    entries_list = Entry.objects.all().order_by('-pub_date')
    dates = filter_datetime_by_month([entry.pub_date for entry in entries_list]) 
    if not request.user.is_authenticated():
        return redirect('login')
    if request.method == "POST":
        form = PostForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            title = request.POST['title']
            post = request.POST['post']
            p = Entry(author=request.user, title=title, post=post, pub_date=timezone.now())
            p.save()
            entry_id = p.pk
            return redirect('detail', entry_id=entry_id)
    else:
        form = PostForm

    return render(request, 'blog/new_post.html', {
        'form': form,
        'dates': dates,
    })

def signup(request):
    entries_list = Entry.objects.all().order_by('-pub_date')
    dates = filter_datetime_by_month([entry.pub_date for entry in entries_list])
    if request.method == "POST":
        form = SignupForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            create_user = User.objects.create_user(username=username, email=email, password=password)
            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            auth_login(request, new_user)

            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html',{
        'form': form,
        'dates': dates,
    })

def month(request, year, month):
    entries_list = Entry.objects.all().order_by('-pub_date')
    dates = filter_datetime_by_month([entry.pub_date for entry in entries_list])
    month_entry_list = Entry.objects.filter(pub_date__year=year, pub_date__month=month).order_by('-pub_date') 
    return render(request, 'blog/list_post_by_month.html', {
        'month_entry_list': month_entry_list,
        'dates': dates
    })

def user_profile(request, username):

    entries_list = Entry.objects.all().order_by('-pub_date')
    dates = filter_datetime_by_month([entry.pub_date for entry in entries_list])
    try:
        instance = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=instance)
    except ObjectDoesNotExist:
        raise Http404 

    return render(request, 'blog/user_profile.html', {
               'view_user': instance,
               'user_profile': user_profile,
               'dates': dates,
             })


def edit_user_profile(request):
    user = request.user
    if not user.is_authenticated():
        return redirect('login')

    entries_list = Entry.objects.all().order_by('-pub_date')
    dates = filter_datetime_by_month([entry.pub_date for entry in entries_list])

    update_email_form = UpdateEmailForm()
    update_about_form = UpdateAboutForm()


    return render(request, 'blog/edit_profile.html', {
              'update_email_form': update_email_form,
              'user': user,
             'dates': dates,
             'update_about_form': update_about_form
           })


def update_email(request):
    user = request.user
    if request.method == "POST":
        update_email_form = UpdateEmailForm(data=request.POST, instance=user, error_class=DivErrorList)
        if update_email_form.is_valid():
            update_email_form.save()
            user.save()
            return redirect('edit_user_profile')

def update_about(request):
    user = request.user
    if request.method == "POST":
        update_about_form = UpdateAboutForm(data=request.POST, instance=user, error_class=DivErrorList)
        if update_about_form.is_valid():
            update_about_form.save()
            user.save()
            return redirect('edit_user_profile')
