from django.contrib import admin
from .models import Ubs, Medico, Endereco,Vinculo

class UBSAdmin(admin.ModelAdmin):
    readonly_fields = ['usuario']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Exibe apenas os objetos do usuário logado
        return qs.filter(usuario=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True  # necessário para mostrar a lista
        return obj.usuario == request.user

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True  # necessário para mostrar a lista
        return obj.usuario == request.user

    def save_model(self, request, obj, form, change):
        if not change or not obj.usuario:
            obj.usuario = request.user
        obj.save()

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields = [f for f in fields if f != 'usuario']
        return fields

admin.site.register(Ubs, UBSAdmin)
admin.site.register(Medico)
admin.site.register(Endereco)
admin.site.register(Vinculo)