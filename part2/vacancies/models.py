from django.contrib.auth.models import User
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    STATUS = [("draft", "Черновик"), ("open", "Открыта"), ("closed", "Closed")]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=50)
    name = models.CharField(max_length=50, null=True)
    text = models.CharField(max_length=1000)
    status = models.CharField(max_length=10, choices=STATUS, default="draft")
    created = models.DateField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill)
    likes = models.IntegerField(default=0)

    @property
    def username(self):
        return self.user.username if self.user else None

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

        ordering = ['name']
