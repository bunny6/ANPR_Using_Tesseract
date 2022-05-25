### importing required libraries
import torch
import cv2
import time
import pytesseract
import re
import numpy as np
#import easyocr
import psycopg2
import psycopg2.extras
from PIL import Image
import io
import imutils

conn = psycopg2.connect( #psycopg2 database adaptor for implementing python
        host="localhost",
        database="num_plate",
        user='postgres',
        password='p@ssw0rd')



#Main function
plates=[]
def main(img_path=None, vid_path=None,vid_out = None):
    
    print(f"[INFO] Loading model... ")
    #loading the custom trained model
    model =  torch.hub.load('yolov5', 'custom', source ='local', path='bestvm.pt',force_reload=True) ### The repo is stored locally
    
   
 #for detection on video
    if vid_path !=None:
        print(f"[INFO] Working with video: {vid_path}")

        ## reading the video
        cap = cv2.VideoCapture(vid_path)


        if vid_out: #creating the video writer if video output path is given

            #by default VideoCapture returns float instead of int
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            codec = cv2.VideoWriter_fourcc(*'mp4v') ##(*'XVID')
            out = cv2.VideoWriter(vid_out, codec, fps, (width, height))

        # assert cap.isOpened()
        frame_no = 1

        cv2.namedWindow("vid_out", cv2.WINDOW_NORMAL)
        while True:
            # start_time = time.time()
            ret, frame = cap.read()
            if ret  and frame_no %1 == 0:
                # pic = Image.open(io.BytesIO(frame))
                results = model(frame, size=640)
                # results.show()  
                croped_img = results.crop(save=True) #cropping the image on bounding box
               
                if croped_img==[]:
                    continue
                croped_img=croped_img[0]['im'] #to get the image array from the array created from above step
                img = imutils.resize(croped_img, width=300 ) 
                img = cv2.cvtColor(croped_img, cv2.COLOR_BGR2GRAY) #to convert image to gray
                img = cv2.resize(img, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)
               
                img = cv2.bilateralFilter(img, 11, 17, 17) 
                img = cv2.medianBlur(img, 3)
                cv2.threshold(img,127,255,cv2.THRESH_BINARY)
                cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        
                frame=Image.fromarray(croped_img) #to get image from array
                frame.show()#to display image
                text = pytesseract.image_to_string(frame)#to extract the charcters from number plate
               
                sent2=''        
                for i in text:
                    if i.lower()!=i or i.isdigit():
                        sent2+=i 
                plates.append(sent2)
                
                print(plates)

               
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break
                frame_no += 1
            else:
               
                break

 #calling the main function
main(vid_path="skoda1.mp4",vid_out="vid_1.mp4") #for custom video
print(plates)

result = list(filter(lambda x: x==str(x),plates))
result = list(filter(lambda x: x!="",result))
most_common = max(result, key = result.count)
print(most_common)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
s = "SELECT * FROM VEHICLE where vehicle_number =%s"


cur.execute(s, (most_common,))
res = cur.fetchall()
if len(res)>=1:
    print("Car has granted permission")
else: 
    print("Car has not granted permission")    


            

