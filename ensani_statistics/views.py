from django.shortcuts import render


# Create your views here.


def amar_avalie(request):
    return render(request, 'ensani_statistics/vaziate_avalie.html')


def amar_gordan_gorhan(request):
    return render(request, 'ensani_statistics/amar_gordan_gorhan.html')


def amar_be_tafkik_madrk_tahsili(request):
    return render(request, 'ensani_statistics/amar_be_tafkik_madrak_tahsili.html')


