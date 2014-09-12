from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from blog.models import Entry
from django.contrib.auth import logout

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

    
