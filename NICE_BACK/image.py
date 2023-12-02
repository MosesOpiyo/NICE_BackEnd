from django.core.files import File
from io import BytesIO
from PIL import Image

def compress_image(image):
    img = Image.open(image)
    # Perform compression or other image processing here
    # Example: Resize the image to a maximum size of 1024x1024 pixels
    img.thumbnail((1024, 1024))
    # Save the compressed image to a BytesIO buffer
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    return img