import cv2
import numpy as np
import imageManip as duim

def cv2CloseWindow(window):
    cv2.destroyWindow(window)
    cv2.waitKey(1)
    cv2.waitKey(1)
    cv2.waitKey(1)
    cv2.waitKey(1)

# Generate and display the images
def update(dummy=None):
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = max(cv2.getTrackbarPos('Min Threshold', 'Blob Detector'),1)
    params.maxThreshold = cv2.getTrackbarPos('Max Threshold', 'Blob Detector')
    params.thresholdStep = cv2.getTrackbarPos('Threshold Step', 'Blob Detector')
    params.minDistBetweenBlobs = cv2.getTrackbarPos('Min Distance', 'Blob Detector')
    params.minRepeatability = int(cv2.getTrackbarPos('Min Repeatability', 'Blob Detector'))
    params.filterByArea = cv2.getTrackbarPos('Area', 'Blob Detector')
    params.minArea = max(cv2.getTrackbarPos('Min Area', 'Blob Detector'),1)
    params.maxArea = cv2.getTrackbarPos('Max Area', 'Blob Detector')
    params.filterByCircularity = cv2.getTrackbarPos('Circularity', 'Blob Detector')
    params.minCircularity = cv2.getTrackbarPos('Min Circularity', 'Blob Detector')/100.
    params.maxCircularity = cv2.getTrackbarPos('Max Circularity', 'Blob Detector')/100.
    params.filterByInertia = cv2.getTrackbarPos('Inertia', 'Blob Detector')
    params.minInertiaRatio = cv2.getTrackbarPos('Min Inertia', 'Blob Detector')/100.
    params.maxInertiaRatio = cv2.getTrackbarPos('Max Inertia', 'Blob Detector')/100.
    params.filterByConvexity = cv2.getTrackbarPos('Convexity', 'Blob Detector')
    params.minConvexity = cv2.getTrackbarPos('Min Convexity', 'Blob Detector')/100.
    params.maxConvexity = cv2.getTrackbarPos('Max Convexity', 'Blob Detector')/100.
    return params

def setup(minArea=16,maxArea=75,minThreshold=0,maxThreshold=150):
    '''
    size_t ;
    bool filterByColor;
    uchar blobColor;
    '''
    cv2.namedWindow('Blob Detector')
    cv2.createTrackbar('Min Threshold', 'Blob Detector', minThreshold, 255, update)
    cv2.createTrackbar('Max Threshold', 'Blob Detector', maxThreshold, 255, update)
    cv2.createTrackbar('Threshold Step', 'Blob Detector', 10, 30, update)
    cv2.createTrackbar('Min Distance', 'Blob Detector', 10, 300, update)
    cv2.createTrackbar('Min Repeatability', 'Blob Detector', 2, 20, update)
    cv2.createTrackbar('Area', 'Blob Detector', 1, 1, update)
    cv2.createTrackbar('Min Area', 'Blob Detector', minArea, 300, update)
    cv2.createTrackbar('Max Area', 'Blob Detector', maxArea, 1000, update)
    cv2.createTrackbar('Circularity', 'Blob Detector', 0, 1, update)
    cv2.createTrackbar('Min Circularity', 'Blob Detector', 90, 100, update)
    cv2.createTrackbar('Max Circularity', 'Blob Detector', 100, 100, update)
    cv2.createTrackbar('Inertia', 'Blob Detector', 0, 1, update)
    cv2.createTrackbar('Min Inertia', 'Blob Detector', 90, 100, update)
    cv2.createTrackbar('Max Inertia', 'Blob Detector', 100, 100, update)
    cv2.createTrackbar('Convexity', 'Blob Detector', 0, 1, update)
    cv2.createTrackbar('Min Convexity', 'Blob Detector', 90, 100, update)
    cv2.createTrackbar('Max Convexity', 'Blob Detector', 100, 100, update)

def outputParams(params):
    string = 'params = cv2.SimpleBlobDetector_Params()\n'
    string = 'params.minThreshold = %s\n'%params.minThreshold

def tuneFunction(function, invert=True):
    setup()
    while True:
        ch = 0xFF & cv2.waitKey(100)
        if ch == 27 or ch == -1:
            break
        params = update()
        detector = cv2.SimpleBlobDetector_create(params) 
        img = function()
        frame = duim.toGray(img)
        # inverse the image
        if invert:
            frame = np.invert(frame)
        ret,thresh = cv2.threshold(frame,params.maxThreshold,255,cv2.THRESH_TRUNC)
        
        # Detect blobs.
        keypoints = detector.detect(thresh)
        output = img.copy()
        output = cv2.drawKeypoints(output, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow('Blob Detector Output', output)
    cv2CloseWindow('Blob Detector')
    cv2CloseWindow('Blob Detector Output')
    return params

def tuneImg(image, invert=True):
    return tuneFunction(lambda: image,invert)

def tuneCam(camera, invert=True):
    return tuneFunction(camera.read, invert)

'''
import cv2
import blobDetectorUtility as blob
img = cv2.imread('blobShared.png')
blob.blobDetectorParameterTune(img)
'''

def findBlobs(img, params, invert=True):
    detector = cv2.SimpleBlobDetector_create(params)
    frame = duim.toGray(img)
    if invert:
        frame = np.invert(frame)
    ret,thresh = cv2.threshold(frame,params.maxThreshold,255,cv2.THRESH_TRUNC)
    return detector.detect(thresh)
