from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from models import Student
from forms import StudentForm
from traitify import Traitify
from django.template import RequestContext, loader
import string
import random

public_key = 'sq1ekdq2849c1778327k1cfqho'
secret_key = 'cdpfn6kmpktklsmtttjerd7fg1'

def get_assessment():
	traitify = Traitify(secret_key)
	# Get the decks
	decks = traitify.get_decks()
	# Set deck id
	traitify.deck_id = decks[0].id
	# Create an assessment
	assessment = traitify.create_assessment()
	return assessment.id

def log(request):
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			stu = form.save()
			test_id = get_assessment()
			print test_id
			stu.test_id = test_id
			stu.save()
			request.session['stu_id'] = stu.id
			request.session['test_id'] = test_id
			return HttpResponseRedirect('/tests/assess/')
	else:
		form = StudentForm()
	#template = loader.get_template('studentlogin.html')
	return render(request, 'studentlogin.html', {'form': form})
	
def testDetail(request):
	session_id = request.session['test_id']
	return render(request, 'studentquiz.html', {'test_id': session_id})
	
def testResult(request):
	cur_stu = get_object_or_404(Student, pk=request.session['stu_id'])
	cur_stu.finished_test = True
	cur_stu.save()
	return render(request, 'tests/assess_confirm.html', {})
	
def generate(request, user_count):
	traitify = Traitify(secret_key)
	decks = traitify.get_decks()
	traitify.deck_id = decks[0].id
	for i in range(user_count):
		cur_id = traitify.create_assessment().id
		first_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
		last_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
		my_stu = Student.objects.create_student(first=first_name,last=last_name,test_id=cur_id)
		slides = traitify.get_slides(cur_id)
		for slide in slides:
			slide.response = random.choice([True, False])
			slide.time_taken = 200
		slides = traitify.update_slides(cur_id, slides)
		my_stu.finished_test = True
		my_stu.save()
	return render(request, 'random_gen.html', {'count': user_count})

	
