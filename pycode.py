from sre_compile import isstring
import pandas as pd
import arabic_reshaper

def arabic(str):
    return arabic_reshaper.reshape(str)[::-1]
daynumber={}
khalafawy="خلفاوي"
road_el_farag="روض الفرج"
professor="ا.د"
Adoctor="ا.م"
doctor="دكتور"
manager =  "رئيس لجنة"
observer = "ملاحظ"
monitor0= "مراقب دور"
dss=[]
mp = {"professor":0,professor:0,Adoctor:1,doctor:2,"Adoctor":1,"doctor":2,"other":3,"road el farag":1 ,"khalafawy":0,road_el_farag:1,khalafawy:0}
class Task(object):
    def __init__(self,day = 0,building = 0,type = observer):
            self.day = day
            self.building = building
            self.type = type

    def select_day(self,d,m,y):
                self.day = d
                self.month = m
                self.year = y

    def print_info (self):
            print(arabic(f'اليوم رقم : {self.day} ، التكليف: {self.type} ، المينى:  {self.building}'))

    def task_place(self):
            return mp[self.building]
    def work_place(self):
            return self.building
        

class Monitor:
    def __init__(self,user_name = "unkhown", title = "employee", work_place = "college", branch = "main",max_days = 0):
        self.user_name = user_name
        self.title = title
        self.work_place = work_place
        self.branch = branch
        self.max_days = max_days
        self.task = []
        self.accupied_days = {
        }

    def append_task(self,new_task):
        self.task.append(new_task)

    def print_info(self):
        print()
        print(arabic("بيانات المكلف"))
        print(arabic( f"الاسم : {self.user_name.capitalize()} "))
        print(arabic(f' المسمى الوظيفى: {self.title}'))
        print(arabic(f'مكان العمل: {self.work_place} '))
        print(arabic(f'المبنى: {self.branch} '))
        print()
        print(arabic("التكليفات: "))

        for task in self.task:
            task.print_info()
        print()
        print('#'*20)
        print()
    def push_info(self,dt,cnt):
        numofworkdays=0
        for i in range(50):
            dt[cnt].append(" ")
            if i in self.accupied_days.keys():
                dt[cnt].append(self.accupied_days[i][1])
                numofworkdays+=1
            else: dt[cnt].append(" ")
        dt[cnt][4]=numofworkdays
        
    def Work_place(self):
        return mp[self.branch]

    def Title(self):
        if(self.title in mp.keys()):return mp[self.title]
        return 3 

class Day:
    def __init__(self,day = 0,obs = 0,monit = 0,manager = 0,building = 0):
        self.day = day
        self.obs = obs
        self.manager = manager
        self.monit = monit
        self.building = building
    def current_day(self):
        x=tuple(self.day.split('/'))
        return daynumber[x]
    
    def observers(self):
        return self.obs

    def Manager(self):
        return self.manager

    def monitor(self):
        return self.monit

    def work_place(self):
        return self.building

def process_single_task(day,tsk,monitors,lst):

	if not monitors:return False

	try:
		if day.current_day() in monitors[lst[0]].accupied_days.keys() :
			return False
	except KeyError:
		pass

	monitors[lst[0]].accupied_days[day.current_day()] = [1,tsk.work_place()]

	if not monitors[lst[0]].max_days:
		lst[1] = lst[0]
		lst[0] = 0

	if not lst[1]:return False
	monitors[lst[0]].append_task(tsk)
	monitors[lst[0]].max_days-=1
	lst[0] = (lst[0] + 1) % lst[1]

	return True

