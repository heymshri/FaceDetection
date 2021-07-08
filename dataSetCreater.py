import cv2
import sqlite3
import tkMessageBox

class Detect:

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
        self.eyeDetector = cv2.CascadeClassifier('haarcascade_eye.xml')
        self.noseDetector = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
        self.mouthDetector = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

    def insert_or_update(self,Id,Name,Age,Gender,Address):
        self.Id=Id
        self.Name=Name
        self.Age=Age
        self.Gender=Gender
        self.Address=Address

        self.conn=sqlite3.connect("my_database.db")
        self.cmd="select * from people where ID ="+str(self.Id)
        self.cursor=self.conn.execute(self.cmd)

        self.isRecordExist=0 #for checking existence of data
        for self.row in self.cursor:
            self.isRecordExist=1

        if(self.isRecordExist==1):
            self.cmd="update people set Name="+str(self.Name)+"Age="+str(self.Age)+"Gender="+str(self.Gender)+"Address="+str(self.Address)+"where ID="+str(self.Id)
        else:
            self.cmd="insert into people(ID,Name,Age,Gender,Address) values("+str(self.Id)+","+str(self.Name)+","+str(self.Age)+","+str(self.Gender)+","+str(self.Address)+")"
    
        self.conn.execute(self.cmd)
        self.conn.commit()
        self.conn.close()
        tkMessageBox.showinfo("Notification!!!","Requested operation is done!")

    def delete_Information(self,del_ID):
        self.del_ID=del_ID
        self.conn=sqlite3.connect("my_database.db")
        self.cmd="delete from people where ID ="+str(self.del_ID)
        self.cursor=self.conn.execute(self.cmd)
        self.conn.commit()
        self.conn.close()
        tkMessageBox.showinfo("Notification!!!","Informations are removed!")

    def check_or_store(self):
        self.sampleNum=0
        while(True):
            self.ret, self.img = self.cam.read()

            if self.ret is True:
                self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            else:
                continue
                
            self.faces = self.detector.detectMultiScale(self.gray, 1.3, 5)
                        
            for (x,y,w,h) in self.faces:
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
        
                #incrementing sample number 
                self.sampleNum += 1
                #saving the captured face in the dataset folder
                cv2.imwrite("dataSet/User."+str(self.Id) +'.'+str(self.sampleNum)+".png", self.gray[y:y+h,x:x+w])

                cv2.imshow('Detecting and Storing the information...',self.img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                tkMessageBox.showinfo("Notification!!!","Images are stored!")
                break
            # break if the sample number is morethan 20
            elif self.sampleNum>100:
                break
        self.cam.release()
        cv2.destroyAllWindows()
