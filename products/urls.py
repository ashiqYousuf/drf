from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(),
         name='product-detail'),
    path('', views.ProductListCreateAPIView.as_view()),
    # path('', views.ProductMixinView.as_view()),
    # path('<int:pk>/', views.ProductMixinView.as_view()),
]
