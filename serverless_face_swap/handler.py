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
PREDICTOR_PATH = os.environ['MODEL_PATH'] if 'MODEL_PATH' in os.environ else 'shape_predictor_68_face_landmarks.dat'

print (S3_BUCKET)
print (PREDICTOR_PATH)
s3 = boto3.client('s3')
try:
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)
except:
    s3.download_file(S3_BUCKET, PREDICTOR_PATH, PREDICTOR_PATH)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)

print ('downloading model complete')

def classify_image (event, context):
    try:
        content_type_header = event['headers']['content-type']
        body = base64.b64decode(event["body"])

        picture = decoder.MultipartDecoder(body, content_type_header)
        
        im_arr1 = np.frombuffer(picture.parts[0].content, dtype=np.uint8)
        img1 = cv2.imdecode(im_arr1, flags=cv2.IMREAD_COLOR)
        im_arr2 = np.frombuffer(picture.parts[1].content, dtype=np.uint8)
        img2 = cv2.imdecode(im_arr2, flags=cv2.IMREAD_COLOR)

        im1Display = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        im2Display = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        img1Warped = np.copy(img2)
        print ('step1')

        points1 = fbc.getLandmarks(detector, predictor, img1)
        points2 = fbc.getLandmarks(detector, predictor, img2)
        print ('step2')

        hullIndex = cv2.convexHull(np.array(points2), returnPoints=False)
        # Create convex hull lists
        hull1 = []
        hull2 = []
        for i in range(0, len(hullIndex)):
            hull1.append(points1[hullIndex[i][0]])
            hull2.append(points2[hullIndex[i][0]])
        print ('step3')

        # Calculate Mask for Seamless cloning
        hull8U = []
        for i in range(0, len(hull2)):
            hull8U.append((hull2[i][0], hull2[i][1]))

        mask = np.zeros(img2.shape, dtype=img2.dtype) 
        cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))
        print ('step4')

        # Find Centroid
        m = cv2.moments(mask[:,:,1])
        center = (int(m['m10']/m['m00']), int(m['m01']/m['m00']))
        print ('step5')

        # Find Delaunay traingulation for convex hull points
        sizeImg2 = img2.shape    
        rect = (0, 0, sizeImg2[1], sizeImg2[0])

        dt = fbc.calculateDelaunayTriangles(rect, hull2)

        imTemp1 = im1Display.copy()
        imTemp2 = im2Display.copy()

        tris1 = []
        tris2 = []
        for i in range(0, len(dt)):
            tri1 = []
            tri2 = []
            for j in range(0, 3):
                tri1.append(hull1[dt[i][j]])
                tri2.append(hull2[dt[i][j]])

            tris1.append(tri1)
            tris2.append(tri2)

        cv2.polylines(imTemp1,np.array(tris1),True,(0,0,255),2);
        cv2.polylines(imTemp2,np.array(tris2),True,(0,0,255),2);
        print ('step6')

        for i in range(0, len(tris1)):
            fbc.warpTriangle(img1, img1Warped, tris1[i], tris2[i])
        print ('step7')

        output = cv2.seamlessClone(np.uint8(img1Warped), img2, mask, center, cv2.NORMAL_CLONE)

        print ('all done')

        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({'swaped_image': str (base64.b64encode (cv2.imencode ('.jpg', output)[1])) })
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
