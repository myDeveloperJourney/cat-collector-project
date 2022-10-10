from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.shortcuts import render
from .models import Cat

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})

def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'cats/detail.html', {'cat': cat})

class CatsCreate(CreateView):
    model = Cat
    fields = '__all__'

class CatsUpdate(UpdateView):
    model = Cat
    fields = ('age', 'description')

class CatsDelete(DeleteView):
    model = Cat
    success_url = '/cats/'