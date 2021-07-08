import cv2,os
import numpy as np
from PIL import Image

class Train:

    def __init__(self):
        self.recognizer = cv2.createLBPHFaceRecognizer()
        self.detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.eyeDetector = cv2.CascadeClassifier('haarcascade_eye.xml')
        self.noseDetector = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
        self.mouthDetector = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
        self.path="dataSet"

    def getImagesAndLabels(self,path):
        #get the path of all the files in the folder
        self.imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        #create empth face list
        self.faceSamples=[]
        #create empty ID list
        self.Ids=[]
        
        #now looping through all the image paths and loading the Ids and the images
        for imagePath in self.imagePaths:
            # Updates in Code
            # ignore if the file does not have jpg extension :
            if(os.path.split(imagePath)[-1].split(".")[-1]!='png'):
                continue

            #loading the image and converting it to gray scale
            self.pilImage=Image.open(imagePath).convert('L')
            #Now we are converting the PIL image into numpy array
            self.imageNp=np.array(self.pilImage,'uint8')
            #getting the Id from the image
            self.Id=int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            self.faces=self.detector.detectMultiScale(self.imageNp)
            
            for face in self.faces:
                face=self.eyeDetector.detectMultiScale(self.imageNp)
                face=self.noseDetector.detectMultiScale(self.imageNp)
                face=self.mouthDetector.detectMultiScale(self.imageNp)
            #If a face is there then append that in the list as well as Id of it
            
            for (x,y,w,h) in self.faces:
                self.faceSamples.append(self.imageNp[y:y+h,x:x+w])
                self.Ids.append(self.Id)
        
        return self.faceSamples,self.Ids

    def convert_and_store(self):
        self.faces,self.Ids = self.getImagesAndLabels(self.path)
        self.recognizer.train(self.faces, np.array(self.Ids))
        self.recognizer.save('recogniser/trainingData.yml')
        cv2.destroyAllWindows()