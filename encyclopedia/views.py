from operator import is_not
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
import markdown2
from . import util
  

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show_entry(request,entry):
    entry_text = util.get_entry(entry)
    if entry_text is None:
        return HttpResponseNotFound(f"<h1>Article {entry} not found. </h1>")
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "entry_text": markdown2.markdown (entry_text)
    })

def search(request):
    search_text=request.GET['q']
    all_entries= util.list_entries()
    search_results=[]
    for entry in all_entries:
        if entry.find(search_text) != -1:
            search_results.append(entry)
    return render(request,"encyclopedia/search.html",{
        "search_text":search_text,
        "search_results":search_results 
    }) 

def new_entry(request):
    if request.method == "POST":
        entry_title=request.POST['title']
        if entry_title == "": 
            return render(request,"encyclopedia/message.html",{"msg_title":"Error","msg_text":"Title is empty"})
        entry_text=request.POST['entry']
        if entry_text == "":
            return render(request,"encyclopedia/message.html",{"msg_title":"Error","msg_text":"Entry is empty"})
        if not (util.get_entry(entry_title) is None):
            return render(request,"encyclopedia/message.html",{"msg_title":"Error","msg_text":"This entry already exists"})
        util.save_entry(entry_title, entry_text)
        return HttpResponseRedirect(f"wiki/{entry_title}") 
    return render(request,"encyclopedia/new_entry.html",{})

def edit_entry(request):
    if request.method == "POST":
        entry_title=request.POST['entry']
        if entry_title == "": 
            return render(request,"encyclopedia/message.html",{"msg_title":"Error","msg_text":"Entry title is empty"})
        entry_text=request.POST['entry_text']
        if entry_text == "":
            return render(request,"encyclopedia/message.html",{"msg_title":"Error","msg_text":"Entry text is empty"})
        util.save_entry(entry_title, entry_text)
        return HttpResponseRedirect(f"wiki/{entry_title}") 
    if "entry" in request.GET.keys(): 
        entry_title=request.GET['entry']
    else:
        return render(request,"encyclopedia/message.html",{"msg_title":"Error","msg_text":"Entry not specified"}) 
    if entry_title == "": 
        return render(request,"encyclopedia/message.html",{"msg_title":"Error","msg_text":"Entry title is empty"})
    entry_text=util.get_entry(entry_title)
    if entry_text is None:
        return render(request,"encyclopedia/message.html",{"msg_title":"Error","msg_text":f"Entry {entry_title} does not exist"})    
    return render(request,"encyclopedia/edit_entry.html",{"entry":entry_title, "entry_text":entry_text})
