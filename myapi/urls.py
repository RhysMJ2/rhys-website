from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'heroes', views.HeroViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.TestAPI.as_view(), name='home'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth/', include(('firstdjango.accounts_urls', 'account'), namespace='rest_framework')),
    path('test/', include((router.urls, 'api'), namespace='api')),
]
