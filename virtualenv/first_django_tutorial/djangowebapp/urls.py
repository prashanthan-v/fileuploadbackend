from django.urls import path
from . import views

urlpatterns = [
    path('greetings/', views.greetings, name='greetingsname'),
    path('attendance/<int:status>/', views.stat, name='status'),
    path('create/',views.create,name ='create'),
    path('read/',views.read,name ='read'),
    path('update/',views.update,name ='update'),
    path('delete/',views.delete,name ='delete'),
]