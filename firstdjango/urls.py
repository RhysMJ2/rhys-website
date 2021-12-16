"""firstdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
import myapi
from accounts import views as accounts_view
from boards import views
from firstdjango.sitemaps import StaticViewSitemap
sitemaps = {
    'static': StaticViewSitemap
}

urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('admin/', admin.site.urls, name='admin'), # For the admin dashboard
    path('boards/<int:pk>/', views.TopicListView.as_view(), name='board_topics'),
    path('boards/<int:pk>/new/', views.new_topic, name='new_topic'),
    path('boards/<int:pk>/topics/<int:topic_pk>/', views.PostListView.as_view(), name='topic_posts'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    path('boards/<pk>/topics/<topic_pk>/posts/<post_pk>/edit/',
         views.PostUpdateView.as_view(), name='edit_post'),
    path('api/', include(('myapi.urls', 'api'), namespace='api')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    path("account/", include(('firstdjango.accounts_urls', 'accounts_url'), namespace="accounts"))
]

handler404 = 'boards.views.error_404'
handler500 = 'boards.views.error_500'
# handler403 = 'boards.views.error_403'
# handler400 = 'boards.views.error_400'
