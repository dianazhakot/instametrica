from django.urls import path, include
from .views import home, postinfo, page_not_found

urlpatterns = [
    path('', home, name='home'),
    path('post-info', postinfo, name='post-info'),
    path('page-not-found', page_not_found, name='page-not-found')
]
