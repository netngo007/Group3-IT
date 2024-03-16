from tkinter import *
import customtkinter as ctk
import requests
from tkinter import *
import requests
import customtkinter as ctk
import requests, base64
import geocoder

from tkinter import messagebox 


apikey="73a13f26ae664ffe56f68cf1e3d93903"

class Dashboard(ctk.CTkFrame):
    
    def __init__(self,parent):

        super().__init__(parent)
        g = geocoder.ip('me') 
        self.configure(fg_color='#e4f2ff',corner_radius=(30))
        self.grid(row=0,column=1,sticky='wens')
        self.blank1=ctk.CTkFrame(self,fg_color='#e4f2ff')
        self.blank1.place(relx=1,rely=0.1,anchor=CENTER)
        self.blank2=ctk.CTkFrame(self,fg_color='#e4f2ff')
        self.blank2.place(relx=1,rely=0.9,anchor=CENTER)
        container0=ctk.CTkFrame(self,fg_color='#e4f2ff')
        container0.pack(anchor='w',padx=(50, 0),pady=(50,50))
        Hello=ctk.CTkLabel(container0,text='Welcome back!',font=('Helvetica',20,'bold'),text_color='black')
        
        Hello.pack(anchor='w')
        Hello2=ctk.CTkLabel(container0,text='Check out today weather information',font=('Helvetica',20),text_color='black')
        Hello2.pack()
        searchentry=ctk.CTkEntry(container0,  #
                                 placeholder_text='Enter city name',#   
                                 placeholder_text_color='black',

                                 height=40,width=200,#                   
                                 border_width=0,corner_radius=10,#        
                                 text_color='black',#                    
                                 fg_color='#ffffff')#     
        searchentry.bind("<Return>", (lambda event: self.forecast(searchentry.get())))
        searchentry.pack(anchor='w')
        self.container1=ctk.CTkFrame(self,fg_color='#e4f2ff')
        self.container1.pack(expand=True,fill=BOTH,pady=(0,20))
        self.container1.rowconfigure(0,weight=10)

        

        container2=ctk.CTkFrame(self,fg_color='#e4f2ff')
        container2.pack(expand=True,fill=BOTH,padx=(20, 20),pady=(0,20))
       
        self.forecast(g.city.lower())

        ###FUNCS
        #1.hàm fetch data dự báo thời tiết chính
    def forecast(self,x):
            
            url2 = f'http://api.openweathermap.org/data/2.5/forecast?q={x}&appid={apikey}'


            req2 = requests.get(url2)
            data2 = req2.json()
            if data2['cod'] == '404':
                    messagebox.showerror("showerror", "Error") 
                    return
            
            else:
                for child in self.container1.winfo_children():
                    child.destroy()
                framesthoitiet=[]  
                framesngay=[]   
                frameshinh=[] 
                framesgio=[]    
                for _ in range(8):  #tạo 7 ô 7 ngày
                    widget=ctk.CTkFrame(self.container1,width=81,height=300,fg_color='#ffffff')
                    widget.pack(side=LEFT,fill=BOTH,expand=True,padx=5)
                    ngay=ctk.CTkLabel(widget,text='',text_color='black',font=('Helvetica',10))
                    ngay.pack(pady=10)

                    thoitiet=ctk.CTkLabel(widget,text='alo',text_color='black',font=('Helvetica',15,'bold'))
                    thoitiet.pack()
                    hinh=ctk.CTkLabel(widget,text='')
                    hinh.pack(padx=5)
                    gio=ctk.CTkLabel(widget,text='',text_color='black',font=('Helvetica',10))
                    gio.pack()
                    framesthoitiet.append(thoitiet)
                    framesngay.append(ngay)
                    frameshinh.append(hinh)
                    framesgio.append(gio)
                req2 = requests.get(url2)
                data2 = req2.json()
                current_date = ''

                # lấy từ 3 bởi vì api này cung cấp thêm 3 khung giờ trước hiện tại
                for item in data2['list'][3:10]:
                        time = item['dt_txt']
                        # chia ngày,giờ ra thành dạng[2018-04-15 06:00:00]
                        next_date, hour = time.split(' ')                   
            
                            
                        framesngay[data2['list'][3:10].index(item)].configure(text=next_date) # thêm ngày vào ô ngày
                        hour = int(hour[:2])   # lấy phần HH ra khỏi chuỗi HH:MM:SS
                        

                        weathericon=item['weather'][0]['icon']
                            
                        url = f'http://openweathermap.org/img/wn/{weathericon}@2x.png'# \
                        response = requests.get(url, stream=True)#                       \
                        a=base64.encodebytes(response.raw.read())#                        |->lấy hình ảnh
                        b=PhotoImage(data=a)#                                            /
                        frameshinh[data2['list'][3:10].index(item)].configure(image=b)#
                        

                        framesgio[data2['list'][3:10].index(item)].configure(text=f'{hour}:00')# thêm giờ vào ô giờ
                        
                        temperature = item['main']['temp']
                        framesthoitiet[data2['list'][3:10].index(item)].configure(text=f'{round(temperature-273.15,1)}℃')# thêm nhiệt độ vào ô giờ

                    
                        
    