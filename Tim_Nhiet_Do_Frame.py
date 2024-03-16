from tkinter import *
import requests
import customtkinter as ctk
import requests, base64
import geocoder
import datetime
from PIL import Image
from tkinter import messagebox 

g = geocoder.ip('me')  # lấy thông tin từ ip cá nhân
apikey="73a13f26ae664ffe56f68cf1e3d93903"   #key api


class Currentweatherframe(ctk.CTkFrame):# bản mẫu, một khuôn mẫu. Ở đó ta khai báo các thuộc tính  và phương thức 

   
    def __init__(self,parent): #chay khi class đc kích hoạt
        
        super().__init__(parent)# khởi tạo chạy cái parent(lớp cha mẹ ở đây là App trong file main.py)

                
    
        self.configure(fg_color='#5c9ce4') # màu nền

        self.grid(row=0,column=0,sticky='wens') # cách đặt frame
      
        self.columnconfigure(0,weight=0,pad=20)#  \ 
        self.rowconfigure(0,weight=0,pad=30)#      \
        self.rowconfigure(1,weight=0,pad=0)#        |--> setup pad,độ lớn,của các hàng,cột
        self.rowconfigure(2,weight=0,pad=85)#      /
        self.rowconfigure(3,weight=0,pad=230)#    /
        

        #khung search
        container0=ctk.CTkFrame(self,fg_color='#5c9ce4')  #tạo frame
        container0.grid(row=0,column=0)     #đặt frame
        searchentry=ctk.CTkEntry(container0,  #\
                                 placeholder_text='Enter city name',    \
                                 placeholder_text_color='black',#       \
                                 height=40,width=200,#                   \
                                 border_width=0,corner_radius=10,#        |->chỉnh cho ô tìm kiểm
                                 text_color='black',#                    /
                                 fg_color='#e4f2ff')#                   /
        searchentry.pack(side=TOP)  #cách đặt ô tìm kiếm
        searchentry.bind("<Return>", (lambda event: city_search(searchentry.get()))) # chạy hàm khi người dùng ấn enter khi đang focus vào ô tìm kiếm,lambda dùng để chạy hàm khi hàm chưa đc tạo(hàm ẩn danh)


        #khung trả lại đữ liệu(thành phố và giờ)
        container=ctk.CTkFrame(self,fg_color='#5c9ce4')
        container.grid(row=1,column=0)
        container.columnconfigure(0,pad=30)
        container.columnconfigure(1,pad=30)
        container.rowconfigure(0,pad=10)
        container.rowconfigure(1,pad=10)
        city=ctk.CTkLabel(container,text='Searching: Ha Noi',font=('Helvetica',20,'bold'))
        city.grid(row=1,column=0)
        val1=ctk.CTkLabel(container,text='Nan',font=('Helvetica',20,'bold'))
        val1.grid(row=1,column=1)
        time=ctk.CTkLabel(container,text=f'📍 {g.city.lower()}',font=('Helvetica',18))
        time.grid(row=0,column=0)
        val2=ctk.CTkLabel(container,text='nan',font=('Helvetica',18))
        val2.grid(row=0,column=1)



        #khung trả lại đữ liệu(nhiệt độ, tình trạng thời tiết)
        container1=ctk.CTkFrame(self,fg_color='#5c9ce4')
        container1.grid(row=2,column=0)
        container1.columnconfigure(0,weight=0)
        container1.columnconfigure(1,weight=0)
        container1.columnconfigure(2,weight=0)
        container1.rowconfigure(0,weight=1,pad=10)
        container1.rowconfigure(1,weight=1,pad=10)
        temp=ctk.CTkLabel(container1,text='_℃',font=('Helvetica',60))
        temp.grid(row=0,column=1)
        type=ctk.CTkLabel(container1,text='Nan',font=('Helvetica',15,'bold'))
        type.grid(row=1,column=1)
         

        #khung hình ảnh thời tiết và minh hoạ 
        bottomcontainer=ctk.CTkFrame(self,fg_color='#5c9ce4')
        bottomcontainer.place(relx=0.25, rely=0.82, anchor=CENTER)
        cityimglabel1=ctk.CTkLabel(self,text='')
        cityimglabel1.place(relx=0.5, rely=0.5, anchor=CENTER)
        cityimg=ctk.CTkImage(light_image=Image.open('./buildings.png'),size=(300,300))
        cityimglabel=ctk.CTkLabel(bottomcontainer,image=cityimg,text='')
        cityimglabel.pack()
        
         


        
       ##################HÀM###############
        
            #1. Hàm lấy các tông tin về nhiệt độ, thời tiết 
        def fetch_weather_conditions(weather_data,x):
                    current_temp = (weather_data.json()['main']['temp']-32)*5/9
                    temp.configure(text=f'{round(current_temp,1)}℃')          #chỉnh nhiệt độ
                    weathericon=weather_data.json()['weather'][0]['icon']   
                    city.configure(text=x)                  #chỉnh tên thành phố
                    type.configure(text=weather_data.json()['weather'][0]['main'])  #chỉnh tên thời tiết
                    url = f'http://openweathermap.org/img/wn/{weathericon}@4x.png' #fetch hình ảnh thời tiết
                    response = requests.get(url,stream=True)
                    print(response)
                    a=base64.encodebytes(response.raw.read()) #base64 dùng mã hoá hình ảnh
                    b=PhotoImage(data=a)        #PhotoImage của tkinter cho phép chuyển ảnh mã hoá thành ảnh
                    cityimglabel1.configure(image=b)    #chỉnh ảnh
                    
                    time_fetched(weather_data)
                    
                   
            #2. Hàm lấy/update thời gian thực(local time) 
        def time_update(weather_data):
                    fmt = "%b,%d %H:%M"   # dạng ví dụ Feb.12 12:20
                    time=weather_data.json()['timezone'] 
                    tz = datetime.timezone(datetime.timedelta(seconds=int(time)))   #chuyển timedelta thành timezone
                    now_time=datetime.datetime.now(tz = tz).strftime(fmt)   
                    val2.configure(text=now_time)
                    val2.after(60000,time_update,weather_data) # after dùng để lặp lại cái hàm này sau khoảng thời gian
            #3. Hàm lấy thời gian thực(GMT time) 

        def time_fetched(weather_data):
                    fmt = "%b,%d %H:%M" # dạng ví dụ Feb.12 12:20
                    time=weather_data.json()['timezone']
                    tz = datetime.timezone(datetime.timedelta(seconds=int(time))) #chuyển timedelta thành timezone
                    now_time=datetime.datetime.now(tz = tz).strftime(fmt) #strftime dùng để thể hiện thời gian ở dạng
                    val1.configure(text=now_time)
             

            #4. Hàm fetch data từ open weather api(qua ô tìm kiếm)
       

        def city_search(x):
                print('enter press')    
                weather_data=requests.get(               #request dùng để gửi một yêu cầu http, trong trường hợp này sẽ là GET      
                    f"https://api.openweathermap.org/data/2.5/weather?q={x}&units=imperial&APPID={apikey}"
                    )
                if weather_data.json()['cod'] == '404': #kiểm tra thành phố có tồn tại
                    messagebox.showerror("ERROR", "City not found !") 
                else:
                    fetch_weather_conditions(weather_data,x) 
            #4. Hàm fetch data từ open weather api(qua vị trí bản thân)                                     
    
                    
        def initial_city_search():
            weather_data=requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q={g.city.lower()}&units=imperial&APPID={apikey}"
                    )
            if weather_data.json()['cod'] == '404':
                    messagebox.showerror("ERROR", "City not found !") 
            else:
                    
            
                    fetch_weather_conditions(weather_data,g.city.lower())
        
            time_update(weather_data)
        initial_city_search()  
        
          
