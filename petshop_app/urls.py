from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('additem/', AddItem.as_view(), name='add_item'),
    path('item/<int:item_id>/', show_item, name='item'),
    path('category/<int:category_id>/', show_category, name='category'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('shopping_cart/', show_shopping_cart, name='shopping_cart'),
    path('add_item_to_shopping_cart/', add_item_to_shopping_cart, name='add_item_to_shopping_cart'),
]