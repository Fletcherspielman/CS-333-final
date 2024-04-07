import boto3
from django.conf import settings

def content_moderation(photo):
    client=boto3.client(
                        'rekognition',
                        aws_access_key_id= settings.AWS_CLIENT_KEY_ID,
                        aws_secret_access_key=settings.SECRET_CLIENT_KEY_REKOG
                        )

    with open(str(settings.BASE_DIR) + photo, 'rb') as image:
        response = client.detect_moderation_labels(Image={'Bytes': image.read()})
    for label in response['ModerationLabels']:
        if label['TaxonomyLevel'] == 1 and label['Confidence'] > 60:
            return False
    return True
    