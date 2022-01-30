from rest_framework import serializers

from vacancies.models import Vacancy, Skill


class VacancyListSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Vacancy
        fields = ['id', 'name', 'text', 'skills', 'username']


class VacancySerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field='name'
    )

    def is_valid(self, raise_exception=False):
        self._skills = self.initial_data.pop("skills")
        super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        vacancy = Vacancy.objects.create(**validated_data)

        for skill in self._skills:
            obj, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(obj)

        vacancy.save()
        return vacancy

    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyUpdateSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field='name'
    )

    def is_valid(self, raise_exception=False):
        self._skills = self.initial_data.pop("skills")
        super().is_valid(raise_exception=raise_exception)

    def save(self):
        vacancy = super().save()

        for skill in self._skills:
            obj, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(obj)

        vacancy.save()
        return vacancy

    class Meta:
        model = Vacancy
        fields = ["name", "status", "slug", "text", "skills"]


class VacancyDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ["id"]
