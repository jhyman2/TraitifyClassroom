from django.contrib import admin
from models import Student

class StudentAdmin(admin.ModelAdmin):
	fields = ['first', 'last', 'test_id', 'finished_test']

admin.site.register(Student)