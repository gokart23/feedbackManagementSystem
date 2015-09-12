from django.shortcuts import render
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory,BaseFormSet
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required

from forms import LoginForm
from itertools import chain

from main.models import *
from main.forms import *

import csv

# Create your views here.
def verifyLogin(request):
    c={}
    c.update(csrf(request))
    if request.method == "GET":
        form = LoginForm()
        c.update({'form':form})
        return render(request, 'login.html', c)
    elif request.method == "POST":
        form = LoginForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            c={}
            c.update(csrf(request))
            login(request, user)
            courseIntegrated,notices = [],[]
            countNotices=0
            if user.person.isstud:
                courses = user.person.courses.all()
                total,num=0,0
                stats=[]
                for course in courses:
                    courseIntegrated.append(CourseIntegratedSurvey(course, course.surveys_course.all()))
                    for survey in course.surveys_course.all():
                        total+=1
                        if user.person in survey.students.all():
                            num+=1    
                    for n in course.notice_course.all():
                        countNotices+=1
                        notices.append(n)
                    stats.append(CourseStats(course, int((float(num/total)+0.05)*100)))
                return render(request, 'StudPage.html', {'name':user.person.user.username, 'courseIntegrated':courseIntegrated, 'role':'Student', 'notices':notices, 'countNotices':countNotices, 'stats':stats})
            elif user.person.isprof:
                courses = user.person.courses.all()
                notices,stats = [],[]
                countNotices=0
                for course in courses:
                    courseIntegrated.append(CourseIntegratedSurvey(course, course.surveys_course.all()))
                    num,total=0,0
                    for person in course.person_set.all():
                        total+=1
                        for survy in course.surveys_course.all():
                            if person in survy.students.all():
                                num+=1
                    for n in course.notice_course.all():
                        countNotices+=1
                        notices.append(n)
                    stats.append(CourseStats(course, int((float(num)/total+0.05)*100)))
                notices.sort(key= lambda x: x.created_date, reverse=True) 
                c.update({'name':user.person.user.username, 'courseIntegrated':courseIntegrated, 'role':'Professor', 'noticeForm':AddNoticeForm(), 'notices':notices, 'countNotices':countNotices, 'stats':stats})
                return render(request, 'PersonPage.html', c)
            elif user.person.isadmin:
                courses = Course.objects.all()
                notices,stats = [],[]
                countNotices=0
                for course in courses:
                    courseIntegrated.append(CourseIntegratedSurvey(course, course.surveys_course.all()))
                    num,total=0,0
                    for person in course.person_set.all():
                        total+=1
                        for survy in course.surveys_course.all():
                            if person in survy.students.all():
                                num+=1
                    for n in course.notice_course.all():
                        countNotices+=1
                        notices.append(n)
                    stats.append(CourseStats(course, int((float(num)/total+0.05)*100)))
                notices.sort(key= lambda x: x.created_date, reverse=True) 
                c.update({'name':user.person.user.username, 'courseIntegrated':courseIntegrated, 'role':'Administrator', 'noticeForm':AddNoticeForm(), 'notices':notices, 'countNotices':countNotices, 'stats':stats, 'users':CsvUploadForm()})
                return render(request, 'AdminPage.html', c)
        else:
            return render(request, 'login.html', {'form':form})

class CourseIntegratedSurvey:
    def __init__(self, course, survey):
        self.course = course
        self.survey = survey

class CourseStats:
    def __init__(self, course, percent):
        self.course = course
        self.percent = percent
                                                                                                                                        
