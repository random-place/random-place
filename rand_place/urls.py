from django.contrib import admin
from django.urls import path
import rand_place_app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', rand_place_app.views.index, name="index"),
    path('random/', rand_place_app.views.random, name="random"),
]
