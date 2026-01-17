# orders/management/commands/seed_orders.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from orders.models import Order, OrderItem
from customers.models import Customer, Address
from products.models import Product
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds 100 realistic orders with order items'

    def handle(self, *args, **options):
        # Check dependencies
        if not Customer.objects.exists():
            self.stdout.write(self.style.ERROR("No customers found! Run 'seed_customers' first."))
            return
        if not Product.objects.exists():
            self.stdout.write(self.style.ERROR("No products found! Run 'seed_products' first."))
            return

        customers = list(Customer.objects.all())
        products = list(Product.objects.all())

        # Order statuses and payment statuses
        order_statuses = ['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED']
        payment_statuses = ['P', 'C', 'F', 'R']
        shipping_methods = ['Standard', 'Express', 'Next Day']
        shipping_costs = [0.00, 9.99, 14.99, 19.99]

        self.stdout.write("Creating 100 orders...")

        for i in range(100):
            # Pick a customer and one of their addresses
            customer = random.choice(customers)
            try:
                address = random.choice(list(customer.addresses.all()))
            except IndexError:
                # Fallback: skip if no address (shouldn't happen if seeded properly)
                continue

            # Generate unique order number
            order_number = f"ORD-{timezone.now().strftime('%Y%m%d')}-{1000 + i}"

            # Random dates
            placed_at = timezone.now() - timedelta(days=random.randint(0, 90))  # up to 3 months ago
            shipped_at = None
            delivered_at = None

            order_status = random.choices(
                order_statuses,
                weights=[1, 2, 3, 4, 1],  # more delivered, fewer cancelled
                k=1
            )[0]

            if order_status == 'SHIPPED':
                shipped_at = placed_at + timedelta(days=random.randint(1, 5))
            elif order_status == 'DELIVERED':
                shipped_at = placed_at + timedelta(days=random.randint(1, 5))
                delivered_at = shipped_at + timedelta(days=random.randint(1, 7))

            payment_status = 'C' if order_status in ['SHIPPED', 'DELIVERED'] else random.choice(payment_statuses)

            # Create order
            order = Order.objects.create(
                customer=customer,
                shipping_address=address,
                order_number=order_number,
                placed_at=placed_at,
                payment_status=payment_status,
                order_status=order_status,
                shipping_method=random.choice(shipping_methods),
                shipping_cost=random.choice(shipping_costs),
                tracking_number=f"TRK{random.randint(1000000000, 9999999999)}" if order_status != 'CANCELLED' else "",
                shipped_at=shipped_at,
                delivered_at=delivered_at,
                customer_notes=random.choice([
                    "",
                    "Please leave at front door",
                    "Call before delivery",
                    "Gift wrap if possible"
                ]),
                admin_notes=random.choice([
                    "",
                    "VIP customer",
                    "Frequent buyer",
                    "Handle with care"
                ])
            )

            # Add 1–5 order items
            num_items = random.randint(1, 5)
            selected_products = random.sample(products, min(num_items, len(products)))
            for product in selected_products:
                quantity = random.randint(1, 3)
                # Use current product price or fallback
                unit_price = product.unit_price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully created 100 orders with order items!')
        )