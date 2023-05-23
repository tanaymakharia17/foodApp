from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    extension = os.path.splitext(value.name)[1]
    print(extension)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not extension.lower() in valid_extensions:
        raise ValidationError('Unsupported file extensions. Allowed files: ' +str(valid_extensions))