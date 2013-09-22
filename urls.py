from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^webapp/', TemplateView.as_view(template_name="index.html")),
)


from settings import DEBUG, MEDIA_URL, MEDIA_ROOT

if DEBUG:
    urlpatterns += patterns('', 
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'})
    )

    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
