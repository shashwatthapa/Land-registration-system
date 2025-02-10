from django.db import models
from django.core.exceptions import ValidationError
import uuid
from django.contrib.auth.models import User
from decimal import Decimal
# Create your models here.
class KYC(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    national_id = models.FileField(upload_to='kyc/national_ids/')
    phone_number = models.IntegerField()
    def __str__(self):
        return f'{self.user.username}'
    
class Property(models.Model):
    transaction_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=200,choices=[('Koshi','Koshi'),('Madhesh','Madhesh'),('Bagmati','Bagmati'),('Gandaki','Gandaki'),('Lumbini','Lumbini'),('Karnali','Karnali'),('Sudurpaschim','Sudurpaschim')])
    property_size = models.DecimalField(max_digits=10,decimal_places=2)
    property_value = models.DecimalField(max_digits=15,decimal_places=2)
    stamp_duty = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    sale_deed = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=20,choices=[('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected')],default='Pending')
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.stamp_duty = self.property_value * Decimal('0.05')  
        super().save(*args, **kwargs)
    def validate_pdf(value):
        if not value.name.endswith('.pdf'):
            raise ValidationError('Only PDF files are allowed.')

   

    def __str__(self):
        return f'{self.owner_name}--{self.address}'
        