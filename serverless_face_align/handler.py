print ('starting....')
try:
    import unzip_requirements
except ImportError:
    pass

import dlib
import cv2
import numpy as np
import faceBlendCommon as fbc

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
PREDICTOR_PATH = os.environ['MODEL_PATH'] if 'MODEL_PATH' in os.environ else 'shape_predictor_5_face_landmarks.dat'

print (S3_BUCKET)
print (PREDICTOR_PATH)
s3 = boto3.client('s3')
faceDetector = dlib.get_frontal_face_detector()
landmarkDetector = dlib.shape_predictor(PREDICTOR_PATH)

print ('downloading model complete')

def classify_image (event, context):
    try:
        content_type_header = event['headers']['content-type']
        body = base64.b64decode(event["body"])

        picture = decoder.MultipartDecoder(body, content_type_header).parts[0]
        im_arr = np.frombuffer(picture.content, dtype=np.uint8)
        im = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        points = fbc.getLandmarks(faceDetector, landmarkDetector, im)
        points = np.array(points)
        im = np.float32(im)/255.0
        h = 600
        w = 600
        imNorm, points = fbc.normalizeImagesAndLandmarks((h, w), im, points)
        imNorm = np.uint8(imNorm*255)

        filename = picture.headers[b'Content-Disposition'].decode().split(';')[1].split('=')[1]
        if len(filename) < 4:
            filename = picture.headers[b'Content-Disposition'].decode().split(';')[2].split('=')[1]
        print ('all done')
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({'file': filename.replace('"', ''), 'aligned_image': str (base64.b64encode (cv2.imencode ('.jpg', imNorm)[1])) })
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
