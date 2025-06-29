from django.urls import path
from .views import MedicoList ,UbsList, RegistrarPresenca

urlpatterns = [
    path('medicos/', MedicoList.as_view(), name='medico-list'),
    path('ubs/', UbsList.as_view(), name='ubs-list'),
    path('registrar-presenca', RegistrarPresenca.as_view(), name='presenca'),

]