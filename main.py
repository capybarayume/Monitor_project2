import os
import cv2
import time
import glob
from emling import send_email
from threading import Thread
from sys import exit

video = cv2.VideoCapture(0)
time.sleep(1)

status_list=[]
first_frame= None
count=0

def send_email_and_clean_images_folder(image_to_send, images_to_delete):
    try:
        send_email(image_to_send)
        for image in images_to_delete:
            os.remove(image)
    except AttributeError:
        print("Maybe I deleted the email too fast , but something had entered the screen my brother D:")
    except Exception:
        print("Something wrong,check the code!!")
        exit()


while True:
    status=0
    check, frame =video.read()
    gray_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau=cv2.GaussianBlur(gray_frame, (21,21) ,0)
    
    if first_frame is None:
        first_frame=gray_frame_gau

    delta_frame=cv2.absdiff(first_frame, gray_frame_gau)

    theresh_frame=cv2.threshold(delta_frame, 70 ,255, cv2.THRESH_BINARY)[1]
    dil_frame=cv2.dilate(theresh_frame ,None, iterations=2)
    contours, check =cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:

        #ignore the subtle light changes
        if cv2.contourArea(contour)<10000:
            continue

        x,y,w,h=cv2.boundingRect(contour)
        retangle=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)

        #if there has any retangle appear then start to save images
        if retangle.any():
            status=1

            #Enter the your own images file location
            cv2.imwrite("/Users/user_name/Monitor_project2/images/{0}.png".format(count), frame)
            count+=1


    status_list.append(status)

    #send the email when object left the screen
    status_list=status_list[-2:]
    if status_list[0]==1 and status_list[1]==0:
        all_image=glob.glob("/Users/user_name/Monitor_project2/images/*.png")
        index=int(len(all_image)/2)
        image_with_object=all_image[index]
        Thread(target=send_email_and_clean_images_folder,args=(image_with_object,all_image),daemon=True,name="send&clean").start()


    cv2.imshow("My video", frame)
    key=cv2.waitKey(1)
    
    if key ==ord("q"):
        break

video.release()

#Enter the your own images file location
final_delete_image=glob.glob("/Users/user_name/Monitor_project2/images/*.png")
for image in final_delete_image:
        os.remove(image)

