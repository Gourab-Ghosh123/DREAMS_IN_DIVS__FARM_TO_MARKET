from django.db import models

from django.core.validators import MinValueValidator , MaxValueValidator
from communication.models import Farmer
from django.utils import timezone
import uuid

# Create your models here.


class Crop_Batch(models.Model):
    """The whole batch tracking from the farmer to the retialer...."""


    STAGE_CHOICES = [
        ('HARVESTED', 'Harvested on Farm'),
        ('COLLECTION_CENTER', 'At Collection Center'),
        ('IN_TRANSIT', 'In Transit'),
        ('WAREHOUSE', 'At Warehouse'),
        ('RETAILER', 'Delivered to Retailer'),
        ('COMPLETED', 'Completed'),
    ]


    CROP_CHOICES = [
        ('WHEAT', 'Wheat (गेहूं)'),
        ('RICE', 'Rice (चावल)'),
        ('TOMATO', 'Tomato (टमाटर)'),
        ('POTATO', 'Potato (आलू)'),
        ('ONION', 'Onion (प्याज)'),
        ('MANGO', 'Mango (आम)'),
        ('SUGARCANE', 'Sugarcane (गन्ना)'),
    ]
    
    batch_id = models.CharField(max_length=50 , unique=True)
    farmer = models.ForeignKey(Farmer , on_delete=models.CASCADE , related_name='batches')


    # Crop details....
    crop_type = models.CharField(max_length=20 , choices=CROP_CHOICES)
    quantity_kg = models.DecimalField(max_digits=10 , decimal_places=2 , validators=[MinValueValidator(0.01)])
    harvest_date = models.DateField()

    # Quality of our crop in grades....

    quality_grade = models.CharField(max_length=10, blank=True, null=True, choices=[
        ('A', 'Grade A - Premium'),
        ('B', 'Grade B - Good'),
        ('C', 'Grade C - Standard'),
    ])
    
    # status of the crop...

    current_status = models.CharField(max_length=30 , choices=STAGE_CHOICES , default='HARVESTED')

    # Qr code.....

    qr_code_url = models.URLField(blank=True , null=True)
    qr_code_image = models.ImageField(upload_to='qrcodes/' , blank=True , null=True)


    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    expected_at_centre = models.DateTimeField(blank=True , null=True)
    expected_at_warehouse = models.DateTimeField(blank=True , null=True)


    def save(self, *args, **kwargs):
        if not self.batch_id:
            # Generate BATCH20260410001 format
            date_str = timezone.now().strftime('%Y%m%d')
            last = Crop_Batch.objects.filter(batch_id__startswith=f'{self.crop_type}{date_str}').count()
            self.batch_id = f"{self.crop_type}{date_str}{last + 1:03d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.batch_id} - {self.crop_type} - {self.quantity_kg}kg"
    





 ####-------------------

    # Batch History....

class Batch_History(models.Model):

        batch = models.ForeignKey(Crop_Batch, on_delete=models.CASCADE, related_name='history')

        stage = models.CharField(max_length=30 , choices=Crop_Batch.STAGE_CHOICES)

        updated_by = models.CharField(max_length=100)  # The person who scanned...

        updated_by_role = models.CharField(max_length=50, choices=[
        ('FARMER', 'Farmer'),
        ('COLLECTION_CENTER', 'Collection Center Staff'),
        ('TRANSPORT', 'Transport Officer'),
        ('WAREHOUSE', 'Warehouse Manager'),
        ('RETAILER', 'Retailer'),
        ])
        
        location = models.CharField(max_length=200, blank=True, null=True)
        notes = models.TextField(blank=True, null=True)
        timestamp = models.DateTimeField(auto_now_add=True)


        class Meta:
            ordering = ['-timestamp']
    
        def __str__(self):
            return f"{self.batch.batch_id} - {self.stage} at {self.timestamp}"
        


class VoiceLog(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='voice_logs')
    batch = models.ForeignKey(Crop_Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='voice_logs')

    # From Twilio
    call_sid = models.CharField(max_length=100, blank=True)
    farmer_SpeechText = models.TextField(blank=True)   # same as ConversationTurn
    farmer_AudioURL = models.URLField(blank=True)
    ai_ResponseText = models.TextField(blank=True)
    ai_AudioURL = models.URLField(blank=True)

    extracted_data = models.JSONField(default=dict)   


    def __str__(self):
        return f"Call from {self.farmer.phone_number} at {self.created_at}"