"""backend_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


schema_view = get_schema_view(
    openapi.Info(
        title='Smart Waste Segregator and Route Planner API',
        default_version='v1',
    ),
    public=True,
    # permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/route-planner/', include('route_planner.urls')),
    path('api/recognition/', include('recognition.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

admin.site.site_header = "Smart Waste Segregation and Route Planner Admin Page"
admin.site.site_title = "Admin's Portal"
admin.site.site_header = "Smart WSARP's Admin Portal"