from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductListCreateAPIView.as_view(), name="product-list"),
    path("<int:pk>/", views.ProductDetailAPIView.as_view(), name="product-detail"),
    path("<int:pk>/update/", views.ProductAPIUpdateView.as_view()),
    path("<int:pk>/delete/", views.ProductAPIDeleteView.as_view()),
]
