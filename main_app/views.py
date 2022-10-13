from atexit import register
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect

from .models import Cat, Toy, Photo

from django.contrib.auth import login

from .forms import FeedingForm
from django.contrib.auth.forms import UserCreationForm


import boto3
import uuid

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'cat-collector-photo-uploads-1'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def cats_index(request):
    cats = Cat.objects.filter(user=request.user)
    return render(request, 'cats/index.html', {'cats': cats})

@login_required
def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()
    # we need a list of toys that are not associated with the cat
    toys = Toy.objects.exclude(id__in=cat.toys.all().values_list('id')) # [1, 5, 10]
    
    import datetime
    today = datetime.datetime.today()

    todays_feedings = cat.feeding_set.filter(date=today)
    return render(request, 'cats/detail.html', {
        'cat': cat, 
        'feeding_form': feeding_form,
        'toys': toys,
        'todays_feedings': todays_feedings
    })

@login_required
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

@login_required
def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cats_detail', cat_id=cat_id)

@login_required
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

def signup(request):
    # what do with POST Requests?
    error_message = None
    if request.method == 'POST':
        # capture user input from the form submission
        form = UserCreationForm(request.POST)
        # check the form to ensure it's valid
        if form.is_valid():
            # use the user input to create a new user in the database
            user = form.save()
            # log the user in
            login(request, user)
            # redirect the user to the cats_index page
            return redirect('cats_index')
        else:
            # if the form data is not valid, we'll set an error message
            error_message = 'Signup input invalid - Please try again'
    # what to do with GET Requests?
    # create an instance of the UserCreateForm and provide the form as context to 
    # the template
    form = UserCreationForm()
    # render the signup template
    context = { 'form': form, 'error': error_message }
    return render(request, 'registration/signup.html', context)

class CatsCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ('name', 'breed', 'description', 'age')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CatsUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ('age', 'description')

class CatsDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'

class ToysCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = ('name', 'color')

class ToysIndex(LoginRequiredMixin, ListView):
    template_name = 'toys/index.html'
    model = Toy

class ToysDetail(LoginRequiredMixin, DetailView):
    template_name = 'toys/detail.html'
    model = Toy

class ToysUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ('name', 'color')

class ToysDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'