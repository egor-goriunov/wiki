from operator import is_not
from django.shortcuts import render
from django.http import HttpResponseNotFound
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
        return render(request,"encyclopedia/message.html",{"msg_title":"Success ","msg_text":"Your entry has been successfully created"})
    return render(request,"encyclopedia/new_entry.html",{})
