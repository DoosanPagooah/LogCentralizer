from django.urls import path
from .views import ReceiveLogView, log_dashboard, finops_dashboard # Add finops_dashboard here
from . import views

urlpatterns = [
path('home/', views.home_page, name='home'), # Add this
    path('receive/', ReceiveLogView.as_view(), name='receive_log'),
    path('insights/', log_dashboard, name='log_insights'),
    path('finops/', finops_dashboard, name='finops_dashboard'), # Remove the "views." prefix
]