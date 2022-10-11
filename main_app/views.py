from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from .models import Cat, Toy
from .forms import FeedingForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})

def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {
        'cat': cat, 
        'feeding_form': feeding_form
    })

def add_feeding(request, cat_id):
    # capture form input from the request
    print(request.POST)
    form = FeedingForm(request.POST) # {'date': '2022-10-11', meal: 'B'}
    # validate form data
    if form.is_valid():
    # save the form data - make sure we reference the cat_id in the feeding
      new_feeding = form.save(commit=False) # saves in memory without committing to the database
      new_feeding.cat_id = cat_id
      new_feeding.save() # this will save to the database now
    # redirect back to the detail page
    else: 
        print(form.errors)
    return redirect('cats_detail', cat_id=cat_id)

class CatsCreate(CreateView):
    model = Cat
    fields = '__all__'

class CatsUpdate(UpdateView):
    model = Cat
    fields = ('age', 'description')

class CatsDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

class ToysCreate(CreateView):
    model = Toy
    fields = ('name', 'color')

class ToysIndex(ListView):
    template_name = 'toys/index.html'
    model = Toy

class ToysDetail(DetailView):
    template_name = 'toys/detail.html'
    model = Toy

class ToysUpdate(UpdateView):
    model = Toy
    fields = ('name', 'color')

class ToysDelete(DeleteView):
    model = Toy
    success_url = '/toys/'