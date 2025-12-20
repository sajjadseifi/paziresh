from soldiers.models import Soldier
from ensani_letter.models import CheckoutLetterModels,FarajaNormallLetter,MoarefiNormallLetter,NormalLetterModels,RawLetter,RegisterNormalLetter,RunawayNormallLetter 


def cleanup_old_period_data():
    Soldier.objects.all().delete()
    CheckoutLetterModels.objects.all().delete()
    FarajaNormallLetter.objects.all().delete()
    MoarefiNormallLetter.objects.all().delete()
    RegisterNormalLetter.objects.all().delete()
    RunawayNormallLetter.objects.all().delete()
    NormalLetterModels.objects.all().delete()
