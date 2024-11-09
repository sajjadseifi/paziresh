from django.urls import path
from .views import *

urlpatterns = [
    path('letter/create/checkout', CreateCheckoutLetter.as_view(), name='CreateCheckoutLetter'),
    path('letter/create/commission/<str:pk>', CreateCommissionLetter.as_view(), name='CreateCommissionLetter'),
    path('letter/create/before/course/commission', CreateBeforeCourseCommissionLetter.as_view(),
         name='CreateBeforeCourseCommissionLetter'),
    path('letter/create/traininginquiry', CreateTrainingInquiryLetter.as_view(), name='CreateTrainingInquiryLetter'),
    path('letter/create/register', CreateRegisterLetter.as_view(), name='CreateRegisterLetter'),
    path('letter/create/runaway', CreaterunawayLetter.as_view(), name='CreaterunawayLetter'),
    path('letter/all/checkout', AllCheckoutLetter, name='AllCheckoutLetter'),
    path('letter/all/normal', AllNormalLetter, name='AllNormalLetter'),
    path('letter/p/checkout/<int:pk>', PrintCheckoutLetter, name='PrintCheckoutLetter'),
    path('letter/p/normall/register/<int:pk>', PrintRegisterLetter, name='PrintRegisterLetter'),
    path('letter/p/checkout/commission/<int:pk>', PrintCheckoutCommissionLetter, name='PrintCheckoutCommissionLetter'),
    path('letter/p/checkout/before/course/commission/<int:pk>', PrintBeforeCourseCommissionLetter,
         name='PrintBeforeCourseCommissionLetter'),
    path('letter/checkout/update_status/<int:pk>', check_status_checkout, name='status_ok_checkout'),
    path('letter/checkout/delete/<int:pk>', check_status_checkout, name='delete_checkout'),
    path('letter/p/normall/training/inquiry/<int:pk>', PrintTrainingInquiryLetter, name='PrintTrainingInquiryLetter'),
    path('letter/p/normall/runaway/<int:pk>', PrintRunawayLetterLetter, name='PrintRunawayLetterLetter'),
]
