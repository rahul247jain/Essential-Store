from django.db import models
from shop.models import Product
ZONE_CHOICES = (
    ('RED ZONE', 'R'),
    ('ORANGE ZONE', 'O'),
    ('GREEN ZONE', 'G')
)
CITY_CHOICES = (
    ('Ahmedabad', 'Ahmedabad'),
    ('Bengaluru', 'Bengaluru'),
    ('Chennai', 'Chennai'),
    ('Chittorgarh', 'Chittorgarh'),
    ('Jodhpur', 'Jodhpur'),
    ('Raipur', 'Raipur'),
    ('Sirohi', 'Sirohi'),
    ('Pali', 'Pali'),
    ('Delhi', 'Delhi'),
    ('Hyderabad', 'Hyderabad'),
    ('Kanpur', 'Kanpur'),
    ('Kolkata', 'Kolkata'),
    ('Mumbai', 'Mumbai'),
    ('Ratnagiri', 'Ratnagiri'),
    ('Pune', 'Pune'),
    ('Surat', 'Surat'),
    ('Sultanpur', 'Sultanpur'),
    ('Lucknow', 'Lucknow'),
    ('Patna', 'Patna'),
    ('Indore', 'Indore'),
    ('Vadodara', 'Vadodara'),
    ('Bhopal', 'Bhopal'),
    ('Coimbatore', 'Coimbatore'),
    ('Agra', 'Agra'),
    ('Meerut', 'Meerut'),
    ('Madurai', 'Madurai'),
    ('Guwahati', 'Guwahati'),
    ('Thiruvananthapuram', 'Thiruvananthapuram'),
    ('Tiruchchirappalli', 'Tiruchchirappalli'),
    ('Kota', 'Kota'),
    ('Jammu', 'Jammu'),
    ('Mangalore', 'Mangalore'),
    ('Ajmer', 'Ajmer'),
    ('Shillong', 'Shillong'),
    ('New Delhi', 'New Delhi')
)

# Create your models here.
class Warehouse(models.Model):
    location = models.CharField(max_length=100,choices=CITY_CHOICES, null=True)
    zone = models.CharField(max_length=30, choices=ZONE_CHOICES, null=True)
    loc_x = models.DecimalField(max_digits=10, decimal_places=6)
    loc_y = models.DecimalField(max_digits=10, decimal_places=6)

class KeyVal(models.Model):
    locname = models.ForeignKey(Warehouse,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)