# products/management/commands/seed_products.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Manufacturer, Product, ProductSpecification, ProductFitment
from vehicles.models import Vehicle
import random

class Command(BaseCommand):
    help = 'Seeds 50 car spare parts with fitments to existing vehicles'

    def handle(self, *args, **options):
        # Ensure vehicles exist
        if not Vehicle.objects.exists():
            self.stdout.write(self.style.ERROR("No vehicles found! Run 'seed_vehicles' first."))
            return

        # ===== CATEGORIES (with hierarchy) =====
        root_categories = ["Engine", "Brakes", "Suspension", "Filters", "Lighting"]
        subcategories = {
            "Engine": ["Oil Filters", "Spark Plugs", "Timing Belts"],
            "Brakes": ["Brake Pads", "Rotors", "Calipers"],
            "Suspension": ["Shock Absorbers", "Control Arms"],
            "Filters": ["Air Filters", "Cabin Filters", "Fuel Filters"],
            "Lighting": ["Headlights", "Tail Lights", "Bulbs"]
        }

        category_map = {}
        for root in root_categories:
            cat, _ = Category.objects.get_or_create(
                name=root,
                defaults={'slug': slugify(root)}
            )
            category_map[root] = cat

        for parent_name, subs in subcategories.items():
            parent = category_map[parent_name]
            for sub in subs:
                Category.objects.get_or_create(
                    name=sub,
                    parent=parent,
                    defaults={'slug': slugify(sub)}
                )

        all_categories = list(Category.objects.filter(parent__isnull=False))  # use leaf categories

        # ===== MANUFACTURERS =====
        manufacturer_names = ["Bosch", "NGK", "ACDelco", "Denso", "Mobil 1", "Fram", "KYB", "EBC Brakes"]
        manufacturers = []
        for name in manufacturer_names:
            manu, _ = Manufacturer.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            manufacturers.append(manu)

        # ===== PRODUCTS DATA =====
        product_templates = [
            ("Premium Oil Filter", "High-efficiency engine oil filter", "Filters", "Oil Filters"),
            ("Ceramic Brake Pads", "Long-lasting ceramic brake pads", "Brakes", "Brake Pads"),
            ("Double Platinum Spark Plug", "Improved ignition performance", "Engine", "Spark Plugs"),
            ("Air Filter Panel", "Reusable high-flow air filter", "Filters", "Air Filters"),
            ("Front Shock Absorber", "Gas-charged shock for smooth ride", "Suspension", "Shock Absorbers"),
            ("Halogen Headlight Bulb", "Bright white 55W headlight bulb", "Lighting", "Bulbs"),
            ("Timing Belt Kit", "Complete kit with tensioner", "Engine", "Timing Belts"),
            ("Disc Brake Rotor", "Drilled and slotted for performance", "Brakes", "Rotors"),
            ("Cabin Air Filter", "Activated carbon for odor reduction", "Filters", "Cabin Filters"),
            ("Control Arm Assembly", "Includes ball joint and bushings", "Suspension", "Control Arms"),
        ]

        # Get all vehicles for fitment
        vehicles = list(Vehicle.objects.all())
        if len(vehicles) < 10:
            self.stdout.write(self.style.WARNING("Fewer than 10 vehicles found — fitments may repeat."))

        created_count = 0
        while created_count < 50:
            # Pick a template
            title_base, desc, root_cat, sub_cat = random.choice(product_templates)
            suffix = f"{random.randint(100, 999)}"
            title = f"{title_base} {suffix}"
            sku = f"SPARE-{created_count + 1:03d}"
            part_number = f"PN{random.randint(10000, 99999)}"

            # Find category
            try:
                category = Category.objects.get(name=sub_cat)
            except Category.DoesNotExist:
                category = Category.objects.filter(parent__isnull=False).first()

            # Create product
            product = Product.objects.create(
                title=title,
                sku=sku,
                description=f"{desc}. Model: {title_base}.",
                unit_price=round(random.uniform(15.0, 250.0), 2),
                cost_price=round(random.uniform(8.0, 120.0), 2),
                inventory=random.randint(5, 200),
                category=category,
                manufacturer=random.choice(manufacturers),
                part_number=part_number,
                oem_part_number=f"OEM{random.randint(1000, 9999)}",
                product_type=random.choice(['AFT', 'PER', 'OEM']),
                is_universal=False,
                warranty_months=random.choice([12, 24, 36])
            )

            # Add specifications
            spec_sets = {
                "Oil Filter": [("Thread Size", "3/4-16", ""), ("Height", "85", "mm"), ("Filter Media", "Synthetic", "")],
                "Brake Pads": [("Thickness", "18", "mm"), ("Material", "Ceramic", ""), ("Set Includes", "4 Pads", "")],
                "Spark Plug": [("Gap", "0.044", "in"), ("Thread", "14mm", ""), ("Heat Range", "7", "")],
                "Air Filter": [("Dimensions", "250x180x30", "mm"), ("Filter Type", "Panel", ""), ("Reusable", "Yes", "")],
                "Shock Absorber": [("Extended Length", "520", "mm"), ("Compressed Length", "340", "mm"), ("Mount Type", "Eye/Eye", "")],
                "Bulb": [("Wattage", "55/60", "W"), ("Voltage", "12", "V"), ("Base Type", "H4", "")],
                "Timing Belt": [("Length", "1200", "mm"), ("Width", "25", "mm"), ("Teeth", "150", "")],
                "Rotor": [("Diameter", "320", "mm"), ("Thickness", "28", "mm"), ("Hat Height", "65", "mm")],
                "Cabin Filter": [("Dimensions", "200x150x20", "mm"), ("Filter Type", "Activated Carbon", ""), ("Replacement Interval", "12000", "miles")],
                "Control Arm": [("Material", "Forged Steel", ""), ("Bushings Included", "Yes", ""), ("Ball Joint Included", "Yes", "")]
            }

            base_type = title_base.split()[0]
            specs = []
            for key in spec_sets:
                if key in title_base:
                    specs = spec_sets[key]
                    break
            if not specs:
                specs = [("Generic Spec", "Value", "")]

            for name, value, unit in specs:
                ProductSpecification.objects.create(
                    product=product,
                    name=name,
                    value=value,
                    unit=unit
                )

            # Add fitments (1 to 3 vehicles)
            num_fitments = random.randint(1, min(3, len(vehicles)))
            selected_vehicles = random.sample(vehicles, num_fitments)
            positions = ["Front", "Rear", "Left", "Right", ""]
            for veh in selected_vehicles:
                ProductFitment.objects.create(
                    product=product,
                    vehicle=veh,
                    position=random.choice(positions),
                    fitment_notes=random.choice([
                        "",
                        "Direct replacement",
                        "May require minor modification",
                        "Check clearance before installation"
                    ])
                )

            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created 50 car spare parts with fitments!')
        )