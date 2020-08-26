from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api import views

router = DefaultRouter()

router.register('profile', views.ProfileModelViewSet, basename='profile')

schema_view = get_schema_view(
   openapi.Info(
         title="Snippets API",
         default_version='v1',
         description="Learn about all the endpoints and their required parameters",
         contact=openapi.Contact(email="sahiil@protonmail.com"),
         license=openapi.License(name="BSD License"),
    ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('register-user', views.RegisterUser.as_view(), name='register-user'),
    path('login', ObtainAuthToken.as_view(), name='login-using-token'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('update-user-profile/<int:pk>', views.UpdateUserProfile.as_view(), name='update-user-profile'),
    path('list-users', views.ListUsers.as_view(), name='list-users'),
    path('user-details/<int:pk>', views.GetUserDetail.as_view(), name='user-details'),
    path('add-friend', views.AddFriend.as_view(), name='add-friend'),
    path('remove-friend', views.RemoveFriend.as_view(), name='remove-friend'),

    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += router.urls
