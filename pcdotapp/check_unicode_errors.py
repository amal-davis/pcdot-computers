from django.core.management.base import BaseCommand
from modeltranslation.utils import get_translation_fields
from pcdotapp import models
from pcdotapp.models import Product, ProductType, Category

class Command(BaseCommand):
    help = 'Check for UnicodeDecodeError in translated fields of Product, ProductType, and Category models'

    def handle(self, *args, **kwargs):
        models_to_check = [Product, ProductType, Category]

        for model in models_to_check:
            for obj in model.objects.all():
                for field in obj._meta.fields:
                    if isinstance(field, (models.CharField, models.TextField)):
                        value = getattr(obj, field.name)
                        if value is not None:
                            try:
                                value.encode('utf-8')
                            except UnicodeDecodeError:
                                self.stdout.write(self.style.ERROR(f"Unicode error in {model.__name__} id {obj.id} field {field.name}"))

                # Check translated fields
                translation_fields = get_translation_fields(model)
                for field_name in translation_fields:
                    value = getattr(obj, field_name)
                    if value is not None:
                        try:
                            value.encode('utf-8')
                        except UnicodeDecodeError:
                            self.stdout.write(self.style.ERROR(f"Unicode error in {model.__name__} id {obj.id} field {field_name}"))
