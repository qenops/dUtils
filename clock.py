import time, cv2, numpy as np

FONT=cv2.FONT_HERSHEY_SIMPLEX

def strToImg(text, scale=1.0,thick=1,color=(255,255,255),backCol=(0,0,0)):
    shape, baseLine = cv2.getTextSize(text,FONT,scale,int(scale*2.5))
    img = np.zeros((shape[1]*2,shape[0]+1,3), dtype=np.uint8)
    point = (0,int(shape[1]*1.5))
    drawStr(img,point,text,scale,thick,color,backCol)
    return img

# Draw a string on an image (from cv2 example common.py)
def drawStr(dst, point, text, scale=1.0,thick=1,color=(255,255,255),backCol=(0,0,0)):
    x,y = point
    cv2.putText(dst, text, (x+1, y+1), FONT, scale, backCol, thickness = thick*2, lineType=cv2.LINE_AA)
    cv2.putText(dst, text, (x, y), FONT, scale, color,thickness = thick, lineType=cv2.LINE_AA)

def cv2CloseWindow(window):
    cv2.destroyWindow(window)
    cv2.waitKey(1)
    cv2.waitKey(1)
    cv2.waitKey(1)
    cv2.waitKey(1)

def renderLoop():
    start = time.time()
    while(True):
        clock = time.time() - start
        frame = strToImg(f'{clock:07.3f}', scale=8, thick=8)
        cv2.imshow('frame', frame)   # Display the frame
        ch = cv2.waitKey(1) & 0xFF
        if ch == 27:                # escape
            break
    cv2CloseWindow('frame')

if __name__ == "__main__":
    renderLoop()