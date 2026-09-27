from django.urls import include, path
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from api.v1.views.user_view import (
    UserViewSet, 
    VerifyConfirmationCodeView, 
    ResendConfirmationCodeView,
    UserPhotoViewSet,
)
from api.v1.views.stego_view import EmbedTextView, ExtractTextView

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API from ...",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)




urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("auth/", include('djoser.urls')),
    path("auth/", include('djoser.urls.authtoken')),
    # Подтверждение email
    path('auth/verify-code/', VerifyConfirmationCodeView.as_view(), name='verify-code'),
    path('auth/resend-code/', ResendConfirmationCodeView.as_view(), name='resend-code'),
    path('stego/embed/', EmbedTextView.as_view()),
    path('stego/extract/', ExtractTextView.as_view()),
    
]


v1_router = DefaultRouter()

v1_router.register('users', UserViewSet, basename='users')
v1_router.register('photos', UserPhotoViewSet, basename='photo')



urlpatterns +=  v1_router.urls