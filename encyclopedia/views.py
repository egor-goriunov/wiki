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
