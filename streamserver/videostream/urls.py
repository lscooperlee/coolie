from django.conf.urls import patterns, url

urlpatterns=patterns('',
    url("^$",'videostream.views.index'),
    url("^get_image$",'videostream.views.get_image'),
    url("^key$",'videostream.views.key_handler'),
)