def landingPage(request):
    c={}
    c.update(csrf(request))
    if request.method == "GET":
        form = LoginForm()
        c.update({'form':form})
        return render(request, 'index.html', c)
    elif request.method == "POST":
        form = LoginForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print user
        if user is not None:
            c={}
            c.update(csrf(request))
            login(request, user)
            courseIntegrated,notices = [],[]
            countNotices=0
            if user.person.isstud:
                courses = user.person.courses.all()
                total,num=0,0
                stats=[]
                for course in courses:
                    courseIntegrated.append(CourseIntegratedSurvey(course, course.surveys_course.all()))
                    for survey in course.surveys_course.all():
                        total+=1
                        if user.person in survey.students.all():
                            num+=1    
                    for n in course.notice_course.all():
                        countNotices+=1
                        notices.append(n)
                    stats.append(CourseStats(course, 0 if total is 0 else int((float(num/total)+0.05)*100)))
                return render(request, 'StudPage.html', {'name':user.person.user.username, 'courseIntegrated':courseIntegrated, 'role':'Student', 'notices':notices, 'countNotices':countNotices, 'stats':stats})
            elif user.person.isprof:
                courses = user.person.courses.all()
                notices,stats = [],[]
                countNotices=0
                for course in courses:
                    courseIntegrated.append(CourseIntegratedSurvey(course, course.surveys_course.all()))
                    num,total=0,0
                    for person in course.person_set.all():
                        total+=1
                        for survy in course.surveys_course.all():
                            if person in survy.students.all():
                                num+=1
                    for n in course.notice_course.all():
                        countNotices+=1
                        notices.append(n)
                    stats.append(CourseStats(course, int((float(num)/total+0.05)*100)))
                notices.sort(key= lambda x: x.created_date, reverse=True) 
                c.update({'name':user.person.user.username, 'courseIntegrated':courseIntegrated, 'role':'Professor', 'noticeForm':AddNoticeForm(), 'notices':notices, 'countNotices':countNotices, 'stats':stats})
                return render(request, 'PersonPage.html', c)
            elif user.person.isadmin:
                courses = Course.objects.all()
                notices,stats = [],[]
                countNotices=0
                for course in courses:
                    courseIntegrated.append(CourseIntegratedSurvey(course, course.surveys_course.all()))
                    num,total=0,0
                    for person in course.person_set.all():
                        total+=1
                        for survy in course.surveys_course.all():
                            if person in survy.students.all():
                                num+=1
                    for n in course.notice_course.all():
                        countNotices+=1
                        notices.append(n)
                    stats.append(CourseStats(course, int((float(num)/total+0.05)*100)))
                notices.sort(key= lambda x: x.created_date, reverse=True) 
                c.update({'name':user.person.user.username, 'courseIntegrated':courseIntegrated, 'role':'Administrator', 'noticeForm':AddNoticeForm(), 'notices':notices, 'countNotices':countNotices, 'stats':stats, 'userForm':CsvUploadForm()})
                return render(request, 'AdminPage.html', c)
        else:
            return render(request, 'login.html', {'form':form})
   
def user_logout(request):
    logout(request)
    c={}
    c.update(csrf(request))
    form = LoginForm()
    c.update({'form':form})
    return render(request, 'index.html', c)

class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False
 
def AddSurvey(request,o_id):
        if request.user.is_authenticated():
                c={}
           	courses = request.user.person.courses.all()
                courseIntegrated,notices,stats = [],[],[]
                countNotices=0
                for course in courses:
                    courseIntegrated.append(CourseIntegratedSurvey(course, course.surveys_course.all()))
                    num,total=0,0
                    for person in course.person_set.all():
                        total+=1
                        for survy in course.surveys_course.all():
                            if person in survy.students.all():
                                num+=1
                    for n in course.notice_course.all():
                        countNotices+=1
                        notices.append(n)
                    stats.append(CourseStats(course, int((float(num)/total+0.05)*100)))
                    notices.sort(key= lambda x: x.created_date, reverse=True) 
                c.update({'name':request.user.person.user.username, 'courseIntegrated':courseIntegrated, 'role':'Professor', 'noticeForm':AddNoticeForm(), 'notices':notices, 'countNotices':countNotices, 'stats':stats})
           	c.update(csrf(request))
           	question_formset = formset_factory(QuestionForm,max_num=50,formset=RequiredFormSet)
           	if request.method == "POST":
          		question_forms = question_formset(request.POST)
          		new_survey = Survey()
          		new_survey.course = Course.objects.filter(id=o_id).get()
          		survey_no = len(Survey.objects.all())+1
          		new_survey.name = str(survey_no)
          		new_survey.save()
          		for question in question_forms:
         			if question.is_valid():
            				temp = question.save(commit=False)
            				#temp.Survey = new_survey
            				#print temp.Survey
            				temp.save()
            				new_survey.questions.add(temp)
            				if not temp.isAnsText:
           					analytic = AnalyticsObjective()
           					analytic.question = temp
           					analytic.survey = new_survey
           					analytic.save()
         			else:
            				c.update({'question_formset':question_forms})
            				return render (request,'PersonPage.html',c)
          		c.update({'messages':"Succesfully added survey"})
          		return render(request, 'PersonPage.html', c)
           	else:
          		c.update({'question_formset':question_formset, 'addsurvey':True})
          		return render(request,'PersonPage.html',c)

