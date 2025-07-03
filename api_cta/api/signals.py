from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Ubs, Vinculo

@receiver(m2m_changed, sender=Ubs.medicos.through)
def criar_vinculo_automaticamente(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for medico_id in pk_set:
            Vinculo.objects.get_or_create(
                medico_id=medico_id,
                ubs=instance,
                defaults={'status': 'Ausente'}
            )
