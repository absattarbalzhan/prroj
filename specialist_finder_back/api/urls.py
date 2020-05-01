from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register),
    path('login/', obtain_jwt_token),
    path('categories/', category_list, name='all specialists'),
    path('categories/<int:category_id>/', category_detail, name='get one specialist'),
    path('categories/<int:category_id>/specialists/', SpecialistByCategoryAPIView.as_view(), name='specialists by categories'),
    path('specialists/', SpecialistListAPIView.as_view(), name='all specialists'),
    path('specialists/<int:specialist_id>/', SpecialistDetailAPIView.as_view(), name='one specialist'),
    path('specialists/<int:specialist_id>/comments/', CommentsBySpecialistAPIView.as_view(), name='comments by specialist'),
    path('specialists/<int:specialist_id>/follow/', FollowSpecialistAPIView.as_view(), name='follow specialist'),
    path('specialists/<int:specialist_id>/like/', LikeSpecialistAPIView.as_view(), name='like specialist'),
    path('specialists/top_ten/', TopTenSpecialistsAPIView.as_view(), name='top ten'),
    path('specialists/search/', SpecialistSearchAPIView.as_view(), name="search_results")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

     #to make search in postman write following query '/?search=specialist_name