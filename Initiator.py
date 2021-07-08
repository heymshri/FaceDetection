from Tkinter import *
from dataSetCreater import Detect 
from trainer import Train
from detector import Recognise
import tkSimpleDialog
import tkMessageBox

class Begin:

	def __init__(self,master):

		tkMessageBox.showinfo("Welcome","WELCOME TO FACE DETECTION AND RECOGNITION SYSTEM!\n""Please press OK to continue...")
		
		self.label=Label(master,text='Face Detection and Recognition System',font=("Arial Bold", 40),bg='Crimson',fg='MediumBlue')
		self.label.pack(pady=50,padx=50)

		master.title("Select the required action!!!")

		self.frame=Frame(master,bg='SkyBlue')
		self.frame.pack()

		self.system_login_button=Button(self.frame,text='Store Information',bd=6,bg='ForestGreen',fg='MidnightBlue',command=self.detect_and_store,font=(" Helvetica", 20),padx=25)
		self.system_login_button.pack(pady=35,padx=25)

		self.recognitionbutton=Button(self.frame,text='Process Recognition',bd=6,bg='ForestGreen',fg='MidnightBlue',command=self.start_detection,font=(" Helvetica", 20),padx=25)
		self.recognitionbutton.pack(pady=35,padx=25)

		self.deletebutton=Button(self.frame,text='Delete Information',bd=6,bg='ForestGreen',fg='MidnightBlue',command=self.delete_Info,font=(" Helvetica", 20),padx=25)
		self.deletebutton.pack(pady=35,padx=25)

		self.quitbutton=Button(self.frame,text="Quit System",bd=6,bg='ForestGreen',fg='MidnightBlue',command=self.quite_system,font=(" Helvetica", 20),padx=25)
		self.quitbutton.pack(pady=35,padx=25)	

	def detect_and_store(self):
		tkMessageBox.showinfo("Notifications!!!","Please Enter your personal Information!")
		self.Id=tkSimpleDialog.askinteger("ID Number","Enter ID:")
		self.name=tkSimpleDialog.askstring("Name","Enter Name:")
		self.Age=tkSimpleDialog.askinteger("Age","Enter Age:")
		self.Gender=tkSimpleDialog.askstring("Gender","Enter Gender:")
		self.Address=tkSimpleDialog.askstring("Address","Enter Address:")

		if(self.Id==None or self.name==None or self.Age==None or self.Gender==None or self.Address==None):
			tkMessageBox.showinfo('Error!!!', 'Sorry, all the personal information should be provided as asked by the system!')
			if(self.Id==None):
				tkMessageBox.showinfo('Notification!!!', 'You have not provided ID!')
			if(self.name==None):		
				tkMessageBox.showinfo('Notification!!!', 'You have not provided Name!')
			if(self.Age==None):
				tkMessageBox.showinfo('Notification!!!', 'You have not provided Age!')		
			if(self.Gender==None):
				tkMessageBox.showinfo('Notification!!!', 'You have not provided Gender!')
			if(self.Address==None):
				tkMessageBox.showinfo('Notification!!!', 'You have not provided Address!')

		else:
			d=Detect()
			d.insert_or_update(self.Id,self.name,self.Age,self.Gender,self.Address)
			d.check_or_store()
			t=Train()
			t.convert_and_store()

	def start_detection(self):
		r=Recognise()
		tkMessageBox.showinfo("Notification!!!","Please Press q to quit the Recognition process!")
		r.capture_and_recognise()

	def quite_system(self):
		tkMessageBox.showinfo("Notification!!!","System is Closed!")
		self.frame.quit()

	def delete_Info(self):
		tkMessageBox.showinfo("Information Erase Process","You need to provide personal ID Number!")
		self.del_ID=tkSimpleDialog.askinteger("ID Number","Enter the previously stored ID Number:")
		if(self.del_ID==None):
			tkMessageBox.showinfo('Notification!!!', 'No ID provided!')
		else:		
			d=Detect()
			d.delete_Information(self.del_ID)

root=Tk()
root.title("WELCOME!!!")
root.state("zoomed")
root.resizable(False,False)
root.configure(background="DarkCyan")
s=Begin(root)
root.mainloop()