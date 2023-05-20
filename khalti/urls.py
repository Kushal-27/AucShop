from django.urls import path
from khalti import views

urlpatterns = [
    path('verify', views.verify, name='verify'),
    path('config', views.config, name='config'),
    # other URL patterns here
]