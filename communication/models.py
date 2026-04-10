from django.db import models

# Create your models here.

class Farmer(models.Model):
    phone_number = models.CharField(max_length=20 , unique=True)
    name = models.CharField(max_length=100 , blank=True)
    preferred_language = models.CharField(max_length=10 , default='hi') # default as hindi...

    village = models.CharField(max_length=100 , blank = True)
    district = models.CharField(max_length=100 , blank = True)
    state = models.CharField(max_length=100 , blank = True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.preferred_language}"
    


class Conversation(models.Model):
    farmer = models.ForeignKey(Farmer , on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now_add=True)
    duration_seconds = models.IntegerField(null=True , blank=True)

    def __str__(self):
        return f"Conversation with {self.farmer.phone_number} at {self.started_at}"
    


class ConversationTurn(models.Model):
    conversation = models.ForeignKey(Conversation , on_delete=models.CASCADE)
    turn_number = models.IntegerField()

    #Farmer side monologues...
    farmer_SpeechText = models.TextField(blank=True) # we store the transcribed text of the farmer...
    farmer_AudioURL = models.URLField(blank=True)  # Record of the Farmer's voice...

    #Ai responses...
    ai_ResponseText = models.TextField(blank=True)
    ai_AudioURL = models.URLField(blank=True)

    language_detected = models.CharField(max_length=10 , blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['turn_number'] # sorts the conco turns of the farmer and our AI...