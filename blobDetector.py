import cv2
import numpy as np
import dUtils.imageManip as duim
import dUtils.configFiles as duConfig

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
    params.thresholdStep = max(cv2.getTrackbarPos('Threshold Step', 'Blob Detector'),1)
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
    params.filterByColor = cv2.getTrackbarPos('Use Color', 'Blob Detector')
    params.blobColor = cv2.getTrackbarPos('Color', 'Blob Detector')
    return params

def setup(params=None):
    '''
    size_t ;
    bool filterByColor;
    uchar blobColor;
    '''
    if params is None:
        params = cv2.SimpleBlobDetector_Params()
    cv2.namedWindow('Blob Detector')
    cv2.createTrackbar('Min Threshold', 'Blob Detector', int(params.minThreshold), 255, update)
    cv2.createTrackbar('Max Threshold', 'Blob Detector', int(params.maxThreshold), 255, update)
    cv2.createTrackbar('Threshold Step', 'Blob Detector', int(params.thresholdStep), 30, update)
    cv2.createTrackbar('Min Distance', 'Blob Detector', int(params.minDistBetweenBlobs), 300, update)
    cv2.createTrackbar('Min Repeatability', 'Blob Detector', int(params.minRepeatability), 20, update)
    cv2.createTrackbar('Area', 'Blob Detector', int(params.filterByArea), 1, update)
    cv2.createTrackbar('Min Area', 'Blob Detector', int(params.minArea), 300, update)
    cv2.createTrackbar('Max Area', 'Blob Detector', int(params.maxArea), 1000, update)
    cv2.createTrackbar('Circularity', 'Blob Detector', int(params.filterByCircularity), 1, update)
    cv2.createTrackbar('Min Circularity', 'Blob Detector', int(params.minCircularity*100), 100, update)
    cv2.createTrackbar('Max Circularity', 'Blob Detector', int(min(2147483647,params.maxCircularity*100)), 100, update)
    cv2.createTrackbar('Inertia', 'Blob Detector', int(params.filterByInertia), 1, update)
    cv2.createTrackbar('Min Inertia', 'Blob Detector', int(params.minInertiaRatio*100), 100, update)
    cv2.createTrackbar('Max Inertia', 'Blob Detector', int(min(2147483647,params.maxInertiaRatio*100)), 100, update)
    cv2.createTrackbar('Convexity', 'Blob Detector', int(params.filterByConvexity), 1, update)
    cv2.createTrackbar('Min Convexity', 'Blob Detector', int(params.minConvexity*100), 100, update)
    cv2.createTrackbar('Max Convexity', 'Blob Detector', int(min(2147483647,params.maxConvexity*100)), 100, update)
    cv2.createTrackbar('Use Color', 'Blob Detector', int(params.filterByColor), 1, update)
    cv2.createTrackbar('Color', 'Blob Detector', int(params.blobColor), 255, update)

def outputParams(params):
    string = 'params = cv2.SimpleBlobDetector_Params()\n'
    string = 'params.minThreshold = %s\n'%params.minThreshold

def tuneFunction(function, params=None):
    setup(params)
    while True:
        ch = 0xFF & cv2.waitKey(100)
        if ch == 27 or ch == -1:
            break
        params = update()
        detector = cv2.SimpleBlobDetector_create(params) 
        img = function()
        frame = duim.toGray(img)
        #ret,thresh = cv2.threshold(frame,params.maxThreshold,255,cv2.THRESH_TRUNC)
        
        # Detect blobs.
        keypoints = detector.detect(frame)
        output = img.copy()
        output = cv2.drawKeypoints(output, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow('Blob Detector Output', output)
    cv2CloseWindow('Blob Detector')
    cv2CloseWindow('Blob Detector Output')
    return params

def tuneImg(image, params=None):
    return tuneFunction(lambda: image,params)

def tuneCam(camera, params=None):
    return tuneFunction(camera.read, params)

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
