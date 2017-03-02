from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^process$', views.process, name='process'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^addquote$', views.addquote),
    url(r'^listquotes/(?P<id>\d+)$', views.listquotes),
    url(r'^addfavorite/(?P<qid>\d+)$', views.addfavorite),
    url(r'^removequote/(?P<id>\d+)$', views.removequote),

    # url(r'^.+$', views.any, name='any')

]
