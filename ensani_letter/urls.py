from django.urls import path
from .views import *

urlpatterns = [
    path('letter/create/checkout', CreateCheckoutLetter.as_view(), name='CreateCheckoutLetter'),
    path('letter/create/commission/<str:pk>', CreateCommissionLetter.as_view(), name='CreateCommissionLetter'),
    path('letter/create/traininginquiry', CreateTrainingInquiryLetter.as_view(), name='CreateTrainingInquiryLetter'),
    path('letter/all/checkout', AllCheckoutLetter, name='AllCheckoutLetter'),
    path('letter/all/normal', AllNormalLetter, name='AllNormalLetter'),
]
