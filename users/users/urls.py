from django.conf.urls import url
from usermanage import views


urlpatterns = [
    url(r'^login/$', views.user_login, name='user-login'),
    url(r'^user/$', views.UserView.as_view(), name='user-create'),
    url(r'^dashboard/$', views.UserDashboardView.as_view(), name='user-dashboard'),
    url(r'^logout/$', views.LogoutView.as_view(), name='user-logout'),
]
