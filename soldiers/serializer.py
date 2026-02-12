# serializers.py
from rest_framework import serializers
from .models import Soldier


class SoldierFullSerializer(serializers.ModelSerializer):
    gordan = serializers.CharField(source='Gordan.name', read_only=True)
    battalion_group = serializers.CharField(source='battalion_group.name', read_only=True)
    t_gordan = serializers.CharField(source='t_Gordan.name', read_only=True)
    t_battalion_group = serializers.CharField(source='t_battalion_group.name', read_only=True)

    class Meta:
        model = Soldier
        fields = [
            # -------- اطلاعات پایه --------
            "id",
            "National_Code",
            "name",
            "family",
            "fathers_name",
            "phone_number",
            "province_name",
            "city_name",
            "Date_of_birth",
            "Date_of_dispatch",
            "Grade",
            "marital_status",
            "Religion",
            "organization_type",

            # -------- وضعیت پذیرش --------
            "has_been_accepted",
            "acceptance_code",
            "in_coures",
            "tatbigh",
            "IsCheckout",
            "tarikh_paziresh",

            # -------- سلامت --------
            "physical_condition",
            "Type_of_disease",

            # -------- امریه و بسیج --------
            "Amriye",
            "Sufficiency_of_mobilization",
            "basij_efficiency",

            # -------- امتیازات --------
            "rank",

            # -------- روابط خواندنی --------
            "gordan",
            "battalion_group",
            "t_gordan",
            "t_battalion_group",
        ]
