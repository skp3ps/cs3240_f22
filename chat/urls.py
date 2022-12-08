from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_rooms, name="all_rooms"),
    path('token', views.token, name='token'),
    path('rooms/<slug>', views.room_detail, name="room_detail"),
]