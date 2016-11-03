from tkinter import *
import pickle, ssl, urllib.request

# 检查
def check(f_station, t_station, d):
    warning_text = ''
    with open('citylist.data','rb') as f:
        city_list = pickle.load(f)
        temp = city_list.keys()

    # 出发车站检查
    if f_station in temp:
        f_station = city_list[f_station]
    else:
        warning_text += '输入出发车站名有误\n'
        from_station.delete(0,END)

    # 到达车站检查
    if t_station in temp:
        t_station = city_list[t_station]
    else:
        warning_text += '输入到达车站名有误\n'
        to_station.delete(0,END)

    # 日期格式检查
    temp = re.compile(r'[\d]{4}-[\d]{2}-[\d]{2}')
    if temp.match(d) == None:
        warning_text += '输入日期格式错误，例：（2016-01-01）'
        date.delete(0,END)
    else:
        d = temp.match(d).group()[:10]
        date.delete(0,END)
        date.insert(0,d)
        return f_station, t_station, d, warning_text

def warning(text):
    top = Toplevel()
    top.title('出错了')
    Message(top,text=text,width=230,anchor=CENTER,justify=CENTER,padx=30,pady=10).pack()

def result(train):
    root = Tk()
    root.title('查询结果')
    Label(root,text='车次').grid(row=0,column=1,rowspan=2)
    Label(root,text='始发车站').grid(row=0,column=2)
    Label(root,text='终点站').grid(row=1,column=2)
    Label(root,text='出发时间').grid(row=0,column=3)
    Label(root,text='到达时间').grid(row=1,column=3)
    Label(root,text='历时').grid(row=1,column=4)
    Label(root,text='余票情况').grid(row=0,column=5,columnspan=11)
    Label(root,text='商务座').grid(row=1,column=5)
    Label(root,text='特等座').grid(row=1,column=6)
    Label(root,text='一等座').grid(row=1,column=7)
    Label(root,text='二等座').grid(row=1,column=8)
    Label(root,text='高级软卧').grid(row=1,column=9)
    Label(root,text='软卧').grid(row=1,column=10)
    Label(root,text='硬卧').grid(row=1,column=11)
    Label(root,text='软座').grid(row=1,column=12)
    Label(root,text='硬座').grid(row=1,column=13)
    Label(root,text='无座').grid(row=1,column=14)
    Label(root,text='其他').grid(row=1,column=15)
    Label(root,text='状况').grid(row=0,column=16,rowspan=2)

    x = 1
    for each in train:
        x *= 2
        Label(root,text=each['station_train_code']).grid(row=x,column=1,rowspan=2)
        Label(root,text=each["start_station_name"]).grid(row=x,column=2)
        Label(root,text=each['end_station_name']).grid(row=x+1,column=2)
        Label(root,text=each['start_time']).grid(row=x,column=3)
        Label(root,text=each['arrive_time']).grid(row=x+1,column=3)
        Label(root,text=each['lishi']).grid(row=x,column=4,rowspan=2)
        Label(root,text=each['swz_num']).grid(row=x,column=5,rowspan=2)
        Label(root,text=each['tz_num']).grid(row=x,column=6,rowspan=2)
        Label(root,text=each['zy_num']).grid(row=x,column=7,rowspan=2)
        Label(root,text=each['ze_num']).grid(row=x,column=8,rowspan=2)
        Label(root,text=each['gr_num']).grid(row=x,column=9,rowspan=2)
        Label(root,text=each['rw_num']).grid(row=x,column=10,rowspan=2)
        Label(root,text=each['yw_num']).grid(row=x,column=11,rowspan=2)
        Label(root,text=each['rz_num']).grid(row=x,column=12,rowspan=2)
        Label(root,text=each['yz_num']).grid(row=x,column=13,rowspan=2)
        Label(root,text=each['wz_num']).grid(row=x,column=14,rowspan=2)
        Label(root,text=each['qt_num']).grid(row=x,column=15,rowspan=2)
        Label(root,text=each['controlled_train_message']).grid(row=x,column=16,rowspan=2)
        x += 1
            
    mainloop()

def get_data(temp):
    ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date='+temp[2]+'&leftTicketDTO.from_station='+temp[0]+'&leftTicketDTO.to_station='+temp[1]+'&purpose_codes='+temp[3]
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        }
    req = urllib.request.Request(url, headers = headers)
    response = urllib.request.urlopen(req)
    response = response.read().decode('utf-8')
    select = re.compile(r'{"queryLeftNewDTO".+?}')
    train = select.finditer(response)
    for each in train:
        each = each.group()[19:]
        each = eval(each)
        yield each

def submit(): 
    f_station = from_station.get()
    t_station = to_station.get()
    d = date.get()
    types = v.get()
    if types == 0:
        types = 'ADULT'
    else:
        types = '0X00'
    check_result = check(f_station, t_station, d)
    f_station, t_station, d, warning_text = check_result[0],check_result[1],check_result[2],check_result[3]
    if warning_text != '':
        warning(warning_text)
    else:
        temp=[f_station,t_station,d,types]
        train = get_data(temp)
        result(train)

def main():
    global from_station, to_station, date, button, v
    root = Tk()
    root.title('火车票查询软件')
    frame = Frame()
    # 创建框架
    Label(frame,text='出发车站：').grid(row=0,column=1)
    Label(frame,text='到达车站：').grid(row=1,column=1)
    Label(frame,text='出发日期：').grid(row=2,column=1)
    from_station = Entry(frame)
    to_station = Entry(frame)
    date = Entry(frame)
    from_station.insert(0,'北京')
    to_station.insert(0,'上海')
    date.insert(0,'2016-01-01')
    from_station.grid(row=0,column=2,padx=5,pady=5)
    to_station.grid(row=1,column=2,padx=5,pady=5)
    date.grid(row=2,column=2,padx=5,pady=5)
    frame.pack(padx=30,pady=10)
    v=IntVar()
    v.set('0')
    Radiobutton(frame,text='成人',variable=v,value=0).grid(row=4,column=1)
    Radiobutton(frame,text='学生',variable=v,value=1).grid(row=4,column=2)
    button = Button(frame,text='查询',command=submit,width=30)
    button.grid(row=5,column=1,columnspan=2,padx=5,pady=5)
    mainloop()
main()
