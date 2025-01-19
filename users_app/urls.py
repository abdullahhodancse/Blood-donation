from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .import views
router=DefaultRouter()
router.register('users_app',views.donerViewSet)
router.register('Blood_Group',views.Blood_Group_ViewSet)
router.register('blood-requests', views.BloodRequestViewSet)
router.register('blood-requestsaccept', views.request_accept_ViewSet)



urlpatterns=[
    path('',include(router.urls)),
    path('register/',views.UserRegistrationApiView.as_view(),name='register'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogOutView.as_view(),name='logout'),
    
    path('active/<uid64>/<token>',views.activate,name='activate'),
]