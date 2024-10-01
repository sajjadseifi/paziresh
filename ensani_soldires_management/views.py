from django.shortcuts import render
from soldiers.models import Soldier
from ensani_letter.models import NormalLetterModels


# Create your views here.


def soldier_search(request):
    query = request.GET.get('name')
    family = request.GET.get('family')
    national_code = request.GET.get('national_code')
    physical_condition = request.GET.get('physical_condition')
    marital_status = request.GET.get('marital_status')
    religion = request.GET.get('religion')

    soldiers = Soldier.objects.all()

    if query:
        soldiers = soldiers.filter(name__icontains=query)
    if family:
        soldiers = soldiers.filter(family__icontains=family)
    if national_code:
        soldiers = soldiers.filter(National_Code__icontains=national_code)
    if physical_condition:
        soldiers = soldiers.filter(physical_condition__icontains=physical_condition)
    if marital_status:
        soldiers = soldiers.filter(marital_status=marital_status)
    if religion:
        soldiers = soldiers.filter(Religion__icontains=religion)

    context = {
        'results': soldiers
    }

    return render(request, 'ensani_soldires_management/soldier_search.html', context)


def soldire_details(request,code):
    if request.method == "GET":
        soldire = Soldier.objects.filter(National_Code=code).first()
        normalLetter = NormalLetterModels.objects.filter(soldire=soldire).all()
        context = {'soldier': soldire, 'normalLetter': normalLetter}
        return render(request, 'ensani_soldires_management/soldire_details.html', context)
