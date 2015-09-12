from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import ListField
from main.fields import CustomListField

class ListField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, CustomListField, **kwargs)

class Course(models.Model):
	year = models.SmallIntegerField(default=2014)
	code = models.CharField(max_length=10)
        #surveys = models.ManyToManyField('Survey',related_name='course_surveys', blank=True)
	
	def __unicode__(self):
		return "%s" %self.code

class Survey(models.Model):
    	name = models.CharField(max_length=100)
	questions = models.ManyToManyField('Question',related_name='survey_questions', blank=True)
	course = models.ForeignKey('Course',related_name='surveys_course')
	students = models.ManyToManyField('Person',related_name='survey_students', blank=True)
	
	def __unicode__(self):
		return "%s" %self.name

class Person(models.Model):
	isadmin = models.BooleanField(default=False)
	isprof = models.BooleanField(default=False)
	isstud = models.BooleanField(default=False)
	ishod = models.BooleanField(default=False)
	user = models.OneToOneField(User)
	courses = models.ManyToManyField('Course', blank=True)
	def __unicode__(self):
		return "%s" %self.user.username

class Question(models.Model):
	name = models.CharField(max_length = 250)
	isAnsText = models.BooleanField(default=False)
	#options = ListField(models.CharField(blank=True, null=True))
	
        def __unicode__(self):
	    return "%s" %self.name

class AnalyticsObjective(models.Model):
	question = models.ForeignKey('Question',related_name='AnalyticsObjective_question',blank=True)
	survey = models.ForeignKey('Survey',related_name='AnalyticsObjective_survey',blank=True)
	one = models.SmallIntegerField(default=0)
	second = models.SmallIntegerField(default=0)
	third = models.SmallIntegerField(default=0)
	fourth = models.SmallIntegerField(default=0)
	fifth = models.SmallIntegerField(default=0)

class AnalyticsSubjective(models.Model):
	question = models.ForeignKey('Question',related_name='AnalyticsSubjective_question',blank=True)
	answer = models.CharField(max_length = 9000)

class Notice(models.Model):
        created_date = models.DateTimeField(auto_now_add = True)
       	course = models.ManyToManyField('Course',related_name='notice_course', blank=False)
        content = models.CharField(max_length=9000)

class OptionTypes(models.Model):
	''' Rating out of 5 point scale
		1.Strongly Disagree 2.Disagree 3.Average 4.Agree 5.Strongly Agree
		1.Very Bad 2.Bad 3.Avergae 4.Good 5.Excellent'''
	rating = models.SmallIntegerField()
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return "%s" %self.name		

class Message(models.Model):
	mfrom = models.ForeignKey(Person,related_name='message_mfrom')
	mto = models.ForeignKey(Person,related_name='message_mto')
	subject = models.CharField(max_length=300)
	content = models.CharField(max_length=9000)