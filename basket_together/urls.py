from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', 'basket_together.views.index', name='index'),
    # url(r'^$', 'recruit.views.post_list', name='index'),
    url(r'^recruit/', include('recruit.urls')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    # url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)