from django import forms
from .models import Group, Competence, Question


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'users', 'show_results','num_competences_displayed']


class CompetenceForm(forms.ModelForm):
    class Meta:
        model = Competence
        fields = ['name', 'questions']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']