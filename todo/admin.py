from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    readonly_fileds=('created',)

admin.site.register(Todo, TodoAdmin)





