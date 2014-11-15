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
			test_id = get_assessment()
			print test_id
			stu.test_id = test_id
			stu.save()
			request.session['test_id'] = test_id
			return HttpResponseRedirect('/tests/assess/')
	else:
		form = StudentForm()
	return render(request, 'tests/log.html', {'form': form})
	
def testDetail(request):
	session_id = request.session['test_id']
	return render(request, 'tests/assess.html', {'test_id': session_id})
	
def testResult(request):
	cur_stu = Student.objects.get(test_id=request.session['test_id'])
	cur_stu.finished_test = True
	cur_stu.save()
	return render(request, 'tests/assess_confirm.html', {})
