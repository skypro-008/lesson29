import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from vacancies.models import Vacancy, Skill
from vacancies.serializers import VacancySerializer, VacancyListSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, VacancyDeleteSerializer


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)
    #
    #     search_text = request.GET.get("text", None)
    #     if search_text:
    #         self.object_list = self.object_list.filter(text=search_text)
    #
    #     self.object_list = self.object_list.select_related('user').prefetch_related('skills')
    #
    #     paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
    #     page_number = request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    #
    #     # vacancies = []
    #     # for vacancy in self.object_list:
    #     #     vacancies.append({
    #     #         "id": vacancy.id,
    #     #         "name": vacancy.name,
    #     #         "text": vacancy.text,
    #     #         "username": vacancy.user.username,
    #     #         "skills": list(map(str, vacancy.skills.all())),
    #     #     })
    #
    #     # list(map(lambda x: setattr(x, "username", x.user.username), self.object_list))
    #     serialized_data = VacancyListSerializer(self.object_list, many=True)
    #
    #     response = {
    #         "items": serialized_data.data,
    #         "num_pages": page_obj.paginator.num_pages,
    #         "total": page_obj.paginator.count,
    #     }
    #     return JsonResponse(response, safe=False)


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

    # def get(self, request, *args, **kwargs):
    #     vacancy = self.get_object()
    #
    #     return JsonResponse(VacancySerializer(vacancy).data)


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer

    # def post(self, request, *args, **kwargs):
    #     vacancy_data = VacancyCreateSerializer(data=json.loads(request.body))
    #     if vacancy_data.is_valid():
    #         vacancy_data.save()
    #     else:
    #         return JsonResponse(vacancy_data.errors)
    #
    #     # vacancy.user = get_object_or_404(User, pk=vacancy_data["user_id"])
    #     # vacancy.save()
    #     #
    #     # for skill in vacancy_data["skills"]:
    #     #     skill_obj, _ = Skill.objects.get_or_create(name=skill)
    #     #     vacancy.skills.add(skill_obj)
    #
    #     return JsonResponse(vacancy_data.data)


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer

    # def post(self, request, *args, **kwargs):
    #     super().post(request, *args, **kwargs)
    #
    #     vacancy_data = json.loads(request.body)
    #     self.object.slug = vacancy_data["slug"]
    #     self.object.text = vacancy_data["text"]
    #     self.object.status = vacancy_data["status"]
    #
    #     for skill in vacancy_data["skills"]:
    #         skill_obj, _ = Skill.objects.get_or_create(name=skill)
    #         self.object.skills.add(skill_obj)
    #
    #     self.object.save()
    #     return JsonResponse({
    #         "id": self.object.id,
    #         "user_id": self.object.user_id,
    #         "slug": self.object.slug,
    #         "text": self.object.text,
    #         "status": self.object.status,
    #         "skills": list(self.object.skills.all().values_list("name", flat=True)),
    #         "created": self.object.created,
    #     })


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDeleteSerializer

    # def delete(self, request, *args, **kwargs):
    #     super().delete(request, *args, **kwargs)
    #
    #     return JsonResponse({"status": "ok"}, status=200)


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
