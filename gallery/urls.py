from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing_page, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='gallery/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('books/', views.book_feed, name='book_feed'),
    path('books/<int:book_id>/request/', views.request_purchase, name='request_purchase'),
    path('orders/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),
    path('purchases/', views.purchase_history, name='purchase_history'),
]