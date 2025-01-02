from django.urls import path
from . import views  # Import your views module correctly

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('bmi/', views.calculate_bmi, name='calculate_bmi'),
]
