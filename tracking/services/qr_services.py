import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from io import BytesIO
import base64
from django.core.files.base import ContentFile
from django.conf import settings
import uuid
import json


class QRService:


    @staticmethod
    def generate_batch_for_batch(batch):
        """Generated QR code containing batch ID and basic info"""

        # Date to encode in QR...


        # Data to encode to QR...
        qr_data = {
            'batch_id': batch.batch_id,
            'crop': batch.crop_type,
            'farmer_name': batch.farmer.name,
            'url': f"{settings.BASE_URL}/trace/batch/{batch.batch_id}/"

        }

        # Convert to JSon string....
        qr_json = json.dumps(qr_data)

        # Create QR code with styling(better for hackathon)
        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(qr_json)


        qr.make(fit = True)

        # Create styled image...
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color="#2E7D32",  # For Agriculture green
            back_color="white"
        )

        # SAved in bytes IO
        buffer = BytesIO()
        img.save(buffer , format='PNG')
        buffer.seek(0)


        # SAved to Django's storage...
        filename = f"qr_codes/{batch.batch_id}.png"
        batch.qr_code_image.save(filename , ContentFile(buffer.getvalue() , save=False))

        # also storing the qr URL....
        batch.qr_code_url = f"{settings.MEDIA_URL}{filename}"
        batch.save()

        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        return{
            'image_url' : batch.qr_code_url,
            'base64' : img_base64
        }