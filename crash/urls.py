from django.conf.urls import patterns, include, url
from django.contrib import admin
from simple_sso.sso_client.client import Client
from django.conf import settings

sso_client = Client(server_url=settings.SSO_SERVER_URL,
	                public_key=settings.SSO_PUBLIC_KEY,
	                private_key=settings.SSO_PRIVATE_KEY)

urlpatterns = patterns('',
    url(r'^sso/', include(sso_client.get_urls())),
    url(r'^login/$', 'crash.views.login', name='login'),
    url(r'^logout/$', 'crash.views.logout', name='logout'),

    url(r'report/android/', 'reporting.views.report_android', name='report-android'),
    url(r'acra/_design/acra-storage/_update/report/', 'reporting.views.report_android', name='report-android-legacy'),

    url(r'^$', 'reporting.views.index'),
    url(r'^reports/android/(?P<package>.*)/(?P<id>.*)/$', 'reporting.views.report'),
    url(r'^reports/android/(?P<package>.*)/$', 'reporting.views.package'),
    url(r'^admin/', include(admin.site.urls)),
)
