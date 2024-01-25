import cv2

def face_detect(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier("C:\\Users\\PC_User\\Desktop\\controller\\CNN\\haarcascade_frontalface_default.xml")
    lists = cascade.detectMultiScale(img_gray, scaleFactor=1.5, minNeighbors=2, minSize=(50, 50)) #minNeighbors(認識する人数)
    if len(lists):
        for (x,y,w,h) in lists:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), thickness=2)
        cv2.waitKey(0)
    else: pass
    return img

def eye_detect(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier("C:\\Users\\PC_User\\Desktop\\controller\\CNN\\haarcascade_frontalface_default.xml")
    lists = cascade.detectMultiScale(img_gray, scaleFactor=1.5, minNeighbors=2, minSize=(50, 50)) #minNeighbors(認識する人数)
    if len(lists):
        for (x,y,w,h) in lists:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), thickness=2)
        cv2.waitKey(0)
    else: pass
    return img

