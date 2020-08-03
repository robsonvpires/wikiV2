from django.shortcuts import render
from django import forms
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

class Page(forms.Form):
    title = forms.CharField(max_length=20, widget=forms.Textarea(attrs={'rows': 1,'style': 'height: 2em;'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 20em;'}))

def load_page(request, title):
    md = markdown2.Markdown()
    page = util.get_entry(title)

    if page:
        return render(request, 'encyclopedia/page.html', {
            'title':title, 
            'content': md.convert(util.get_entry(title))
        }) 
    else:
        return render(request, 'encyclopedia/not_found.html', {
            'title':title
        })
        

def random_page(request):
    md = markdown2.Markdown()
    page = random.randint(0,(len(util.list_entries())-1))
 
    return render(request, 'encyclopedia/random.html', {
        'title':util.list_entries()[page], 
        'content':md.convert(util.get_entry(util.list_entries()[page]))
    })

def edit(request, title):
    md = markdown2.Markdown()
    if request.method == 'POST':
        form = Page(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            util.save_entry(title,content)
            return render(request, 'encyclopedia/page.html',{
                'title':title, 
                'content':md.convert(content)
            })
    else:
        edit_page = Page({'title':title, 'content':util.get_entry(title)})
        return render(request, 'encyclopedia/edit.html',{
            'edit_page':edit_page
        })

def new_page(request):
    if request.method == 'POST':
        md = markdown2.Markdown()
        new_form = Page(request.POST)
        if new_form.is_valid():
            title = new_form.cleaned_data.get('title')
            content = new_form.cleaned_data.get('content')
            for i in util.list_entries():
                if i.upper() == title.upper():
                    return render(request, 'encyclopedia/already_exist.html',{
                        'title': title })
            else:
                util.save_entry(title, content)
                page = util.get_entry(new_form.cleaned_data.get('title'))
                return render(request, 'encyclopedia/page.html', {
                    'title':new_form.cleaned_data.get('title'), 'content':md.convert(page)})
    else:
        new_form = Page()
        return render(request,'encyclopedia/new.html',{'new_form':new_form})

def search(request):
    if request.method == 'POST':
        md = markdown2.Markdown()
        query = request.POST['q']
        entries = []

        for i in util.list_entries():
            if i.upper() == query.upper():
                return render(request, 'encyclopedia/page.html', {
                    'title':query, 
                    'content': md.convert(util.get_entry(query))    
                })
        
        for j in util.list_entries():
            if query.upper() in j.upper():
                entries.append(j) 
        return render(request, 'encyclopedia/search.html', {
            'entries': entries, 'query':query
        })
