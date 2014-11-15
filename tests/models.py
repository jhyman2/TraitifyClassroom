from django.db import models

class StudentManager(models.Manager):
	def create_student(self, first, last, test_id):
		stu = self.create(first=first, last=last, test_id=test_id)
		return stu

class Student(models.Model):
	first = models.CharField(max_length=100)
	last = models.CharField(max_length=100)
	test_id = models.CharField(max_length=256)
	finished_test = models.BooleanField(default=False)
	
	objects=StudentManager()
	
	def __unicode__(self):
		return (self.first + ' ' + self.last)
