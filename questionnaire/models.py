from django.db import models


class Block(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.name

class User(models.Model):
    full_name = models.CharField(max_length=100)
    chosen_group = models.ForeignKey('Group', on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Question(models.Model):
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class Competence(models.Model):
    name = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.name


class Group(models.Model):
    title = models.CharField(max_length=50)
    users = models.ManyToManyField(User, blank=True)
    show_results = models.BooleanField(default=True)
    num_competences_displayed = models.IntegerField(default=5)

    def __str__(self):
        return self.title


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    competence = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class UserResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competence_name = models.CharField(max_length=100)
    competence_count = models.IntegerField()
