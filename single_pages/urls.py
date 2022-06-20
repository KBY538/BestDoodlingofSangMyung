from django.urls import path, include

from . import views # .을 찍는 게 blog라고 적는 것보다 에러가 덜 난다.

urlpatterns = [
    path('about_it/', views.about_it), # about me 페이지
    path('time_table/', views.time_table), # time table 페이지
    path('', views.landing), # 메인페이지
]
