from .models import GarbageLabel
import boto3

# Initialize AWS Rekognition client
rekognition = boto3.client('rekognition')

# Send image to AWS Rekognition and detect labels


def detect_labels(image_bytes_data: bytes, min_confidence: float = 85.0):
    if not isinstance(image_bytes_data, bytes):
        return False

    response = rekognition.detect_labels(
        Image={'Bytes': image_bytes_data},
        MinConfidence=min_confidence,
    )

    # filter confident labels
    labels = response['Labels']
    confident_labels = []
    for label in labels:
        if label['Confidence'] >= min_confidence:
            del label['Instances']
            del label['Parents']
            del label['Categories']
            confident_labels.append(label)
    return confident_labels


def classify_label(labels: list):
    # sort labels based on confidence level
    labels = sorted(labels, key=lambda x: x.get(
        'Confidence'), reverse=True)
    high_confidence_label = labels[0].get("Name")

    label_classification: GarbageLabel = GarbageLabel.objects.filter(
        label=high_confidence_label).last()

    if label_classification:
        msg = {
            'class': label_classification.label_class,
            'label': label_classification.label,
            'error': None,
        }
    else:
        # create new label in db with None class
        GarbageLabel(label=high_confidence_label).save()
        msg = {
            'class': None,
            'label': high_confidence_label,
            'error': f'{high_confidence_label} class is not classified. Add label class using admin page.'
        }
    return msg
