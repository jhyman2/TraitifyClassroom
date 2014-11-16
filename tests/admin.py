from django.contrib import admin
from models import Student
from django.contrib.admin import AdminSite


class StudentAdmin(admin.ModelAdmin):
	fields = ['first', 'last', 'test_id', 'finished_test']

admin.site.register(Student)

class MyAdminSite(AdminSite):
    site_header = 'Monty Python administration'

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Student)