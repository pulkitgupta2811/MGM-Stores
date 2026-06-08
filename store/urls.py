from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home with login/register form
    path('', views.home, name='home'),
    path('register/', views.user_register, name='register'),

    # Categories and Products
    path('categories/', views.categories, name='categories'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),

    # Cart operations
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Authentication
    path('logout/', views.user_logout, name='logout'),

    # User profile
    path('profile/', views.user_profile, name='profile'),

    # Password Reset via Email
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]
