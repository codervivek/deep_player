from django.shortcuts import render

# Create your views here.
from deep_player.forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import Video
from django.db.models import Max
from django.views import generic

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):

    video = Video.objects.annotate(
        max_created=Max("created_date")
    ).order_by("-max_created")


    return render(request, 'index.html', {'videos': video})

class VideoDetailView(generic.DetailView):
    model=Video

def fileupload(request):
    return render(request, 'upload.html')
