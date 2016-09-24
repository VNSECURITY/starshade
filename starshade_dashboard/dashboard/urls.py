"""frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns

# from django.contrib import admin
from dashboard import settings

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'starshade.views.home'),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^virtual-fixes$', 'starshade.views.virtual_fix_list', name='virtual_fix_list'),
    url(r'^threads$', 'starshade.views.threads', name=''),
    url(r'^virtual-fixes/get$', 'starshade.views.virtual_fix_public', name='virtual_fix_public'),
    url(r'^virtual-fix/new$', 'starshade.views.virtual_fix_new', name='virtual_fix_new'),
    url(r'^virtual-fix/(?P<id>[0-9a-zA-Z_-]+)/edit', 'starshade.views.virtual_fix_edit', name='virtual_fix_edit'),
    url(r'^virtual-fix/(?P<id>[0-9a-zA-Z_-]+)/remove', 'starshade.views.virtual_fix_remove', name='virtual_fix_remove'),

    url(r'^ajax/latest_data$', 'starshade.datasource.latest_data'),

]

urlpatterns += patterns('',
                        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})
                    )
