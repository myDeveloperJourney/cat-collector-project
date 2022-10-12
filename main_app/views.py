from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from .models import Cat, Toy, Photo
from .forms import FeedingForm

import boto3
import uuid

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'cat-collector-photo-uploads-1'

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
    # we need a list of toys that are not associated with the cat
    toys = Toy.objects.exclude(id__in=cat.toys.all().values_list('id')) # [1, 5, 10]
    return render(request, 'cats/detail.html', {
        'cat': cat, 
        'feeding_form': feeding_form,
        'toys': toys
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

def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cats_detail', cat_id=cat_id)

def add_photo(request, cat_id):
    # 1) capture form input - aka photo files
    photo_file = request.FILES.get('photo-files')
    # 2) if there is a photo file
    if photo_file:
        # 2.1 intialize a s3 client object
        s3 = boto3.client('s3')
        # 2.2 Create a unique id for the photo file
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # 2.3 Attempt to upload the photo
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
        # 2.4 If the photo uploaded successful
            # 2.4.1 We will capture the url of the photo hosted in our s3 bucket
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            # 2.4.2 We will create an instance of a photo object
            photo = Photo(url=url, cat_id=cat_id)
            # save the instance
            photo.save()
        except Exception as error:
        # 2.5 If not successful
            # 2.5.1 show errors in the console
            print('An error has occured uploading or saving the new photo')
            print(error)
    # 3) In every case, we'll always redirect back to the detail page for the cat
    return redirect('cats_detail', cat_id=cat_id)


class CatsCreate(CreateView):
    model = Cat
    fields = ('name', 'breed', 'description', 'age')

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