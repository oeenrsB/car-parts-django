from django.core.management.base import BaseCommand
from django.utils.text import slugify
from vehicles.models import Make, Model, Vehicle
import random

class Command(BaseCommand):
    help = 'Seeds the database with 50 realistic vehicle records'

    def handle(self, *args, **options):
        # Define data
        makes_data = ["Toyota", "Honda", "Ford", "Chevrolet", "BMW", "Audi", "Mercedes-Benz", "Nissan", "Volkswagen", "Hyundai"]
        models_by_make = {
            "Toyota": ["Camry", "Corolla"],
            "Honda": ["Civic", "Accord"],
            "Ford": ["F-150", "Mustang"],
            "Chevrolet": ["Silverado", "Malibu"],
            "BMW": ["3 Series", "X5"],
            "Audi": ["A4", "Q5"],
            "Mercedes-Benz": ["C-Class", "GLC"],
            "Nissan": ["Altima", "Rogue"],
            "Volkswagen": ["Jetta", "Atlas"],
            "Hyundai": ["Elantra", "Tucson"]
        }
        trims = ["Base", "LE", "Sport", "Limited"]
        engines = ["2.0L I4", "3.5L V6", "2.0L Turbo"]
        body_types = ["Sedan", "SUV", "Truck"]

        # Create Makes
        make_objs = {}
        for name in makes_data:
            make, _ = Make.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            make_objs[name] = make

        # Create Models
        model_objs = []
        for make_name, model_names in models_by_make.items():
            for model_name in model_names:
                model, _ = Model.objects.get_or_create(
                    make=make_objs[make_name],
                    name=model_name,
                    defaults={'slug': slugify(f"{make_name} {model_name}")}
                )
                model_objs.append(model)

        # Create 50 Vehicles
        years = list(range(2020, 2025))
        count = 0
        while count < 50:
            model = random.choice(model_objs)
            year = random.choice(years)
            trim = random.choice(trims)
            if not Vehicle.objects.filter(model=model, year=year, trim=trim).exists():
                Vehicle.objects.create(
                    model=model,
                    year=year,
                    trim=trim,
                    engine=random.choice(engines),
                    body_type=random.choice(body_types)
                )
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} Vehicle records!')
        )