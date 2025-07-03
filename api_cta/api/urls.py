from django.urls import path
from .views import MedicoList ,UbsList, BuscarVinculosAPIView, MarcarPresencaAPIView

urlpatterns = [
    path('medicos/', MedicoList.as_view(), name='medico-list'),
    path('ubs/', UbsList.as_view(), name='ubs-list'),
    path('buscar-vinculo/', BuscarVinculosAPIView.as_view(), name='vinculos'),
    path('marcar-presenca/',MarcarPresencaAPIView.as_view(),name='presenca'),

]