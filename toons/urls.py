from django.urls import path

from . import views

urlpatterns = [
    path('<str:slug>/<int:episode>/add_comment/', views.add_comment),
    path('upload_work/', views.WorkCreate.as_view()),
    path('<str:slug>/upload_toon/', views.toon_create),
    path('<str:slug>/<int:episode>/update_toon/', views.toon_update),
    path('category/<str:slug>/', views.show_toon_category),
    path('<str:slug>/<int:episode>/', views.show_toon_episode),
    path('<str:slug>/', views.show_toon_episodes),
    path('', views.WorkList.as_view()),
]