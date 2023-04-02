import boto3

# Initialize AWS Rekognition client
rekognition = boto3.client('rekognition')

# Send image to AWS Rekognition and detect labels
def detect_labels(image_bytes_data:bytes, min_confidence:float=85.0):
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