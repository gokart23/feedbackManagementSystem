from django.forms import ModelForm
from django import forms
from django.forms import Textarea, Select
from django.contrib.auth import authenticate

from models import *

class LoginForm(ModelForm):
   
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }
        
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return cleaned_data

class SurveyForm(ModelForm):
	
	course = forms.ModelChoiceField(queryset = Course.objects.all())
	class Meta:
		model = Survey
		exclude = ('questions','students',)

class AddNoticeForm(ModelForm):

	class Meta:
		model = Notice
		exclude = ('created_date',)
		widgets = {
                            'content': Textarea(),
                }
		
class GiveSurveyForm(forms.Form):

	def __init__(self,*args,**kwargs):
		questions = kwargs.pop('questions')
		super(GiveSurveyForm,self).__init__(*args,**kwargs)
		for question in questions:
			if question.isAnsText:
				self.fields['%s' %question.name]=forms.CharField(label=question.name)
			else:
				self.fields['%s' %question.name]=forms.ModelChoiceField(queryset = OptionTypes.objects.all())
class MessageForm(ModelForm):
	mto = forms.ModelChoiceField(queryset = Person.objects.filter(isprof=True))
	class Meta:
		model = Message
		exclude = ('mfrom',)

class CsvUploadForm(forms.Form):
	file = forms.FileField(required=True)

class QuestionForm(ModelForm):
	class Meta:
		model = Question
		exclude = ('survey',)