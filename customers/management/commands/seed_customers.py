# customers/management/commands/seed_customers.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from customers.models import Customer, Address, CustomerVehicle
from vehicles.models import Vehicle
import random
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds 50 customers with addresses and saved vehicles'

    def handle(self, *args, **options):
        # Check dependencies
        if not Vehicle.objects.exists():
            self.stdout.write(self.style.ERROR("No vehicles found! Run 'seed_vehicles' first."))
            return

        fake = Faker()
        vehicles = list(Vehicle.objects.all())
        memberships = ['R', 'S', 'G', 'P']
        cities = ["Cairo", "Alexandria", "Giza", "Sharm El Sheikh", "Luxor", "Aswan", "Hurghada"]
        streets_base = ["Nile St", "Tahrir St", "Pyramids Rd", "Corniche Rd", "Airport Rd"]

        self.stdout.write("Creating 50 customers...")

        for i in range(50):
            # Generate unique username/email
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}.{i+1}"
            email = f"{username}@example.com"

            # Create User
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'password': 'pbkdf2_sha256$600000$...dummy_hash...'  # won't be used for login
                }
            )
            if not created:
                continue  # skip if already exists

            # Set a real password (optional, for testing login)
            user.set_password('customer123')
            user.save()

            # Create Customer
            customer = Customer.objects.create(
                user=user,
                phone=f"+2010{random.randint(10000000, 99999999)}",
                email=email,
                membership=random.choice(memberships)
            )

            # Create 1-2 Addresses
            num_addresses = random.randint(1, 2)
            for j in range(num_addresses):
                is_default = (j == 0)
                street = f"{random.randint(1, 200)} {random.choice(streets_base)}"
                city = random.choice(cities)
                Address.objects.create(
                    customer=customer,
                    street=street,
                    city=city,
                    is_default=is_default
                )

            # Link 1-3 Vehicles to customer's garage
            num_vehicles = random.randint(1, min(3, len(vehicles)))
            selected_vehicles = random.sample(vehicles, num_vehicles)
            for idx, vehicle in enumerate(selected_vehicles):
                CustomerVehicle.objects.create(
                    customer=customer,
                    vehicle=vehicle,
                    nickname=f"My {vehicle.model.name}" if idx == 0 else "",
                    is_primary=(idx == 0),
                    vin=f"VIN{random.randint(10000000000000000, 99999999999999999)}"[:17],
                    mileage=random.randint(5000, 150000) if random.random() > 0.2 else None,
                    purchase_date=fake.date_between(start_date='-5y', end_date='today') if random.random() > 0.3 else None
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully created 50 customers with addresses and vehicles!')
        )