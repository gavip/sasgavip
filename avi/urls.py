from django.conf.urls import include, patterns, url
from plugins.urls import job_list_urls
from avi import views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.index,
        name='index'),

    url(r'^run_query/$',
        views.run_query,
        name='run_query'),

    url(r'^result/(?P<job_id>[0-9]+)/$',
        views.job_result,
        name='job_result'),

    url(r'^job_list/',
        include(job_list_urls,
        namespace='job_list')),
)
