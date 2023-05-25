
from django.contrib import admin
from django.urls import path, include
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings

static_urlpatterns = [
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT, "show_indexes": True}),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.Scanner.urls')),
    path('accounts/', include('django.contrib.auth.urls'), name="accounts"),
    path('accounts/', include('website.Account.urls')),
    path("", include(static_urlpatterns)),
]
