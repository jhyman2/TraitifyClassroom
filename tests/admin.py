from django.contrib import admin
from models import Student

class StudentAdmin(admin.ModelAdmin):
	fields = ('first', 'last', 'finished_test')
	list_display = ('first', 'last')

admin.site.register(Student)
