from django.conf.urls import url
from . import views

urlpatterns = [
	#url(r'^view/(?P<pk>[0-9]+)', views.ArticleDetailView.as_view(), name = "detail"),
	#url(r'', views.ArticleIndexView.as_view(), name = "index"),
	url(r'volume$', views.GetVolume),
	url(r'volume/([0-9]+)', views.SetVolume),
	url(r'time$', views.GetTime),
	url(r'time/([0-9]+)', views.SetTime),
	url(r'length', views.GetLength),
	url(r'start', views.Start),
	url(r'stop', views.Stop),
	url(r'next', views.Next),
	
	url(r'queue$', views.GetQueue),
	url(r'queue/([0-9 ]+)', views.Queue),
	
	url(r'add/(.+)', views.AddSong),
	
	url(r'status$', views.Status),
	url(r'playlist$', views.Playlist),
	url(r'playlist/all', views.PlaylistTotal),
	
	url(r'users', views.Users),
	
	url(r'logger$', views.LoggerRecent),
	url(r'logger/(\-{0,1}[0-9]+)', views.LoggerSince),
	url(r'logger/wait/(\-{0,1}[0-9]+)', views.LoggerWait),
	
	
	url(r'', views.Invalid)
]
