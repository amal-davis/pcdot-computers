from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _




# Create your models here.



class ProductType(models.Model):
    name = models.CharField(_('name'), max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    heading = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.heading)
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_page', kwargs={'slug': self.slug})

    def get_stock_status(self):
        if self.stock == 0:
            return 'Out of Stock'
        elif self.stock < 5:
            return 'Limited Stock'
        else:
            return 'In Stock'

    def decrease_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
        else:
            raise ValueError("Not enough stock available")
    

    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_images/')


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True)
    phone_number = models.CharField(max_length=20)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    


    @property
    def total_price(self):
        return self.quantity * self.product.price

    def update_quantity(self, quantity):
        self.quantity = quantity
        self.save()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.heading}"
    
class Video(models.Model):
    product = models.ForeignKey(Product, related_name='videos', on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='product_videos/')
    created_at = models.DateTimeField(default=timezone.now)  # Add this line


class ClientLogo(models.Model):
    image = models.ImageField(upload_to='client_logos/')  # Image upload location
    alt_text = models.CharField(max_length=255, default='Client Logo')  # Alt text for accessibility

    def __str__(self):
        return self.alt_text
    


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # Add status field
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"{self.quantity} x {self.product.heading}"


class DesktopCarouselImage(models.Model):
    image = models.ImageField(upload_to='desktop_carousel_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.alt_text or 'Desktop Carousel Image'

class MobileCarouselImage(models.Model):
    image = models.ImageField(upload_to='mobile_carousel_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.alt_text or 'Mobile Carousel Image' 



class Links(models.Model):
    name = models.CharField(_('name'), max_length=255)
    website = models.URLField(max_length=200, blank=True, null=True)