def process(monitors,days):

    monitors = sorted(monitors ,key = lambda monitor : monitor.max_days ,reverse = True)

    employees = {   
        0:{
            2:[[],[]],
            3:[[],[]],
            1:[[],[]],
            0:[[],[]],
        },
        1:{
            2:[[],[]],
            3:[[],[]],
            1:[[],[]],
            0:[[],[]],
        },
    }
    for monitor in monitors:
        employees[monitor.Work_place()][monitor.Title()][1].append(monitor)
    
    for i in employees:
        for j in employees[i]:
            employees[i][j][0] = [0,len(employees[i][j][1])]

    done , ok = 1 , 0
    for day in days:
        for i in range(1,day.observers()+1):
            tsk = Task(day.current_day(),day.work_place(),observer)
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][3][1], 
            employees[tsk.task_place()][3][0])
            if ok:continue
            ok = process_single_task(day, tsk, 
            employees[(tsk.task_place()+1)%2][3][1], 
            employees[(tsk.task_place()+1)%2][3][0])
            if ok:continue
            return False

        for i in range(1,day.monitor()+1):

            tsk = Task(day.current_day(),day.work_place(),monitor0)
            
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][2][1], 
            employees[tsk.task_place()][2][0])
            if ok:continue
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][1][1], 
            employees[tsk.task_place()][1][0])
            if ok:continue
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][0][1], 
            employees[tsk.task_place()][0][0])
            if ok:continue
            return False

        for i in range(1,day.Manager()+1):

            tsk = Task(day.current_day(),day.work_place(),manager)
            employees[tsk.task_place()][0]
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][0][1], 
            employees[tsk.task_place()][0][0])
            if ok:continue
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][1][1], 
            employees[tsk.task_place()][1][0])
            if ok:continue
            
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][2][1], 
            employees[tsk.task_place()][2][0])
            if ok:continue
            return False

        monitors = []
        for i in employees:
            for j in employees[i]:
                for k in employees[i][j][1]:
                    monitors.append(k)
    return True

monitors , days, observser_data_lst = [],[],[]

def read_input(exel_name):
    monitors.clear()
    days.clear()
    observser_data_lst.clear()
    dataframe1 = pd.read_excel(exel_name, na_values = "E",sheet_name='Sheet1')
    col=["الاسم","المسمى الوظيفى","مكان العمل","المبنى","التكليف الحالي"]
    for i in range(50):
        if(not i):
            col.append(" ")
            col.append(" ")
        else:
            col.append(f'يوم {i} وقت')
            col.append(f'يوم {i}')
    observser_data_lst.append(col)
    ok = True
    values= []
    for i in range(5):
        values.append(dataframe1.columns[i])
    print(values)   
    ok &= values ==['nameNN', 'nik', 'job', 'place', 'num']
    if not ok:
        return False
    for index, rows in dataframe1.iterrows():
        my_list =rows.values.tolist()
        observser_data_lst.append(my_list)
    for x in observser_data_lst:
        if(x==observser_data_lst[0]):continue
        monitors.append(Monitor(*x))
    # Day(day number , number of observres , number of monitors,number of managers) needed for that day in total
    # temp=dataframe2.columns
    def srt(elem):
        return (elem[2],elem[1],elem[0])
    dataframe2=pd.read_excel(exel_name,sheet_name='days')
    temp=[]
    day=[]
    cnt=0
    for  x,y in dataframe2.items():
        if(isstring(y[0])):continue
        day.append(tuple(x.split('.')[0].split('/')));
        print(y.values)
        temp=y.values.tolist()
        temp.insert(0,x.split('.')[0])
        # temp.remove(temp[0])
        days.append(temp)
    day = sorted(day, key =srt )
    for x in day:
        if x not in daynumber.keys():
            cnt+=1
            daynumber[x]=cnt 
    print(daynumber)
    for i in range(len(days)):
        days[i]=Day(*days[i])
    print(dataframe1)
    return True
# read_input()
# ok = process(monitors, days)
# cnt=1
# if not ok :
#     print(arabic("عدد الموظفين غير كافى"))
# else:
#     for mon in monitors:
#         mon.push_info(observser_data_lst,cnt)
#         mon.print_info()
#         cnt=cnt+1
#     dataframeout=pd.DataFrame(observser_data_lst)
#     dataframeout.to_excel("observer_output.xlsx")
