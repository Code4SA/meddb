from django.conf.urls import patterns, include, url

urlpatterns = patterns('reports.views',
    #url(r'^reference_report/$', 'reference_report', name='reference_report'),
    url(r'^price_grid/$', 'medicine_grid', name='medicine_grid'),
)

