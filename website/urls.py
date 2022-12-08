from re import template
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='home'),
    path('profile', views.profile, name='profile'),
    path('profile/add_book/<int:pk>', views.add_book, name='add_book'),

    path('api/refresh_courses', views.refresh_courses, name='refresh_courses'),
    path('profile/choose_course', views.choose_course, name='choose_course'),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
    path('profiles/<int:pk>', views.profile_detail, name='profile_detail'),
    path('chat/<int:pk>', views.chat, name='chat'),
    path('courses/<int:pk>', views.course_detail, name='course_detail'),
    path('search', views.search, name='search'),

    # managing books
    path('books/<int:pk>/edit', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete', views.delete_book, name='delete_book'),
    path('books/<int:pk>', views.book_detail, name='book_detail'),

    # favoriting books
    path('books/<int:pk>/favorite', views.favorite_book, name='favorite_book'),
    path('books/<int:pk>/remove', views.remove_favorite, name='remove_favorite'),
    path('books/<int:pk>/remove1', views.remove_favorite1, name='remove_favorite1'),

    #friending users
    path('profiles/<int:pk>/send_friend_request', views.send_friend_request, name='send_friend_request'),
    path('profiles/<int:pk>/accept_friend_request', views.accept_friend_request, name='accept_friend_request'),
    path('profiles/<int:pk>/accept_friend_request1', views.accept_friend_request1, name='accept_friend_request1'),
    path('profiles/<int:pk>/remove_friend', views.remove_friend, name='remove_friend'),
    path('profiles/<int:pk>/remove_friend1', views.remove_friend1, name='remove_friend1'),
    path('profiles/<int:pk>/remove_request', views.remove_request, name='remove_request'),
    path('profiles/<int:pk>/remove_request1', views.remove_request1, name='remove_request1'),
    path('profiles/<int:pk>/reject_request', views.reject_request, name='reject_request'),
    path('profiles/<int:pk>/reject_request1', views.reject_request1, name='reject_request1'),
]