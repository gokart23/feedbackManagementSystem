from django.contrib import admin
from models import *
# Register your models here.

admin.site.register(Person)
admin.site.register(Course)
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(AnalyticsObjective)
admin.site.register(AnalyticsSubjective)
admin.site.register(OptionTypes)
admin.site.register(Notice)
admin.site.register(Message)