print ('starting....')
try:
    import unzip_requirements
except ImportError:
    pass
import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image

import boto3
import os
import tarfile
import io
import base64
import json
import requests
from requests_toolbelt.multipart import decoder
print ('import end...')

S3_BUCKET = os.environ['S3_BUCKET'] if 'S3_BUCKET' in os.environ else 'draj-models'
MODEL_PATH = os.environ['MODEL_PATH'] if 'MODEL_PATH' in os.environ else 'mobilenet_v2.pt'

print (S3_BUCKET)
print (MODEL_PATH)
s3 = boto3.client('s3')

def load_model_from_s3():
    try:
	# get object from s3
        obj = s3.get_object(Bucket=S3_BUCKET, Key=MODEL_PATH)
        print (obj)
        print (type (obj))
	# read it in memory
        print ('creating bytestream')
        bytestream = io.BytesIO(obj['Body'].read())
        print ('loading model')
        model = torch.jit.load (bytestream)
        return model
    except Exception as e:
        print (e)
        raise(e)

print ('downloading model')
model = load_model_from_s3()
classes = requests.get ('https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json').json ()
classes = {int(key) : value[1] for key, value in classes.items ()}

def transform_image(image_bytes):
    try:
        transformations = transforms.Compose([
            transforms.Resize(255),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
        image = Image.open(io.BytesIO(image_bytes))
        return transformations(image).unsqueeze(0)
    except Exception as e:
        print(repr(e))
        raise(e)

def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    return model(tensor).argmax().item()

def classify_image (event, context):
    try:
        content_type_header = event['headers']['content-type']
        print(event['body'])
        body = base64.b64decode(event["body"])

        picture = decoder.MultipartDecoder(body, content_type_header).parts[0]
        prediction = get_prediction(image_bytes=picture.content)
        print (prediction)

        filename = picture.headers[b'Content-Disposition'].decode().split(';')[1].split('=')[1]
        if len(filename) < 4:
            filename = picture.headers[b'Content-Disposition'].decode().split(';')[2].split('=')[1]

        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({'file': filename.replace('"', ''), 'predicted': [prediction, classes[prediction] ]})
        }
    except Exception as e:
        print(repr(e))
        return {
            "statusCode": 500,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({"error": repr(e)})
        }
