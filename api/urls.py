from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('item/', views.ItemModelView.as_view(), name='item'),
    path('item/<int:pk>/', views.ItemModelDetailView.as_view(), name='item_detail'),
]