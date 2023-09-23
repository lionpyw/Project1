from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from random import choice
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    page=util.get_entry(title)
    if page == None:
        return render(request, 'encyclopedia/E404.html', {
            "title": title,
            'error_message' : '404 not found'
        })
        
    content = Markdown().convert(page)
    return render(request, "encyclopedia/enter.html", {
        "content": content,
        "title": title
    })

def search(request):
    entries= util.list_entries()
    list=[]
    if request.method == 'POST':
        search = request.POST['q']
        for entry in entries:
            if search.lower() in entry.lower():
                list.append(entry)
        if len(list) == 0:
            title = search
            return render(request, 'encyclopedia/E404.html', {
                "title": title,
                'error_message' : 'No such topic found'
            })
        elif len(list) == 1 and search.lower() == list[0].lower():
            title= list[0]
            return HttpResponseRedirect(reverse("entry", args=(title,)))
        else:
            return render(request, "encyclopedia/search.html", {
        "entries": list
    })     
        
        
def create(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/create.html")
    elif request.method == 'POST':
        title =request.POST['title']
        content =request.POST['content']
        if util.get_entry(title) != None:
                return render(request, 'encyclopedia/E404.html', {
                "title": title,
                'error_message' : 'The Title already exists'
            })
        else:
            util.save_entry(title, content)
            content = Markdown().convert(content)
            return render(request, "encyclopedia/enter.html", {
        "content": content,
        "title": title
    })
            
def edit(request):
    if request.method == 'GET':
        title =request.GET['title']
        content =util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
        "content":content,
        "title": title
        })
    elif request.method == 'POST':
        title =request.POST['title']
        content =request.POST['content']
        util.save_entry(title, content)
        content = Markdown().convert(content)
        return render(request, "encyclopedia/enter.html", {
        "content":content,
        "title": title
    })
        
def random(request):
    entries=util.list_entries()
    title= choice(entries)
    page=util.get_entry(title)
    content = Markdown().convert(page)
    return render(request, "encyclopedia/enter.html", {
        "content":content,
        "title": title
    })