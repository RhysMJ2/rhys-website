from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from . import views

testRouter = routers.DefaultRouter()
testRouter.register(r'heroes', views.HeroViewSet)
boardsRouter = routers.DefaultRouter()
boardsRouter.register(r'board', views.BoardViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.TestAPI.as_view(), name='home'), # todo remove and change button access api
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), todo remove
    path('api-auth/', include(('firstdjango.accounts_urls', 'account'), namespace='rest_framework')),
    # path('test/', include((testRouter.urls, 'api'), namespace='api')), todo remove
    path('boards/', include((boardsRouter.urls, 'board'), namespace='board'))
]
