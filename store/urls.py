from django.urls import path
from . import views

urlpatterns = [
   path('', views.store, name='store'), # 메인 화면 보여줌
   path('<slug:category_slug>/', views.store, name='products_by_category'),
] 
