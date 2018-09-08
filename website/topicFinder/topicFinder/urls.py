"""topicFinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from bookDisplayer import views


urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^index.html$' , views.index, name = 'index'),
    url(r'^descript-books.html$' , views.descript_books , name='descript_books'),
    url(r'^descript-topics.html$',views.descript_topics, name='descript_topics'),

    url(r'^toc-books.html/$' ,views.toc_books, name ='toc_books'),
    url(r'^toc-topics.html/$',views.toc_topics, name='toc_topics'),
    
    url(r'^classes.html$', views.classes, name = "classes"),
    url(r'^about.html$', views.about, name = "about"),

    url(r'^toc-about.html$' , views.toc_about , name = "toc_about"),
    url(r'^descript-about.html$' , views.descript_about , name = "descript_about"),
    url(r'^classes-about.html$' , views.classes_about , name = "classes_about"),
    url(r'^job-about.html$' , views.job_about , name = "job_about"),
    url(r'^job-search.html$' , views.job_search , name = "job_search"),
    url(r'^tree-node.html$' , views.tree_node , name = "tree_node"),
    url(r'^circle-packer.html$' , views.circle_packer , name = "circle_packer"),
    url(r'^api/json-circle.html/(?P<department>\w+)$' , views.load_json , name = 'load_json'),
    url(r'^api/json-node.html/(?P<department>\w+)$' , views.load_json_treenode , name = 'load_json_treenode'),

    url(r'^class-detail/(?P<class_id>\d+)/$' , views.class_detail , name ='class_detail'),
    url(r'^book-detail/(?P<book_id>\d+)/$' , views.book_detail , name = 'book_detail'),
    url(r'^job-detail/(?P<job_id>\d+)/$' , views.job_detail , name ='job_detail'),
    url(r'^toc-topic-detail/(?P<topic_id>\d+)$' , views.toc_topic_detail , name='toc_topic_detail'),
    url(r'^descript-topic-detail/(?P<topic_id>\d+)$' , views.descript_topic_detail , name = 'descript_topic_detail'),

    url(r'^toc-freq.html$' , views.toc_freq , name = "toc_freq"),
    url(r'^search/(?P<course>\w+\s\w+)$',views.search , name='search'),
    url(r'^search/(?P<course>\w+)/$' , views.search , name = 'search')

]


urlpatterns+=staticfiles_urlpatterns()
