from django.core.serializers import json
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from datasource import get_data
from . import forms, models

import json


@login_required
def live_data():
    return JsonResponse(get_data(sort="@timestamp:desc"))
