from django.contrib import admin
from models import Student
from django.contrib.admin import AdminSite, ModelAdmin

class StudentAdmin(ModelAdmin):
	fields = ['first', 'last', 'test_id', 'finished_test']

class MyAdminSite(AdminSite):
    site_header = 'Traitify Teacher Login'

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Student, StudentAdmin)

