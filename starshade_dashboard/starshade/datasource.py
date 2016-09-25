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

es = Elasticsearch(["52.77.212.201"])

use_mock = False


def current_data():
    s = Search(using=es)
    s = s.query('range', **{
        '@timestamp': {
            'gte': int(time.time()*1000 - 30*60*1000)
        }
    })
    s = s.query('exists', field='clientip')
    s = s.sort({
        "@timestamp": {"order": "desc", "unmapped_type": "boolean"}
    })
    response = s.execute()
    result = []
    for obj in response.to_dict().get('hits',{}).get('hits',[]):
        obj.update(obj.get('_source',{}))
        del obj['_source']
        print obj
        result.append(obj)
    print result
    return result


def threads():
    s = Search(using=es)
    s = s.filter('range', response={'gte': 400, 'lt': 600})
    s = s.sort({"@timestamp": {"order": "desc"}})
    return s.execute()


def blocked_data():
    s = Search(using=es)
    s = s.filter('match', response='403')
    s = s.sort({"@timestamp": {"order": "desc"}})
    return s.execute()


@login_required
def threads_tree(request):
    response = threads().to_dict()

    result = {
        "name": '/',
    }
    for record in response.get('hits', {}).get('hits', []):
        root = result
        record = record.get('_source')
        if record.get('request', False):
            for part in record.get('request', '').split("/")[:6]:
                if not ("children" in root):
                    root["children"] = []
                child = None
                for c in root['children']:
                    if c['name'] == part:
                        child = c
                if child is None:
                    name = part
                    if len(name) > 10:
                        name = name[:7] + "..."
                    child = {
                        "name": name,
                    }
                    root['children'].append(child)
                root = child
    return JsonResponse(result)


realtime_span = 10 * 60 * 1000
realtime_split = 10 * 1000


def get_request_histogram():
    s = Search(using=es)
    time_range = {
        'min': int(time.time() * 1000 - realtime_span),
        'max': int(time.time() * 1000)
    }

    s = s.query('range', **{
        '@timestamp': {
            'gte': time_range['min'],
            # 'time_zone': '+0000',
        }})
    s.aggs.bucket('request_histogram', 'date_histogram',
                  field='@timestamp',
                  # time_zone='+0000',
                  min_doc_count=0,
                  interval='%dms' % (realtime_split),
                  extended_bounds=time_range
                  )

    response = s.execute()
    hist = []
    print response.to_dict()
    for bucket in response.aggregations.request_histogram.buckets:
        hist.append((bucket['key'], bucket['doc_count']))
    return hist


def get_threads_histogram():
    s = Search(using=es)
    time_range = {
        'min': int(time.time() * 1000 - realtime_span),
        'max': int(time.time() * 1000)
    }

    s = s.query('range', **{
        '@timestamp': {
            'gte': time_range['min'],
            # 'time_zone': '+0000',
        }}).filter('range', response={'gte': 400, 'lt': 600})

    s.aggs.bucket('thread_histogram', 'date_histogram',
                  field='@timestamp',
                  # time_zone='+0000',
                  min_doc_count=0,
                  interval='%dms' % (realtime_split),
                  extended_bounds=time_range
                  )

    response = s.execute()
    hist = []
    print response.to_dict()
    for bucket in response.aggregations.thread_histogram.buckets:
        hist.append((bucket['key'], bucket['doc_count']))
    return hist


@login_required
def latest_data(request):
    if use_mock:
        now = time.time()
        hist = []
        for i in range(-5 * 60, 0, 1):
            t = int(now + i)
            hist.append((t, ((t * .3) ** 2) % 20, (((t * 9999) % 9898) ** 2) % 100))
        obj = {
            "request_histogram": hist
        }
        return JsonResponse(obj)
    else:
        obj = {
            "request_histogram": get_request_histogram(),
            "threads_histogram": get_threads_histogram(),
            "barwidth": realtime_split * .7,
        }
        return JsonResponse(obj, safe=False)
