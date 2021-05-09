"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_control
from django.contrib.staticfiles.views import serve
from product.views import (search_products,
                           product_page,
                           brand_page,
                           compare_page,
                           del_category,
                           seller_products,
                           )

from shop.views import (start_page,
                        promotion_page,
                        connect_contact,
                        login_contact,
                        test_mail)
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search_products/', search_products, name='search_products_page'),
    path('', start_page, name='start_page'),
    path('', include('accounts.urls')),
    path('', include('product.urls')),
    path('api/', include('api.urls')),
    path('support/', include('support.urls')),
    path('product/<int:pid>/', product_page, name='product_page'),
    path('brand/<int:brand_id>', brand_page, name='brand_page'),
    path('compare/<str:cid>', compare_page, name='compare_page'),
    path('del_category/', del_category, name='del_category'),
    path('seller_products/', seller_products, name='seller_products'),
    path('promo/<int:promo_id>', promotion_page, name='promotion_page'),
    path('getapi/', connect_contact, name='coco'),
    path('login_contact/', login_contact, name='login_contact_page'),
    path('test_mail/', test_mail)
]
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      view=cache_control(no_cache=True, must_revalidate=True)(serve))
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
