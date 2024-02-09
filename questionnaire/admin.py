from django.contrib import admin
from .models import Competence, User, Question,UserAnswer,Group

admin.site.register(Competence)
admin.site.register(User)
admin.site.register(UserAnswer)
admin.site.register(Question)
admin.site.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_results')