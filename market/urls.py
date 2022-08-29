"""djcaching URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from .views import start_page, contact_page  # to_product_profile, to_category, to_shop, to_inshop
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
import debug_toolbar
from django.views.static import serve as mediaserve


schema_view = get_schema_view(
    openapi.Info(
        title='ItemsApi',
        default_version='v1',
        description='Описание проекта',
        terms_of_service='https://www/google.com/policies/terms/',
        contact=openapi.Contact(email='admin.company@local'),
        license=openapi.License(name="")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('site_api.urls')),
    path('users/', include('app_users.urls')),
    path('shops/', include('app_shops.urls')),
    path('statistics/', include('add_statistics.urls')),
    path('', start_page, name='start_page'),
    # path('to_product/', to_product_profile, name='to_product'),
    # path('to_category/', to_category, name='to_category'),
    # path('to_shop/', to_shop, name='to_shop'),
    # path('to_inshop/', to_inshop, name='to_inshop'),
    path('contact', contact_page, name='contact'),
    path('i18n', include('django.conf.urls.i18n')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0,), name='schema_swagger_ui'),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += [
#    path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$', mediaserve, {'document_root': settings.MEDIA_ROOT}),
#    path(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$', mediaserve, {'document_root': settings.STATIC_ROOT}),
#]
