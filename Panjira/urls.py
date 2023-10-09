from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
import work, account


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='account/login/')),
    path('', include('work.urls')),
    path('account/', include('account.urls')),
]
