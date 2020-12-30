
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 20:03:17 2020

@author: satya
"""

import cv2    ## version 4.2.0

import numpy as np

import pyautogui    # any Latest version

from tkinter import Label  # any latest version
from tkinter import Tk
from tkinter import Entry
import tkinter as HUE_VALUES







master = Tk()

master.geometry("400x250")
master.title(" Values index ")



Label(master,text='Enter the hue Values:').place(x=100,y=0)



Label(master,text='HUE MIN:').place(x=50,y=20)
Label(master,text='SAT MIN:').place(x=50,y=40)
Label(master,text='VAL MIN:').place(x=50,y=60)

Label(master,text='HUE MAX:').place(x=50,y=100)
Label(master,text='SAT MAX:').place(x=50,y=120)
Label(master,text='VAL MAX:').place(x=50,y=140)

# Default HSV values for Color ORANGE

HUE_MIN_p=Entry(master )
HUE_MIN_p.insert(0,"0")
HUE_MIN_p.place(x=150,y=20)

SAT_MIN_p =Entry(master )
SAT_MIN_p.insert(0,"200")
SAT_MIN_p.place(x=150,y=40)

VAL_MIN_p =Entry(master )
VAL_MIN_p.insert(0,"136")
VAL_MIN_p.place(x=150,y=60)

HUE_MAX_p =Entry(master )
HUE_MAX_p.insert(0,"22")
HUE_MAX_p.place(x=150,y=100)

SAT_MAX_p=Entry(master )
SAT_MAX_p.insert(0,"255")
SAT_MAX_p.place(x=150,y=120)

VAL_MAX_p=Entry(master )
VAL_MAX_p.insert(0,"255")
VAL_MAX_p.place(x=150,y=140)

def fun():

    global HUE_MIN
    global SAT_MIN
    global VAL_MIN
    global HUE_MAX
    global SAT_MAX
    global VAL_MAX



    HUE_MIN = int ( HUE_MIN_p.get());
    SAT_MIN = int ( SAT_MIN_p.get());
    VAL_MIN=  int (VAL_MIN_p.get());

    print(type (HUE_MIN), SAT_MIN,VAL_MIN);

    #  #HSV VALUES -MAX

    HUE_MAX = int ( HUE_MAX_p.get());
    SAT_MAX=  int (SAT_MAX_p.get());
    VAL_MAX=  int (VAL_MAX_p.get());

    master.destroy();

def fine_tuning ():

    cap = cv2.VideoCapture(0)

    def nothing(x):
        pass
    # Creating a window for later use
    cv2.namedWindow('result')

    # Starting with 100's to prevent error while masking
    h,s,v = 100,100,100

    def print_saved_numbers():
        print("Hue_value",h);
        return ;

    # Creating track bar
    cv2.createTrackbar('hue', 'result',0,179,nothing)
    cv2.createTrackbar('saturation', 'result',0,255,nothing)
    cv2.createTrackbar('value', 'result',0,255,nothing)

    while(1):

        _, frame = cap.read()

        #converting to HSV
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        # get info from track bar and appy to result
        HUE_MIN = cv2.getTrackbarPos('hue','result')
        SAT_MIN = cv2.getTrackbarPos('saturation','result')
        VAL_MIN = cv2.getTrackbarPos('value','result')



        # Normal masking algorithm
        lower_blue = np.array([HUE_MIN,SAT_MIN,VAL_MIN])
        upper_blue = np.array([180,255,255])

        mask = cv2.inRange(hsv,lower_blue, upper_blue)

        result = cv2.bitwise_and(frame,frame,mask = mask)

        cv2.imshow('result',result)

        print(type(HUE_MIN),SAT_MIN,SAT_MIN)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:

            HUE_MIN_p.delete(0,HUE_VALUES.END);
            HUE_MIN_p.insert(0,str(HUE_MIN))


            SAT_MIN_p.delete(0,HUE_VALUES.END);
            SAT_MIN_p.insert(0,str(SAT_MIN))

            VAL_MIN_p.delete(0,HUE_VALUES.END);
            VAL_MIN_p.insert(0,str(VAL_MIN))

            HUE_MAX_p.delete(0,HUE_VALUES.END)
            HUE_MAX_p.insert(0,"180")

            SAT_MAX_p.delete(0,HUE_VALUES.END)
            SAT_MAX_p.insert(0,"255")

            VAL_MAX_p.delete(0,HUE_VALUES.END);
            VAL_MAX_p.insert(0,"255")


            cap.release();
            cv2.destroyAllWindows();
            break

    HUE_MAX = 180
    SAT_MAX = 255
    VAL_MAX = 255



    pass;


HUE_VALUES.Button(master, text="START", command = fun ).place(x=180,y=180)

HUE_VALUES.Button(master, text="FINE TUNING", command = fine_tuning).place(x=180,y=160)




master.mainloop()

pyautogui.PAUSE = 0.05           # over ridding the default value of PAUSE  from 0.1 to 0.05
counter =0
maving_status = 'NOT MOVING'     # Default message of color tracker





# Refresh Rate
Refresh_rate = 30
min_dist = 70

cap =cv2.VideoCapture(0)

while True:

    ret , img =cap.read()


    gray=cv2.cvtColor(img, cv2.COLOR_BGR2HSV);

    img_cpy = img.copy();


    lower = np.array([HUE_MIN, SAT_MIN,VAL_MIN ],np.uint8);
    upper = np.array([HUE_MAX,SAT_MAX , SAT_MAX],np.uint8);

    print (HUE_MIN, SAT_MIN,VAL_MIN);

    mask= cv2.inRange(gray, lower, upper)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    for i in  contours:
        cnt = i

        area = cv2.contourArea(cnt)
        M = cv2.moments(cnt)
        #print('Area',area);
        if (area >= 100 ):                          # condition so that errors might not take over
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            if (counter ==0):
                intial_pos =[cx,cy]                  #Storing position OF center at intial Time

            counter= counter+1

            #print ("Centers:",cx,cy,'counter',counter)
            if (counter == Refresh_rate):                       #Calculating Diff afeter every 50 Counts
                counter = 0

                final_pos =[cx,cy]
                x_diff = intial_pos[0]-final_pos[0];
                y_diff = intial_pos[1]-final_pos[1];

                print("lenght_gap",x_diff,y_diff)

                if (x_diff> min_dist or y_diff > min_dist ): #for UP and RIght movement
                    if x_diff > y_diff :
                        if (x_diff>0):

                            # MOVING RIGHT Detection
                            print("moving_right");
                            pyautogui.press('right')
                            maving_status = 'MOVING RIGHT'
                           # cv2.putText(img_cpy,'moving_right' , (10,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
                    else :
                        if (y_diff>0): # MOVING UP Detection

                            pyautogui.press('up')
                            maving_status = 'MOVING UP'
                           # cv2.putText(img_cpy,'moving_right' , (10,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)


                elif (x_diff < (-1 * (min_dist)) or y_diff< (-1 * (min_dist)) ): #for UP and RIght movement
                    if x_diff < y_diff :
                        if (x_diff<0):
                            print("moving_left");
                            pyautogui.press('left')
                            maving_status = 'MOVING LEFT'
                           # cv2.putText(img_cpy,'moving_right' , (10,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
                    else :
                        if (y_diff<0):
                            pyautogui.press('down')
                            maving_status = 'MOVING DOWN'
                           # cv2.putText(img_cpy,'moving_right' , (10,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)



                else :
                    maving_status = 'NOT MOVING'

                        #cv2.putText(img_cpy,'moving_Left' , (10,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)

            cv2.drawContours(img_cpy, cnt, -1, (0,255,0), 3);
            cv2.putText(img_cpy,maving_status, (10,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)





    cv2.imshow("frame", img);
    cv2.imshow("frame1", mask);
    cv2.imshow("convex", img_cpy);


    if cv2.waitKey(1) & 0xFF == ord('q'):      # Press 'q' or "Q" to EXIT
        cv2.destroyAllWindows();
        cap.release();
        break
