from django.urls import path
from . import views

app_name = 'book_store_app'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('sing_up/', views.sing_up_view, name='sing_up'),
    path('login/', views.login_view, name='login'),
    path('client_index/', views.client_index_view, name='client_index'),
    path('client_profile/', views.client_profile_view, name='client_profile'),
    path('client_purchases_history/', views.client_purchases_history_view, name='client_purchases_history'),
    path('logout/', views.logout_view, name='logout'),
]
