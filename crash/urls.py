from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crash.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'report/android/', 'reporting.views.report_android', name='report-android'),
    url(r'acra/_design/acra-storage/_update/report/', 'reporting.views.report_android', name='report-android-legacy'),

    url(r'^admin/', include(admin.site.urls)),
)
