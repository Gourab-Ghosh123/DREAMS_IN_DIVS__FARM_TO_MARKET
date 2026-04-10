import requests
import boto3
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import uuid

class SpeechService:

    @staticmethod
    def text_to_speech(text , language='hi'):
        """this converts text to speech using Hindi
        """

        # Amazon Polly
        polly = boto3.client('polly',
                aws_access_key_id=settings.AWS,
                             )