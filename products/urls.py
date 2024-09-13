from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view()),
    path('', views.ProductListCreateAPIView.as_view()),
]
