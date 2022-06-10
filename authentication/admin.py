from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Bus, UserDetail, Book, Profile


# Register your models here.
admin.site.site_header = "Yatayat Management System Admin"
admin.site.index_title  =  "Yatayat Management System - ADMIN"

admin.site.unregister(Group)

admin.site.register(Bus)
admin.site.register(UserDetail)
admin.site.register(Book)
admin.site.register(Profile)


