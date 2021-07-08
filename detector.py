import cv2,os
import numpy as np
from PIL import Image
import pickle
import sqlite3
import pygame

class Recognise:
    def __init__(self):
        self.recognizer = cv2.createLBPHFaceRecognizer()
        self.recognizer.load('recogniser/trainingData.yml')
        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
        self.eyeDetector = cv2.CascadeClassifier('haarcascade_eye.xml')
        self.noseDetector = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
        self.mouthDetector = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
        
        self.path="dataSet"
        pygame.init()
        pygame.mixer.music.load('Alert.mp3')

    def getProfile(self,Id):
        self.conn=sqlite3.connect("my_database.db")
        self.cmd="select * from people where ID="+str(self.Id)
        self.cursor=self.conn.execute(self.cmd)

        self.profile=None

        for row in self.cursor:
            self.profile=row
        
        self.conn.close()
        return self.profile

    def capture_and_recognise(self):    
        self.cam = cv2.VideoCapture(0)
        self.font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
        self.flag = False
        
        while True:
            self.ret, self.img =self.cam.read()
            if self.ret is True:
                self.gray=cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
            else:
                continue

            self.faces=self.faceCascade.detectMultiScale(self.gray, 1.3,5)
                        
            self.profile = 1
            
            for (x,y,w,h) in self.faces:
                self.Id, self.conf = self.recognizer.predict(self.gray[y:y+h,x:x+w])
                cv2.rectangle(self.img, (x,y), (x+w,y+h), (255,0,0), 2)
                
                self.roi_gray = self.gray[y:y+h, x:x+w]
                self.roi_color = self.img[y:y+h, x:x+w]

                self.eyes = self.eyeDetector.detectMultiScale(self.roi_gray)                
                self.nose =  self.noseDetector.detectMultiScale(self.roi_gray)
                self.mouth = self.mouthDetector.detectMultiScale(self.roi_gray)

                for (ex,ey,ew,eh) in self.eyes:
                    cv2.rectangle(self.roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)
                for (nx, ny, nw, nh) in self.nose:
                    cv2.rectangle(self.roi_color, (nx, ny), (nx + nw, ny + nh), (0, 0, 255), 2)
                for (mx, my, mw, mh) in self.mouth:
                    cv2.rectangle(self.roi_color, (mx, my), (mx + mw, my + mh), (0, 0, 0), 2)
        
                self.flag = False
                
                self.profile = self.getProfile(self.Id)
               # print(self.profile)
                if(self.conf<42):
                    if(self.profile==None):
                        self.flag = True            
                    if(self.profile!=None):
                        cv2.cv.PutText(cv2.cv.fromarray(self.img),str(self.profile[1]), (x,y+h+30),self.font, 255)
                        cv2.cv.PutText(cv2.cv.fromarray(self.img),str(self.profile[2]), (x,y+h+60),self.font, 255)
                        cv2.cv.PutText(cv2.cv.fromarray(self.img),str(self.profile[3]), (x,y+h+90),self.font, 255)
                        cv2.cv.PutText(cv2.cv.fromarray(self.img),str(self.profile[4]), (x,y+h+120),self.font, 255)
    
                    if(self.profile == None):
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play()
            cv2.imshow('Recognizing...',self.img)

            if cv2.waitKey(10) & 0xFF==ord('q'):
                break

        self.cam.release()
        cv2.destroyAllWindows()
