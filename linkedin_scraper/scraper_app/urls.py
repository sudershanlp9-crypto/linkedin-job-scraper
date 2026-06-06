from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.index,         name='index'),
    path('scrape/',                       views.scrape,        name='scrape'),
    path('status/<str:job_id>/',          views.scrape_status, name='status'),
    path('download/<str:filename>/',      views.download_report, name='download'),
]