def GiveSurvey(request,o_id):
	c={}
	c.update(csrf(request))
	courses = request.user.person.courses.all()
	courseIntegrated,notices = [],[]
        for course in courses:
                courseIntegrated.append(CourseIntegratedSurvey(course, course.surveys_course.all()))
	countNotices=0
	surv = Survey.objects.filter(id=o_id)[0]
	questions = surv.questions.all()
	courses = request.user.person.courses.all()
        total,num=0,0
        stats=[]
        for course in courses:
            courseIntegrated.append(CourseIntegratedSurvey(course, course.surveys_course.all()))
            for survey in course.surveys_course.all():
                total+=1
                if request.user.person in survey.students.all():
                    num+=1    
            for n in course.notice_course.all():
                countNotices+=1
                notices.append(n)
            stats.append(CourseStats(course, int((float(num/total)+0.05)*100)))
            c.update({'name':request.user.username, 'courseIntegrated':courseIntegrated, 'role':'Student', 'notices':notices, 'countNotices':countNotices, 'stats':stats,})
            if request.method=="POST":
		form = GiveSurveyForm(request.POST,questions=questions)
		if form.is_valid():
                        surv.students.add(request.user.person)		
			for question in questions:
				if not question.isAnsText:
					analytic = AnalyticsObjective.objects.filter(question=question).get()
					temp = form.cleaned_data['%s' %question.name].rating
					#The Hard Work done to write should be ignored------(For the crudeness of further lines I can't be held responsible it was duddu's idea)
					if temp == 1:
						analytic.one = analytic.one+1
					elif temp ==2:
						analytic.second = analytic.second +1
					elif temp ==3:
						analytic.third = analytic.third +1
					elif temp ==4:
						analytic.fourth = analytic.fourth +1
						print analytic.fourth
					elif temp ==5:
						analytic.fifth = analytic.fifth +1 
					analytic.save()
				else:
					analytic = AnalyticsSubjective()
					analytic.question = question
					analytic.answer = form.cleaned_data['%s' %question.name]
					analytic.save()
			c.update({'messages':"Your feedback has been successfully recorded"})               
                        return render(request, 'StudPage.html', c)	        

	else:
	        if request.user.person in surv.students.all():
	            c.update({'messages':"Sorry, you have already given the survey"})
	            return render(request, 'StudPage.html', c)
		form = GiveSurveyForm(questions=questions)
		c.update({'form':form, 'name':request.user.username, 'role':'Student', 'givesurvey':True, 'surveyname':surv.name})
		return render (request,'StudPage.html',c)

def AnalyticPage(request,o_id):
        if request.user.is_authenticated():
                c={}
                courses = request.user.person.courses.all()
           	courseIntegrated = []
                for course in courses:
                    courseIntegrated.append(CourseIntegratedSurvey(course, course.surveys_course.all()))
                survey = Survey.objects.filter(id=o_id)[0]
                c.update({'name':request.user.username, 'courseIntegrated':courseIntegrated, 'surveyname':survey.name, 'role':"Professor"})
           	questionsObjective = AnalyticsObjective.objects.filter(survey=survey)
           	questions = survey.questions.all()
           	docs = []
           	qrating = []
           	for question,q2 in zip(questionsObjective,questions):
           	    rat = (1*question.one + 2*question.second + 3*question.third + 4*question.fourth + 5*question.fifth)/float(question.one+question.second+question.third+question.fourth+question.fifth+1)
           	    qrating.append((rat,question.question.name))
           	for question in questions:
          		if question.isAnsText:
         			docs.append(AnalyticsSubjective.objects.filter(question=question))
           	questionsSubjective = list(chain(*docs))
           	print len(questionsSubjective)
           	#questionsSubjective = [AnalyticsSubjective.objects.filter(question=question) for question in questions: if question.isAnsText:]
           	c.update({'questionsSubjective':questionsSubjective,'questionsObjective':questionsObjective,'survey':survey,'qrating':qrating})
           	return render(request,'AnalyticsPage.html',c)

