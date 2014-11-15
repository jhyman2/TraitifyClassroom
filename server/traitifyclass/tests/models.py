from django.db import models

class Student(models.Model):
	first = models.CharField(max_length=100)
	last = models.CharField(max_length=100)
	test_id = models.CharField(max_length=256,unique=True)
	finished_test = models.BooleanField(default=False)
