from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import util
from django import forms
import random
from markdown2 import Markdown

mark = Markdown()

#Why I use widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder' : 'Search'})) this here???
class Search(forms.Form):
	item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder' : 'Search'}))
# Why I use form.CharField(widget = forms.Textarea(), label = '') this?
class Post(forms.Form):
	title = forms.CharField(label = 'Title')
	textarea = forms.CharField(widget = forms.Textarea(), label = '')
class Edit(forms.Form):
	textarea = forms.CharField(widget = forms.Textarea(), label = '')
	
def index(request):
	entries = util.list_entries()
	search_list = []
	if request.method == "POST":
		form = Search(request.POST)
		if form.is_valid():
			item = form.cleaned_data["item"]
			for i in entries:
				if item in entries:
					page = util.get_entry(item)
					page_convert = mark.convert(page)
					return render(request,"encyclopedia/add.html", {
						"article" : page_convert, 'title' : item, "form" : Search()
						})
				elif item.lower() in i.lower():
					search_list.append(i) 
			return render(request,"encyclopedia/search.html",{
				"searched" : search_list, "form" : Search()
				})
		
		else:
			return render(request, "encyclopedia/index.html", {
					"form":form
				})
	else:
		return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),"form" : Search()
    })


def add(request, title):
	if title in util.list_entries():
		page = util.get_entry(title)
		page_convert = mark.convert(page)
		return render(request, "encyclopedia/add.html",{
		"article": page_convert, "title" : title, "form" : Search()
		})
	else:
		return render(request,"encyclopedia/error.html",{
			"message":"The requested page was not found.", "form" : Search()
			})

def create(request):
	if request.method == "POST":
		form = Post(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			textarea = form.cleaned_data["textarea"]
			entries = util.list_entries()
			if title in entries:
				return render(request, "encyclopedia/error.html", {
					"message" : "Text already exist!", "form" : Search()
					})
			else:
				util.save_entry(title, textarea)
				page = util.get_entry(title)
				page_convert = mark.convert(page)
				return render(request, "encyclopedia/add.html",{
					"article" : page_convert, "form" : Search()
					})
	else:
		return render(request, "encyclopedia/create.html",{
			"pos": Post(), "form" : Search()
			})

def edit(request,title):
	
	if request.method == "GET":
		page = util.get_entry(title)
		return render(request, "encyclopedia/edit.html",{
			"title" : title, "edit": Edit(initial={'textarea': page}), "form" : Search()
			})
	else:
		form = Edit(request.POST)
		if form.is_valid():
			textarea = form.cleaned_data['textarea']
			util.save_entry(title,textarea)
			page = util.get_entry(title)
			page_convert = mark.convert(page)
			return render(request, "encyclopedia/add.html", {
				"article" : page_convert, "form" : Search()
				})
def randomPage(request):
	entries = util.list_entries()
	num = random.randint(0, len(entries) - 1)
	page_random = entries[num]
	page = util.get_entry(page_random)
	page_convert = mark.convert(page)
	return render(request, "encyclopedia/add.html",{
		"article" : page_convert, "form" : Search()
		})
