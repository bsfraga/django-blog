from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError

#import valida_cpf


class Perfil(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    idade = models.PositiveIntegerField()
    data_nascimento = models.DateField()
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        default='Selecione',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        ))

    def __str__(self):
        return f'{self.usuario}'

    def clean(self):
        error_message = {}

        usuario_enviado = self.usuario or None
        usuario_salvo = None
        perfil = Perfil.objects.filter(usuario=usuario_enviado).first()

        if perfil:
            usuario_salvo = perfil.usuario

            if usuario_salvo is not None and self.pk != perfil.pk:
                error_message['usuario'] = 'Usuário já existe.'

        if error_message:
            raise ValidationError(error_message)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
