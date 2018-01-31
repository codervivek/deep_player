from django.shortcuts import render

# Create your views here.
from deep_player.forms import SignUpForm, UploadForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import Video
from django.db.models import Max
from django.views import generic
from django.contrib.auth.models import User
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
    for vi in video:
        if not (vi.json):
            headers = {
                # Request headers
                'Ocp-Apim-Subscription-Key': '8eec2a625b584342b4adde9c7ea87c6a',
            }

            params = urllib.parse.urlencode({
                # Request parameters
                'id': vi.embed,
            })

            try:
                conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
                conn.request("GET", "/Breakdowns/Api/Partner/Breakdowns/{id}?%s" % params, "", headers)
                response = conn.getresponse()
                string = response.read().decode('utf-8')
                json_obj = json.loads(string)
                print(json_obj)
                if(json_obj["state"]=="Processed"):
                    v=Video.objects.get(id=vi.id)
                    v.json=string
                    v.thumbnail=json_obj["summarizedInsights"]["thumbnailUrl"]
                    v.processed=None
                    a=json_obj["breakdowns"][0]["insights"]["contentModeration"]["adultClassifierValue"]
                    if (a>0.8):
                        v.adult='a'
                    else:
                        v.adult=None
                    v.save()
                    # print(json_obj["summarizedInsights"]["thumbnailUrl"])
                else:
                    v=Video.objects.get(id=vi.id)
                    print(json_obj)
                    v.processed=json_obj["breakdowns"][0]["processingProgress"]
                    v.save()
                conn.close()
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))


    return render(request, 'index.html', {'videos': video})


class VideoDetailView(generic.DetailView):
    model=Video

import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
def fileupload(request):
    # a=Video.objects.create(name="GOT",embed="60bbdcb789",user=request.user)
    # a.save()
    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            headers = {
                # Request headers
                'Content-Type': 'multipart/form-data',
                'Ocp-Apim-Subscription-Key': '8eec2a625b584342b4adde9c7ea87c6a',
            }
            n=form.cleaned_data.get('name')
            u=form.cleaned_data.get('url')
            user1=form.cleaned_data.get('user')
            params = urllib.parse.urlencode({
                # Request parameters
                'name': n,
                'privacy': 'Public',
                'videoUrl': u,
            })

            # try:
            conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
            conn.request("POST", "/Breakdowns/Api/Partner/Breakdowns?%s" % params, "", headers)
            response = conn.getresponse()
            string = response.read().decode('utf-8')
            json_obj = json.loads(string)
            user1=User.objects.get(id=user1)
            new_video = Video.objects.create(name=n,embed=json_obj,user=user1)
            new_video.save()
            # print(response.content)
            conn.close()
            return redirect('home')
            # except Exception as e:
            #     print("[Errno {0}] {1}".format(e.errno, e.strerror))
            #     return redirect('admin')
    else:
        form=UploadForm
    return render(request, 'upload.html',{'form':form})

def my_videos(request):
    video = Video.objects.annotate(
        max_created=Max("created_date")
    ).order_by("-max_created")
    return render(request, 'my_videos.html', {'videos': video})

def xyz(request):
    return render(request,'xyz.html')

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import ListView

class SearchListView(ListView):
    model = Video

    def get_queryset(self):
        qs = Video.objects.all()
        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vector = SearchVector('json','name')
            qs = qs.annotate(search=vector).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')

        return qs

