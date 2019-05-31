from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

from home import models
from home.views import home, activate, signup, like, AuthView, detail_article, comment

from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', home, name='home'),
    path('comment_add/', comment,),
    path('logout/', LogoutView.as_view(next_page='/signup')),
    path('article/<str:pk>/', detail_article, name='detail_article'),
    path('auth/', AuthView.as_view(), name='signup'),
    path('signup/', signup, name='signup'),
    path('like_update/<str:pk>/', like, name='like'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         activate, name='activate'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
