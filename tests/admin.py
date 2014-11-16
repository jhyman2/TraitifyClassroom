from django.contrib import admin
from models import Student

admin.site.register(Student)

class StudentAdmin(admin.ModelAdmin):
	fields = ['first', 'last', 'finished_test']
	list_display = ('first', 'last')


