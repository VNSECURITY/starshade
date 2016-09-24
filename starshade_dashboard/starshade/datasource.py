import time
from django.core.serializers import json
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from . import forms, models

import json

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

es = Elasticsearch(["52.221.240.46"])

use_mock = True

def current_data():
    s = Search(using=es)
    s.query('range', **{'@timestamp': {'gte': time.time()*1000 - 30*60}})
    s.sort({"@timestamp" : {"order" : "desc"}})
    return s.execute()

def threads():
    s = Search(using=es)
    s.filter('match', score='select')
    s.sort({"@timestamp" : {"order" : "desc"}})
    return s.execute()

@login_required
def latest_data(request):
    if use_mock:
        now = time.time()
        hist = []
        for i in range(-5*60,0,1):
            t = int(now + i)
            hist.append((t,((t*.3)**2)%20,(((t*9999)%9898)**2)%100))
        obj = {
            "request_histogram": hist
        }
        return JsonResponse(obj)
    else:
        s = Search(using=es)
        time_range = {
            'min': time.time() * 1000 - 30 * 60,
            'max': time.time() * 1000
        }
        s.query('range',**{'@timestamp':{'gte':time_range['min']}})
        s.aggs.bucket('request_histogram', 'date_histogram', field='@timestamp', interval='3s',
                      extended_bounds=time_range
                      )
        return JsonResponse(s.execute().to_dict(), safe=False)
