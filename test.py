from tkinter import *
from Dashboard import Dashboard
from Currentweatherframe import Currentweatherframe
import customtkinter as ctk 
class App(ctk.CTk):  

    def __init__(self):  #khoi tao  chuong trinh

        #core setup 
        super().__init__() # khởi tạo chạy cái parent(lớp cha mẹ)
        
        self.title('Weather forecast') # dat ten window
        self.geometry('1200x800')   # size window
        self.configure(fg_color='#5c9ce4') #chỉnh lại màu của app 
        #widget
        self.columnconfigure(0,weight=0) # chỉnh lại độ to của cột 0
        self.columnconfigure(1,weight=9)# chỉnh lại độ to của cột 1
        self.rowconfigure(0,weight=1)# chỉnh lại độ to của hàng 1

        self.dashboard=Dashboard(self)  #khung dashboard
        
        self.current=Currentweatherframe(self)  #khung tìm thời tiết
        mainloop()  #lặp lại vòng lặp này vô hạn
App()
