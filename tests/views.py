import string
import random

from django.core.urlresolvers import reverse
from django.views.generic import View
from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404

from models import Student
from forms import StudentForm
from traitify import Traitify

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

public_key = 'sq1ekdq2849c1778327k1cfqho'
secret_key = 'cdpfn6kmpktklsmtttjerd7fg1'

class PictureView(View):

	def aggregrate_data(self):
		traitify = Traitify(secret_key)
		decks = traitify.get_decks()
		traitify.deck_id = decks[0].id
		complete_students = Student.objects.filter(finished_test=True)
		trait_list = []
		trait_count = {}
		for stu in complete_students:
			personality_types = traitify.get_personality_types(stu.test_id)
			# Get an assessment's results (personality type traits)
			personality_type = personality_types["personality_types"][0]["personality_type"]
			main_trait = personality_type.name
			trait_list.append(main_trait)
		for trait in set(trait_list):
			trait_count[trait] = 0
		for i in trait_list:
			trait_count[i] += 1
		return trait_count

	def generate_png(self, trait_dict):
		labels = trait_dict.keys()
		sizes = []
		for t in labels:
			print t
			sizes.append(trait_dict[t])
		plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True)
		plt.axis('equal')
		pict_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(12))
		pict_name = pict_name + '.png'
		plt.savefig('static/' + pict_name)
		return pict_name
		
	def get(self, request, *args, **kwargs):
		trait_dict = self.aggregrate_data()
		pict = self.generate_png(trait_dict)
		return render(request, 'groupimage.html', {'pict': pict})
		
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
        for i in range(int(user_count)):
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
