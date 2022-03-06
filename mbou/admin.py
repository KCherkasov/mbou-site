from django.contrib import admin
from mbou import models

admin.site.register(models.Document)
admin.site.register(models.DocumentCategory)
admin.site.register(models.News)
admin.site.register(models.FoodTable)