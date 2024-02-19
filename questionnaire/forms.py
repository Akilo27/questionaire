from django import forms
from .models import Group, Competence, Question, Block


class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ['name', 'content']
        labels = {
            'name': 'Название',
            'content': 'Контент'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'users', 'show_results', 'num_competences_displayed']
        labels = {
            'title': 'Название',
            'users': 'Пользователи',
            'show_results': 'Показывать результаты',
            'num_competences_displayed': 'Количество отображаемых компетенций'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


class CompetenceForm(forms.ModelForm):
    class Meta:
        model = Competence
        fields = ['name', 'questions']
        labels = {
            'name': 'Название',
            'questions': 'Вопросы',
        }


        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        labels = {
            'text': 'Текст'
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'})
        }