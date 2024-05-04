from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    images = models.ImageField(upload_to='app/category',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Carousel(models.Model):
    images = models.ImageField(upload_to='app/carousel',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

CATEGORY_CHOICES=(
    ('M', 'Mobile'),
    ('G', 'Grocery'),
    ('F', 'Fashion'),
    ('E', 'Electronic'),
    ('F', 'Furniture'),
    ('A', 'Appliances')
)
class Product(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    dicounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    images = models.ImageField(upload_to='app/product',null=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.brand

indian_states_tuple = (
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Puducherry', 'Puducherry'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal')
)
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.IntegerField(default=0)
    locality = models.CharField(max_length=100)
    cities = models.CharField(max_length=100)
    state = models.CharField(choices=indian_states_tuple,max_length=50)
    zipcode = models.IntegerField()
    def __str__(self):
        return str(self.id)
    
choice = (
    (1,"Read"),
    (2,"Unread")
)
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=20,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    status = models.IntegerField(choices=choice,default=2)
    created = models.DateField(auto_now_add=True)
    updated= models.DateField(auto_now=True)
    def __str__(self):
        return self.user.username
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
    @property
    def totalCost(self):
        return self.quantity * self.product.dicounted_price
    
order_status = (
    (1,'Pending'),
    (2,'Accepted'),
    (3,'Dispatch'),
    (4,'On the way'),
    (5,'Delivered'),
    (6,'Cancel'),
    (7,'Return')
)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.IntegerField(choices=order_status, default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    orderNo = models.PositiveIntegerField(default=16000, unique=True)  # Starting from 16000
    delivery_date = models.DateTimeField(null=True, blank=True)  # Nullable delivery date

    def save(self, *args, **kwargs):
        # Automatically generate unique order number starting from 16000
        if not self.pk:
            latest_booking = Booking.objects.order_by('-orderNo').first()
            if latest_booking:
                self.orderNo = latest_booking.orderNo + 1

        # Ensure created is timezone-aware and has a value
        if not self.created:
            self.created = timezone.now()

        # Set delivery date to be 48 hours from the creation time
        if not self.delivery_date:
            self.delivery_date = self.created + timedelta(days=2)

        super().save(*args, **kwargs)
    def __str__(self):
        return f"Order {self.orderNo}"
    @property
    def totalCost(self):
        return self.quantity * self.product.dicounted_price 
    

    

