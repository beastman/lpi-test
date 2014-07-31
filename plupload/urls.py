from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^upload/$', 'plupload.views.plupload_handler', name='plupload_upload_handler'),
    url(r'^admin-preview/image/$', 'plupload.views.admin_image_preview', name='plupload_admin_image_preview'),
)