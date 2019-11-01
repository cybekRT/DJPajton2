from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^view/(?P<pk>[0-9]+)', views.ArticleDetailView.as_view(), name = "detail"),
    #url(r'', views.ArticleIndexView.as_view(), name = "index"),
    url(r'login', views.Login.as_view()),
    url(r'logout', views.Logout.as_view()),
    url(r'register', views.Register.as_view()),
    url(r'token/(.+)', views.Token.as_view()),
    url(r'', views.Panel),
]
