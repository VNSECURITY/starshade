from django.core.serializers import json
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from . import datasource
from . import forms, models

import json

@login_required
def redirect_kibana(request):
    return HttpResponseRedirect("http://%s:5601/app/kibana" % (request.META['HTTP_HOST']))


@login_required
def home(request):
    return render(request, "dashboard/home.html", {
        "current_data" : datasource.current_data(),
        "threads" : datasource.threads(),
        "blocked" : datasource.blocked_data(),
    })


@login_required
def virtual_fix_list(request):
    return render(request, "dashboard/virtual_fix_list.html", {
        'page_name': "Virtual Fixes",
        'fixes': models.VirtualFix.objects.all()
    })

def virtual_fix_public(request):
    content = ""
    first = True
    for fix in models.VirtualFix.objects.all():
        if not first:
            content += ",\n"
        first = False
        content += fix.title + "\n"
        content += fix.patch + ""
    content += "\n"
    return HttpResponse(content)


def virtual_fix_version(request):
    content = ""
    first = True
    for fix in models.VirtualFix.objects.all():
        content += fix.title + "\n"
    return HttpResponse(content)


@login_required
def virtual_fix_new(request):
    if request.method == 'POST':
        form = forms.VirtualFixForm(request.POST)
    else:
        form = forms.VirtualFixForm()
    if form.is_valid():
        form.save()
        request.session['message'] = [{"type":"success","msg":"Fix created!"}]
        return HttpResponseRedirect(reverse('virtual_fix_edit', kwargs={'id':form.instance.pk}))
    return render(request, "dashboard/virtual_fix_edit.html", {
        'page_name': "New Virtual Fix",
        'form': form
    })

@login_required
def virtual_fix_edit(request, id):
    fix = get_object_or_404(models.VirtualFix, pk=id)

    if request.method == 'POST':
        form = forms.VirtualFixForm(request.POST, instance=fix)
        if form.is_valid():
            form.save()
            request.session['message'] = [{"type":"info","msg":"Fix updated!"}]
    else:
        form = forms.VirtualFixForm(instance=fix)

    return render(request,"dashboard/virtual_fix_edit.html", {
        'page_name' : ("Edit Virtual Fix"),
        'form' : form
    })

@login_required
def virtual_fix_remove(request, id):
    try:
        fix = get_object_or_404(models.VirtualFix, pk=id)
        fix.delete()
        request.session['message'] = [{"type":"info","msg":"Fix deleted!"}]
    except:
        request.session['message'] = [{"type":"danger","msg":"Failed to delete fix!"}]
    return HttpResponseRedirect(reverse('virtual_fix_list'))


def threads(request):
    return render_to_response('dashboard/threads.html',{
        "page_name" : "Threads",
        "threads": datasource.threads(),
    })
