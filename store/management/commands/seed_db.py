from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth import get_user_model
from store.models import Category, Product, Order, OrderItem
import os
import shutil
from decimal import Decimal
from PIL import Image, ImageDraw

User = get_user_model()

class Command(BaseCommand):
    help = 'Clear existing database and seed it with dummy data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        
        # 1. Clear database
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

        # 2. Re-create media products folder
        media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        if os.path.exists(media_products_dir):
            self.stdout.write(f'Cleaning up media folder: {media_products_dir}')
            shutil.rmtree(media_products_dir)
        os.makedirs(media_products_dir, exist_ok=True)

        self.stdout.write('Creating dummy data...')

        # Helper to generate themed dummy images
        def generate_dummy_image(category_name, product_name):
            filename = f"{slugify(category_name)}_{slugify(product_name)}.jpg"
            file_path = os.path.join(media_products_dir, filename)
            
            # Curated flat colors for each category
            colors = {
                'electronics': (41, 128, 185), # Blue
                'groceries': (39, 174, 96),     # Green
                'clothing': (155, 89, 182),     # Purple
                'home-decor': (230, 126, 34),   # Orange
                'books': (241, 196, 15)         # Yellow
            }
            color = colors.get(slugify(category_name), (127, 140, 141)) # Default gray
            
            # Create a 300x300 image
            img = Image.new('RGB', (300, 300), color=color)
            draw = ImageDraw.Draw(img)
            
            # Draw a nice layout (white borders, geometric shape)
            draw.rectangle([15, 15, 285, 285], outline=(255, 255, 255), width=2)
            draw.ellipse([80, 80, 220, 220], outline=(255, 255, 255), width=2)
            
            img.save(file_path, 'JPEG')
            return f"products/{filename}"

        # 3. Create users
        # Create Superuser
        superuser = User.objects.create_superuser(
            username='admin',
            mobile='9999999999',
            email='admin@example.com',
            password='admin123'
        )
        self.stdout.write('Created superuser: admin (9999999999) / admin123')

        # Create Normal Users
        user1 = User.objects.create_user(
            username='John Doe',
            mobile='1234567890',
            email='john@example.com',
            password='user123'
        )
        user2 = User.objects.create_user(
            username='Jane Smith',
            mobile='9876543210',
            email='jane@example.com',
            password='user123'
        )
        self.stdout.write('Created test users: 1234567890 / user123 and 9876543210 / user123')

        # 4. Categories & Products Data
        data = {
            'Electronics': [
                ('Smartphone', 19999.00, "A powerful smartphone with a crystal-clear display and long-lasting battery."),
                ('Laptop', 54999.00, "Lightweight and powerful laptop suitable for productivity and creative tasks."),
                ('Wireless Headphones', 2999.00, "Noise-cancelling wireless headphones with deep bass and high fidelity."),
                ('Smart Watch', 4999.00, "Track your fitness, heart rate, and notifications on the go."),
                ('Bluetooth Speaker', 1899.00, "Portable waterproof speaker with crystal clear sound.")
            ],
            'Groceries': [
                ('Organic Honey', 350.00, "Pure, raw, organic honey harvested from local farms."),
                ('Premium Green Tea', 220.00, "Refreshing green tea leaves packed with antioxidants."),
                ('Roasted Almonds', 450.00, "Crunchy and delicious lightly salted roasted almonds."),
                ('Oats Breakfast Cereal', 180.00, "Whole grain oats, perfect for a healthy start to your day."),
                ('Extra Virgin Olive Oil', 850.00, "Cold-pressed extra virgin olive oil for gourmet cooking.")
            ],
            'Clothing': [
                ('Classic T-Shirt', 599.00, "100% cotton classic fit crewneck t-shirt."),
                ('Slim Fit Jeans', 1499.00, "Comfortable slim-fit denim jeans with dynamic stretch."),
                ('Winter Jacket', 2999.00, "Warm and stylish insulated jacket for cold weather."),
                ('Athletic Socks', 299.00, "Pack of 3 breathable cotton athletic crew socks."),
                ('Baseball Cap', 399.00, "Adjustable cotton cap with classic curved brim.")
            ],
            'Home Decor': [
                ('Ceramic Vase', 799.00, "Elegant hand-crafted ceramic vase for modern living rooms."),
                ('LED Desk Lamp', 1299.00, "Dimmable eye-caring LED desk lamp with USB charging port."),
                ('Modern Wall Clock', 999.00, "Minimalist silent wall clock with clean wooden styling."),
                ('Decorative Cushion', 450.00, "Soft textured throw pillow cushion cover with insert."),
                ('Scented Candle Set', 650.00, "Aroma therapeutic soy wax scented candles in glass jars.")
            ],
            'Books': [
                ('Science Fiction Novel', 399.00, "A thrilling journey through space, time, and human evolution."),
                ('Biography of an Innovator', 499.00, "The inspiring life story of one of the greatest minds of the century."),
                ('Learn Python Programming', 799.00, "A comprehensive guide to coding with Python for absolute beginners."),
                ('Detective Mystery Book', 350.00, "A suspenseful whodunit thriller that will keep you guessing."),
                ('Visual Art History', 1200.00, "A beautiful coffee table book tracing the evolution of visual arts.")
            ]
        }

        # Save categories and products
        products_map = {}
        for cat_name, items in data.items():
            category = Category.objects.create(name=cat_name)
            self.stdout.write(f'Created Category: {cat_name}')
            
            for prod_name, price, desc in items:
                image_relative_path = generate_dummy_image(cat_name, prod_name)
                product = Product.objects.create(
                    name=prod_name,
                    price=Decimal(price),
                    description=desc,
                    image=image_relative_path,
                    category=category
                )
                products_map[prod_name] = product
                self.stdout.write(f'  Created Product: {prod_name} (INR {price})')

        # 5. Create Dummy Orders
        # Order 1 for John Doe (User 1)
        order1 = Order.objects.create(user=user1)
        OrderItem.objects.create(order=order1, product=products_map['Smartphone'], quantity=1)
        OrderItem.objects.create(order=order1, product=products_map['Organic Honey'], quantity=2)
        
        # Order 2 for Jane Smith (User 2)
        order2 = Order.objects.create(user=user2)
        OrderItem.objects.create(order=order2, product=products_map['Classic T-Shirt'], quantity=2)
        OrderItem.objects.create(order=order2, product=products_map['Learn Python Programming'], quantity=1)
        OrderItem.objects.create(order=order2, product=products_map['Modern Wall Clock'], quantity=1)

        self.stdout.write(self.style.SUCCESS('Database successfully seeded with dummy data!'))
