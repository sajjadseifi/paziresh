from django.urls import path
from .views import *

urlpatterns = [
    path('letter/create/checkout', CreateCheckoutLetter.as_view(), name='CreateCheckoutLetter'),
    path('letter/create/commission/<str:pk>', CreateCommissionLetter.as_view(), name='CreateCommissionLetter'),
    path('letter/create/before/course/commission', CreateBeforeCourseCommissionLetter.as_view(),
         name='CreateBeforeCourseCommissionLetter'),
    path('letter/create/traininginquiry', CreateTrainingInquiryLetter.as_view(), name='CreateTrainingInquiryLetter'),
    path('letter/create/register', CreateRegisterLetter.as_view(), name='CreateRegisterLetter'),
    path('letter/all/checkout', AllCheckoutLetter, name='AllCheckoutLetter'),
    path('letter/all/normal', AllNormalLetter, name='AllNormalLetter'),
    path('letter/p/checkout/<int:pk>', PrintCheckoutLetter, name='PrintCheckoutLetter'),
    path('letter/p/checkout/commission/<int:pk>', PrintCheckoutCommissionLetter, name='PrintCheckoutCommissionLetter'),
    path('letter/p/normall/training/inquiry/<int:pk>', PrintTrainingInquiryLetter, name='PrintTrainingInquiryLetter'),
]
