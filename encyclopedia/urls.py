from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>/', views.load_page, name='page'),
    path('random/', views.random_page, name='random'),
    path('wiki/<str:title>/edit', views.edit, name='edit'),
    path('new/', views.new_page, name='new'),
    path('search/', views.search, name='search'),
]
