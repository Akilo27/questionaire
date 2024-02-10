from django.contrib import admin
from .models import Competence, User, Question,UserAnswer,Group

from django.contrib import admin
from .models import User, Group, Competence, Question, UserAnswer


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'chosen_group')
    list_filter = ('chosen_group',)
    search_fields = ('full_name',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'show_results')


class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'competence', 'date')


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Competence, CompetenceAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
