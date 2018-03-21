from django.conf.urls import url, include
from dashboard import views

urlpatterns = [
    url(r'^$',views.top, name='dashboard_top'),
]
