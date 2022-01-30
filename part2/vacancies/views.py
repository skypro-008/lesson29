from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q, F
from django.http import JsonResponse
from django.views import View
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from vacancies.models import Vacancy, Skill
from vacancies.serializers import (
    VacancySerializer,
    VacancyListSerializer,
    VacancyCreateSerializer,
    VacancyUpdateSerializer,
    VacancyDeleteSerializer,
    SkillSerializer
)


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    def get(self, request, *args, **kwargs):
        vacancy_name = request.GET.get("text", None)
        if vacancy_name:
            self.queryset = self.queryset.filter(
                name__contains=vacancy_name
            )

        skills = request.GET.getlist("skill", None)
        skills_q = None
        for skill_name in skills:
            if not skills_q:
                skills_q = Q(skills__name__contains=skill_name)
            else:
                skills_q |= Q(skills__name__contains=skill_name)
        if skills_q:
            self.queryset = self.queryset.filter(skills_q)

        return super().get(request, *args, **kwargs)


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDeleteSerializer


class UserVacancyDetailView(View):
    def get(self, request):
        users_qs = User.objects.annotate(vacancies=Count('vacancy'))

        paginator = Paginator(users_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        users = []
        for user in users_qs:
            users.append({
                "id": user.id,
                "name": user.username,
                "vacancies": user.vacancies,
            })

        response = {
            "items": users,
            "avg": users_qs.aggregate(Avg('vacancies')),
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }
        return JsonResponse(response, safe=False)


class VacancyLikeView(ListModelMixin, UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

    def put(self, request, *args, **kwargs):
        Vacancy.objects.filter(pk__in=request.data).update(likes=F('likes') + 1)

        return Response(VacancySerializer(Vacancy.objects.filter(pk__in=request.data), many=True).data)
