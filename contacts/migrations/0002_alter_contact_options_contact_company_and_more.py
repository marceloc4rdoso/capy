# Generated by Django 5.2.4 on 2025-07-20 16:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contacts", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="contact",
            options={
                "ordering": ["name"],
                "verbose_name": "Contato",
                "verbose_name_plural": "Contatos",
            },
        ),
        migrations.AddField(
            model_name="contact",
            name="company",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"person_type": "PJ"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="contacts.contact",
                verbose_name="Empresa Associada (PJ)",
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="document",
            field=models.CharField(
                blank=True,
                max_length=18,
                null=True,
                unique=True,
                verbose_name="CPF/CNPJ",
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Ativo"),
        ),
        migrations.AddField(
            model_name="contact",
            name="person_type",
            field=models.CharField(
                choices=[("PF", "Pessoa Física"), ("PJ", "Pessoa Jurídica")],
                default="PF",
                max_length=2,
                verbose_name="Tipo de Pessoa",
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="contact",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Usuário Associado",
            ),
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type_address",
                    models.CharField(
                        choices=[
                            ("residential", "Residencial"),
                            ("commercial", "Comercial"),
                            ("billing", "Cobrança"),
                            ("shipping", "Entrega"),
                        ],
                        default="Comercial",
                        max_length=50,
                        verbose_name="Tipo de Endereço",
                    ),
                ),
                ("street", models.CharField(max_length=255, verbose_name="Logradouro")),
                ("number", models.CharField(max_length=20, verbose_name="Número")),
                (
                    "complement",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Complemento",
                    ),
                ),
                (
                    "neighborhood",
                    models.CharField(max_length=100, verbose_name="Bairro"),
                ),
                ("city", models.CharField(max_length=100, verbose_name="Cidade")),
                ("state", models.CharField(max_length=2, verbose_name="UF")),
                ("zip_code", models.CharField(max_length=9, verbose_name="CEP")),
                (
                    "country",
                    models.CharField(
                        default="Brasil", max_length=50, verbose_name="País"
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="addresses",
                        to="contacts.contact",
                    ),
                ),
            ],
            options={
                "verbose_name": "Endereço",
                "verbose_name_plural": "Endereços",
                "ordering": ["type_address", "city", "neighborhood"],
            },
        ),
    ]
