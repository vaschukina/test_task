from django.shortcuts import render
from .models import Site
import sys
import os
import subprocess
from django.http import HttpResponseRedirect
import pyperclip

def show(request):
    objs=Site.objects.all()
    data = {"objs": objs}
    return render(request, "index.html", context=data)

def post_site(request):
    name = request.POST.get("path")
    proc = subprocess.run( ['nslookup', name], stdout=subprocess.PIPE, text = True )
    f = False
    ip = ""
    for line in proc.stdout.splitlines():
        if f == True:
            if len(line)>0:
                ip += ", " + line.strip()
        if line.find("Addresses:")>-1:
            ip = line[10:].strip()
            f = True

    S  = Site(path = name, ip = ip)
    S.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_site(request):
    id = request.POST.get("id")[:-1]
    Site.objects.filter(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def copy_ip(request):
    objs=list(Site.objects.all().values_list('ip', flat=True))
    pyperclip.copy(", ".join( objs ))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
