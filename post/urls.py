from django.urls import path,include
from .import views

urlpatterns = [
    path('like/<int:id>/<int:user_id>/',views.likeview,name='like'),
    path('dislike/<int:id>/<int:user_id>/',views.dislikeview,name='dislike'),
    path('dashboard/',views.dashboardview,name='dashboard'),
    path('user_post/<int:user_id>/',views.user_post,name='userPost'),
    path('add_post/',views.addpostview,name='addPost'),
    path('detailview/<int:pk>/', views.DetailViewOfPost.as_view(), name='detailview'),
]
