from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from blog.models import Entry, LoginForm, SignupForm
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

def index(request):
    latest_entry_list = Entry.objects.order_by('-pub_date')[:5]
    template = loader.get_template('blog/index.html')
    context = RequestContext(request, {
        'latest_entry_list': latest_entry_list
    })
    return HttpResponse(template.render(context))
    
def detail(request, entry_id):
    try:
        entry = Entry.objects.get(pk=entry_id)
    except Entry.DoesNotExist:
        raise Http404
    return render(request, 'blog/detail.html', {'entry': entry})
    
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/blog/')
            else:
                pass
        else:
            pass
    else:
        form = LoginForm()
        
    return render(request, 'blog/login_form.html', {
        'form': form
    })
    
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        print 'in signup'
        
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html',{
        'form': form
    })
