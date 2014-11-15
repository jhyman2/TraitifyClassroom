from django.shortcuts import render, HttpResponseRedirect
from forms import StudentForm
from traitify import Traitify

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
			#TODO generate id
			test_id = get_assessment()
			print test_id
			stu.test_id = test_id
			request.session['test_id'] = test_id
			return HttpResponseRedirect('/tests/assess/')
	else:
		form = StudentForm()
	return render(request, 'tests/log.html', {'form': form})
	
def testDetail(request):
	pass
	
def testResult(request):
	pass
