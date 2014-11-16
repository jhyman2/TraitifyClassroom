import string
import random

from django.core.urlresolvers import reverse
from django.views.generic import View
from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404

from models import Student
from forms import StudentForm
from traitify import Traitify

public_key = 'sq1ekdq2849c1778327k1cfqho'
secret_key = 'cdpfn6kmpktklsmtttjerd7fg1'

class PictureView(View):
	def get(self, request, *args, **kwargs):
		pass

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

class LogView(View):

    def get(self, request, *args, **kwargs):
        form = StudentForm()
        return render(request, 'studentlogin.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST)
        if form.is_valid():
            stu = form.save()
            test_id = self.get_assessment()
            stu.test_id = test_id
            stu.save()
            request.session['stu_id'] = stu.id
            request.session['test_id'] = test_id
            return HttpResponseRedirect(reverse('tests:test_detail'))
        return render(request, 'studentlogin.html', {'form': form})

    def get_assessment(self):
        traitify = Traitify(secret_key)
        # Get the decks
        decks = traitify.get_decks()
        # Set deck id
        traitify.deck_id = decks[0].id
        # Create an assessment
        assessment = traitify.create_assessment()
        return assessment.id


class TestDetailView(TemplateView):
    template_name = 'studentquiz.html'

    def get_context_data(self, **kwargs):
        session_id = self.request.session['test_id']
        return {'test_id': session_id}
        
    def post(self, request, *args, **kwargs):
		cur_stu = get_object_or_404(Student, pk=request.session['stu_id'])
		cur_stu.finished_test = True
		cur_stu.save()
		return {}

class GenerateView(View):

    def get(self, request, user_count, *args, **kwargs):
        traitify = Traitify(secret_key)
        decks = traitify.get_decks()
        traitify.deck_id = decks[0].id
        for i in range(user_count):
            cur_id = traitify.create_assessment().id
            first_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
            last_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
            my_stu = Student.objects.create(
                first=first_name,
                last=last_name,
                test_id=cur_id
            )
            slides = traitify.get_slides(cur_id)
            for slide in slides:
                slide.response = random.choice([True, False])
                slide.time_taken = 200
            slides = traitify.update_slides(cur_id, slides)
            my_stu.finished_test = True
            my_stu.save()
        return render(request, 'random_gen.html', {'count': user_count})