def CreateUser(request):
	c={}
	c.update(csrf(request))
	if request.method == "POST":
		form = CsvUploadForm(request.POST,request.FILES)
		courses = Course.objects.all()
                courseIntegrated,notices,stats = [],[],[]
                countNotices=0
                for course in courses:
                    courseIntegrated.append(CourseIntegratedSurvey(course, course.surveys_course.all()))
                    num,total=0,0
                    for person in course.person_set.all():
                        total+=1
                        for survy in course.surveys_course.all():
                            if person in survy.students.all():
                                num+=1
                    for n in course.notice_course.all():
                        countNotices+=1
                        notices.append(n)
                    stats.append(CourseStats(course, int((float(num)/total+0.05)*100)))
                notices.sort(key= lambda x: x.created_date, reverse=True) 
                c.update({'name':request.user.username, 'courseIntegrated':courseIntegrated, 'role':'Administrator', 'noticeForm':AddNoticeForm(), 'notices':notices, 'countNotices':countNotices, 'stats':stats, 'users':CsvUploadForm(),})
		if form.is_valid():
			csv_file = request.FILES.get('file','')
			reader = csv.DictReader(csv_file,fieldnames=('Name','Email','Password',))
			for entry in reader:
				user = User.objects.create_user(username=entry['Email'],email=entry['Email'],password=entry['Password'])
				user.save()
				person = Person (user=user,isstud=True)
				person.save()
			c.update({'messages':"Students successfully added"})            
                        return render(request,'AdminPage.html',c)
      		else:
			c.update({'form':form})
			c.update({'messages':"Students not added"})
                        return render(request,'AdminPage.html',c)
	else:
		form = CsvUploadForm()
		c.update({'form':form})
	

def AddNotice(request):
	noticeform = AddNoticeForm()
	c = {}
	c.update(csrf(request))
	if request.method == "POST":
		noticeform = AddNoticeForm(request.POST)
		if noticeform.is_valid():
			notice = noticeform.save()
			courses = request.user.person.courses.all()
                        courseIntegrated,notices,stats = [],[],[]
                        countNotices=0
                        for course in courses:
                            courseIntegrated.append(CourseIntegratedSurvey(course, course.surveys_course.all()))
                            num,total=0,0
                            for person in course.person_set.all():
                                total+=1
                                for survy in course.surveys_course.all():
                                    if person in survy.students.all():
                                        num+=1
                            for n in course.notice_course.all():
                                countNotices+=1
                                notices.append(n)
                            stats.append(CourseStats(course, int((float(num)/total+0.05)*100)))                        
                            notices.sort(key= lambda x: x.created_date, reverse=True) 
                        c.update({'name':request.user.person.user.username, 'courseIntegrated':courseIntegrated, 'role':'Professor', 'noticeForm':AddNoticeForm(), 'notices':notices, 'countNotices':countNotices, 'stats':stats, 'messages':"Notice successfully posted"})
                   	c.update(csrf(request))
			return render(request, 'PersonPage.html', c)
		else:
		      print request.POST['course']
		      return HttpResponse(noticeform.errors)
	else:
		c.update({'noticeForm':noticeform})
	return render(request,'AddNotice.html',c)
	
def SendMessage(request):
  c = {}
  c.update(csrf(request))
  if request.method == "POST":
    form = MessageForm(request.POST)
    if form.is_valid():
      message = form.save(commit=False)
      message.mfrom = request.user.person
      message.save()
      return HttpResponse("YES")
    else:
      return HttpResponse("NO")
  else:
    form = MessageForm()
    c.update({'form':form})
  return render (request,'SendMessage.html',c)