from django.contrib import admin
from django.urls import path, include

from core.gym.urls import router


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
