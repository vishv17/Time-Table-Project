"""time_table_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.views.generic import TemplateView
from django import template
from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$',TemplateView.as_view(template_name="timetable/index.html"),name="first_page"),
    url(r'^subject/$',views.Subject.as_view(),name="subject_page"),
    url(r'^faculty/$',views.Faculty.as_view(),name="subject_page"),
    url(r'^timetable/$',views.timetable,name="timetable_page"),
    url(r'^dashboard/$',views.dashboard,name="dashboard_page"),
    url(r'^dashboard/fetch_data/$',views.before_timetable_subject),
    url(r'^dashboard/add_semester$',views.add_semester,name="add_semester"),
    url(r'^timetable/get_timetable$',views.timetable_generation,name="get_timetable"),

    #url(r'^timetable/$',views.Timetable.as_view(),name="timetable_page"),
]