import json
from django.http import HttpResponse
from django.http import Http404  
# import 
def sceneSearch(request):
    qs = Video.objects.all()
    movie = request.GET.get('movie')
    transript = request.GET.get('transcript')
    print(movie)
    m = 'abc'
    string = 'ab'
    if movie and not transript:
        query = SearchQuery(movie)
        vector=SearchVector('name')
        qs = qs.annotate(search=vector).filter(search=query)
        qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')
        print(qs)
        m = qs[:1]
        q = request.GET.get('q')
        if not q:
            return render(request, 'scene.html', {'video':m[0]})
        print(m[0].name)
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': '8eec2a625b584342b4adde9c7ea87c6a',
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'id': m[0].embed,
            'query': q,
            'pageSize': '1',
        })

        # try:
        conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
        conn.request("GET", "/Breakdowns/Api/Partner/Breakdowns/Search?%s" % params, "", headers)
        print("/Breakdowns/Api/Partner/Breakdowns/Search?%s" % params)
        response = conn.getresponse()
        string = response.read().decode('utf-8')
        json_obj=json.loads(string)
        if not (json_obj["results"]):
            return render(request,'failed.html')
        if(json_obj["results"][0]):
            string=json_obj["results"][0]["searchMatches"][0]["startTime"]
            timestr = string
            timestr = timestr.split('.')[0]
            ftr = [3600,60,1]
            string=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
        else:
            string = 0
        print(string)
        conn.close()
        # except Exception as e:
        #     print("[Errno {0}] {1}".format(e.errno, e.strerror))
        # return render(request, 'video/video_detail.html', {'video': video})
        return render(request, 'scene.html', {'time':string,'video':m[0]})
        # return HttpResponse(json.dumps(json_obj), content_type="application/json")
        
    elif not transript:
        m = qs
        q = request.GET.get('q')
        if not q:
            print("1")
            return render(request, 'index.html',{'videos':Video.objects.all})
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': '8eec2a625b584342b4adde9c7ea87c6a',
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'query': q,
        })

        # try:
        conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
        conn.request("GET", "/Breakdowns/Api/Partner/Breakdowns/Search?%s" % params, "", headers)
        print("/Breakdowns/Api/Partner/Breakdowns/Search?%s" % params)
        response = conn.getresponse()
        string = response.read().decode('utf-8')
        json_obj=json.loads(string)
        print(json_obj)
        if (len(json_obj["results"])==1):
            if(json_obj["results"][0]):
                string=json_obj["results"][0]["searchMatches"][0]["startTime"]
                timestr = string
                timestr = timestr.split('.')[0]
                ftr = [3600,60,1]
                string=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                for vi in m:
                    print("6")
                    print(vi.embed)
                    print(json_obj["results"][0]["id"])
                    if(vi.embed==json_obj["results"][0]["id"]):
                        print("2")
                        return render(request, 'scene.html', {'time':string,'video':vi})
            print("3")
            return render(request, 'index.html',{'videos': Video.objects.all})
        else:
            if q:
                query = SearchQuery(q)
                vector = SearchVector('json','name')
                m = m.annotate(search=vector).filter(search=query)
                m = m.annotate(rank=SearchRank(vector, query)).order_by('-rank')
            print("5")
            return render(request, 'video/video_list.html',{'video_list':m})
        conn.close()
    else:
        movie=request.GET.get('movie')
        qs = Video.objects.all()
        face=request.GET.get('face')
        print(face)
        if movie:
            query = SearchQuery(movie)
            vector=SearchVector('name')
            qs = qs.annotate(search=vector).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')
            print(qs)
            m = qs[0]
            if m:
                print(m)
                string = m.json
                # print(string)
                json_obj=json.loads(string)
                for line in json_obj["breakdowns"][0]["insights"]["transcriptBlocks"]:
                    # print(line["lines"])
                    for z in line["lines"]:
                        text=z["text"]
                        if transript.lower() in text.lower():
                            print("xyz")
                            if face:
                                print(face)
                                for person in json_obj["breakdowns"][0]["insights"]["faces"]:
                                    print(person["name"])
                                    if person["name"].lower() in face.lower():
                                        timestr = line["lines"][0]["timeRange"]["start"]
                                        timestr = timestr.split('.')[0]
                                        ftr = [3600,60,1]
                                        string=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                                        return render(request, 'scene.html', {'time':string,'video':m})
                                return render(request,'video/video_list.html',{'video_list':Video.objects.all})
                            timestr = line["lines"][0]["timeRange"]["start"]
                            timestr = timestr.split('.')[0]
                            ftr = [3600,60,1]
                            string=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                            return render(request, 'scene.html', {'time':string,'video':m})
                else:
                    return render(request, 'video/video_detail.html',{'video':m})
            else:
                return render(request, 'video/video_detail.html',{'video':m})
        else:
            print(qs)
            for m in qs:
                print(m)
                string = m.json
                json_obj=json.loads(string)
                for line in json_obj["breakdowns"][0]["insights"]["transcriptBlocks"]:
                    print(line["lines"][0]["text"].lower())
                    for z in line["lines"]:
                        text=z["text"]
                        print(transript.lower())
                        if transript.lower() in text.lower():
                            print("xyz")
                            if face:
                                print(face)
                                for person in json_obj["breakdowns"][0]["insights"]["faces"]:
                                    print(person["name"])
                                    if person["name"].lower() in face.lower():
                                        timestr = line["lines"][0]["timeRange"]["start"]
                                        timestr = timestr.split('.')[0]
                                        ftr = [3600,60,1]
                                        string=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                                        return render(request, 'scene.html', {'time':string,'video':m})
                                return render(request,'video/video_list.html',{'video_list':Video.objects.all}) 
                            timestr = line["lines"][0]["timeRange"]["start"]
                            timestr = timestr.split('.')[0]
                            ftr = [3600,60,1]
                            string=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                            return render(request, 'scene.html', {'time':string,'video':m})
            return render(request,'video/video_list.html',{'video_list':Video.objects.all})     



class VideoListView(ListView):
    model = Video

def info(request,pk,time):
    video=Video.objects.get(id=pk)
    json_obj=video.json
    json_final=json.loads(json_obj)
    actor=[]
    for person in json_final["summarizedInsights"]["faces"]:
        for appearance in person["appearances"]:
            if int(appearance["startSeconds"])+1 <= int(time) and int(appearance["endSeconds"])-1 >= int(time):
                 print("xyz")
                 actor.append(person)
                 break
    return render(request, 'info.html',{'person_list':actor})

from urllib.request import urlretrieve
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def uploadvideo(request):
    link=request.POST["videoid"]
    url="https://keepvid.com/?url=https://www.youtube.com/watch?v="+link
    print(url)
    binary = FirefoxBinary('./geckodriver')
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(url)
    time.sleep(7)
    html = driver.page_source
    soup  = BeautifulSoup(html,'lxml')
    for a in soup.find_all('a', href=True):
        if len(a["href"])>100:
            headers = {
                # Request headers
                'Content-Type': 'multipart/form-data',
                'Ocp-Apim-Subscription-Key': '8eec2a625b584342b4adde9c7ea87c6a',
            }
            params = urllib.parse.urlencode({
                # Request parameters
                'name': (a["href"].split('='))[-1],
                'privacy': 'Public',
                'videoUrl': a['href'],
            })
            # try:
            conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
            conn.request("POST", "/Breakdowns/Api/Partner/Breakdowns?%s" % params, "", headers)
            response = conn.getresponse()
            string = response.read().decode('utf-8')
            json_obj = json.loads(string)
            new_video = Video.objects.create(name=(a["href"].split('='))[-1],embed=json_obj,user=request.user)
            new_video.save()
            # print(response.content)
            conn.close()
            break
    driver.quit()