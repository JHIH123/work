from django.contrib import admin
from .models import Place, Photo

# Register your models here.

admin.site.register(Photo,admin.ModelAdmin)
admin.site.register(Place,admin.ModelAdmin)