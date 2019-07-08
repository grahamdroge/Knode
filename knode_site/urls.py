from django.urls import path
from . import views 


urlpatterns = [
	# ex: /knode_site/
	path('', views.login_user, name="login_user"),
	path('logout_user', views.logout_user, name="logout_user"),

	path('home', views.home, name="home"),
	path('signin', views.signin, name="signin"),
	path('signup', views.signup, name="signup"),
]