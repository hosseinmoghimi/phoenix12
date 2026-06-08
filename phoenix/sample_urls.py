from django.contrib import admin
from django.urls import path,include,re_path
from django.views.static import serve
from phoenix.server_settings import QRCODE_ROOT,STATIC_ROOT,MEDIA_ROOT
from authentication.views import LoginView
from market.views import IndexView
from phoenix.settings import COMING_SOON
if COMING_SOON:
    from core.views import ComingSoonView
    urlpatterns=[
        path('', ComingSoonView.as_view(),name=''),
        path('authentication/', include('authentication.urls')),
        path('utility/', include('utility.urls')),
        path('accounts/login/', LoginView.as_view(),name='login'),
        path('core/', include('core.urls')),

        path('admin/', admin.site.urls),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    ]
else:
        
    urlpatterns = [ 
        path('', IndexView.as_view(),name='home'),
        path('admin/', admin.site.urls),
        path('utility/', include('utility.urls')),
        path('authentication/', include('authentication.urls')),
        path('core/', include('core.urls')),
        path('log/', include('log.urls')),
        path('attachments/', include('attachments.urls')),
        path('blog/', include('blog.urls')),
        path('messenger/', include('messenger.urls')),
        path('accounts/login/', LoginView.as_view(),name='login'),
        path('accounting/', include('accounting.urls')),
        path('organization/', include('organization.urls')),
        path('projectmanager/', include('projectmanager.urls')),
        path('warehouse/', include('warehouse.urls')),
        path('market/', include('market.urls')),
        path('cafe/', include('cafe.urls')),
        path('bms/', include('bms.urls')),
        

        re_path(r'^qrcode/(?P<path>.*)$', serve, {'document_root': QRCODE_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),


    ]
