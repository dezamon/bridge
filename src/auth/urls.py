from django.conf.urls import url, include
from auth import views

urlpatterns = [
    url(r'^create-designer/$',views.create_designer_account, name='create_designer_account'),
    url(r'^login/$',views.login_account, name='login_account'),
    url(r'^logout/$',views.logout_account, name='logout_account'),
    url(r'^reset/(?P<key>[0-9A-Za-z\-]+)/$',views.reset_password, name='reset_password'),
    url(r'^reset-request/$',views.reset_password_request, name='reset_password_request'),
]
