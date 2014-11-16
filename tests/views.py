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

def aggregrate_data():
	#complete_students = Student.obects.filter(finished_test=True)
	#for stu in complete_students:
	#	# Get an assessment's results (personality types)
	#personality_types = traitify.get_personality_types(assessment.id)
	# Get an assessment's results (personality type traits)
	#personality_type = personality_types["personality_types"][0]["personality_type"]
	#main_trait = personality_type.name
	#add main_trait to list
	pass

def generate_png():
	#import matplotlib
	#matplotlib.use('Agg')
	#import matplotlib.pyplot as plt
	#labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
	#sizes = [15, 30, 45, 10]
	#colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
	#plt.pie(sizes, explode=explode, labels=labels, colors=colors,
     #   autopct='%1.1f%%', shadow=True, startangle=90)
	# Set aspect ratio to be equal so that pie is drawn as a circle.
	#plt.axis('equal')
	#plt.savefig('mypng.png')
	pass

def log(request):
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			stu = form.save()
			test_id = get_assessment()
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
	if request.method == 'POST':
		cur_stu = get_object_or_404(Student, pk=request.session['stu_id'])
		cur_stu.finished_test = True
		cur_stu.save()
		return HttpResponse('')
		#alternatively, just do the same thing
	else:
		return render(request, 'studentquiz.html', {'test_id': session_id})
	
def generate(request, user_count):
	traitify = Traitify(secret_key)
	decks = traitify.get_decks()
	traitify.deck_id = decks[0].id
	for i in range(int(user_count)):
		cur_id = traitify.create_assessment().id
		first_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
		last_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
		my_stu = Student.objects.create_student(first=first_name,last=last_name,test_id=cur_id)
		print my_stu.pk
		slides = traitify.get_slides(cur_id)
		for slide in slides:
			slide.response = random.choice([True, False])
			slide.time_taken = 200
		slides = traitify.update_slides(cur_id, slides)
		my_stu.finished_test = True
		my_stu.save()
	return render(request, 'random_gen.html', {'count': user_count})

	
