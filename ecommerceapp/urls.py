from django.urls import path
from ecommerceapp import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('profile/', views.profile, name="profile"),
    path('checkout/', views.checkout, name="checkout"),
    path('handlerequest/', views.handlerequest, name="handlerequest"),
    path('place_order/', views.place_order, name="place_order"),  # Add this line for the place_order view
]
