import trend_following_strategy as td
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import calender
import datetime
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

BG_X = 1600 #窗口宽度
BG_Y = 900 #窗口高度

class Client:
	def __init__(self, master):
		self.master = master
		
		self.cv = Canvas(self.master, width = BG_X, height = BG_Y, background = 'white')
		self.cv.place(relx = 0.5, rely = 0.5, x = -BG_X / 2, y = -BG_Y / 2)
		self.cv.focus_set()
		self.cv.create_rectangle(0,0,1600,110,fill = 'lightgray')

		#还要把控件位置写成相对的，现在是写死的============================================================================！！！
		#开始时间label
		self.lb_start = Label(self.master, text = '开始时间', background = 'lightgray', foreground = 'black', font = ('微软雅黑',18),)
		self.lb_start.place(x = 30, y = 30,width =200, heigh = 50)
		#结束时间label
		self.lb_end = Label(self.master, text = '结束时间', background = 'lightgray', foreground = 'black', font = ('微软雅黑',18))
		self.lb_end.place(x = 530, y = 30,width =200, heigh = 50)

		#开始时间输入框
		self.date_start_str = StringVar()
		self.date_start = ttk.Entry(root, textvariable = self.date_start_str)
		self.date_start.place(x = 200, y = 30, width = 200, heigh = 50)
		#结束时间输入框
		self.date_end_str = StringVar()
		self.date_end = ttk.Entry(root, textvariable = self.date_end_str)
		self.date_end.place(x = 700, y = 30, width = 200, heigh = 50)

		#self.date_start_str.set('2014-01-02')
		#self.date_end_str.set('2019-10-01')

		#Calendar((x, y), 'ur').selection() 获取日期，x,y为点坐标
		#开始时间日历函数
		date_start_str_gain = lambda: [
			self.date_start_str.set(date)
			for date in [calender.Calendar((300,300), 'ur').selection()] 
			if date]
#		#结束时间日历函数
		date_end_str_gain = lambda: [
			self.date_end_str.set(date)
			for date in [calender.Calendar((800,300), 'ur').selection()] 
			if date]

		#选择按钮
		self.btn_choice_start_date = Button(self.master, text = '选择', command = date_start_str_gain, font = ('微软雅黑',18))
		self.btn_choice_start_date.place(x = 400, y = 30, width = 100, heigh = 50)
		self.btn_choice_end_date = Button(self.master, text = '选择', command = date_end_str_gain, font = ('微软雅黑',18))
		self.btn_choice_end_date.place(x = 900, y = 30, width = 100, heigh = 50)

		#运行按钮
		self.btn_run = Button(self.master, text = '开始模拟', background = '#FFCC33', foreground = 'black', font = ('微软雅黑',24))
		self.btn_run.place(x = 1100, y = 25, width = 200, height = 60)
		self.btn_run.bind('<Button-1>', self.run_strategy)

	def run_strategy(self, event):
		#运行策略
		#开始输入框容错检测
		can_run = True #检查输入框的内容
		d = self.date_start_str.get()
		start_date = d[0:4] + d[5:7] + d[8:10]
		if not self.check_date(start_date): #检查输入框的内容
			can_run = False
			showinfo('日期错误','起始日期格式不正确。\n格式示例：“2014-03-03”\n起始日期应位于“2014-01-02”和“2019-10-08”之间')

		if can_run:
			d = self.date_end_str.get()
			end_date = d[0:4] + d[5:7] + d[8:10]
			if not self.check_date(end_date): #检查输入框的内容
				can_run = False
				showinfo('日期错误','终止日期格式不正确。\n格式示例：“2014-03-03”\n终止日期应位于“2014-01-02”和“2019-10-08”之间')
		if can_run:
			if datetime.date(int(start_date[0:4]),int(start_date[4:6]),int(start_date[6:8])).__gt__(datetime.date(int(end_date[0:4]),int(end_date[4:6]),int(end_date[6:8]))):
				can_run = False #检查输入框的内容
				showinfo('日期错误','起始日期大于终止日期')
		#检测完毕

		if can_run:
			self.fig, self.ax, self.fig2, self.ax2= td.run_strategy(start_date, end_date) #('20141201', '20141204')
			self.switcher = 1
			self.show_graph1(1)

			

	def check_date(self,d): #检查输入框的内容
		if len(d) != 8:
			return False
		if not d.isdigit():
			return False
		date = datetime.date(int(d[0:4]),int(d[4:6]),int(d[6:8]))
		s = datetime.date(2014,1,2)
		e = datetime.date(2019,10,8)
		if date.__lt__(s) or date.__gt__(e):
			return False
		return True

	def show_graph1(self, event):
		self.canvas1 = FigureCanvasTkAgg(self.fig, master=root)
		self.canvas1.draw()  # 注意show方法已经过时了,这里改用draw
		self.toolbar1 = NavigationToolbar2Tk(self.canvas1, root) # matplotlib的导航工具栏显示上来(默认是不会显示它的)
		self.toolbar1.update()
		self.canvas1.get_tk_widget().place(x = 0, y = 120, width = 1600, height = 760)  # get_tk_widget()得到的就是_tkcanvas
		self.btn_switch = Button(self.master, text = '切换至持仓图', background = '#F2F2F2', foreground = '#FF9900', font = ('微软雅黑',18))
		self.btn_switch.place(width = 180, height = 50, x = 1400, y = 115)
		self.btn_switch.bind('<Button-1>', self.switch_graph)

	def show_graph2(self, event):
		self.canvas2 = FigureCanvasTkAgg(self.fig2, master=root)
		self.canvas2.draw()  # 注意show方法已经过时了,这里改用draw
		self.toolbar2 = NavigationToolbar2Tk(self.canvas2, root) # matplotlib的导航工具栏显示上来(默认是不会显示它的)
		self.toolbar2.update()
		self.canvas2.get_tk_widget().place(x = 0, y = 120, width = 1600, height = 760)  # get_tk_widget()得到的就是_tkcanvas
		self.btn_switch = Button(self.master, text = '切换至账户图', background = '#F2F2F2', foreground = '#FF9900', font = ('微软雅黑',18))
		self.btn_switch.place(width = 180, height = 50, x = 1400, y = 115)
		self.btn_switch.bind('<Button-1>', self.switch_graph)

	def switch_graph(self, event): #两图切换
		if(self.switcher == 1): #换成图2
			self.switcher = 2	
			self.canvas1._tkcanvas.place_forget()
			self.toolbar1.destroy() #删除掉原来的工具栏，不然会有两个
			self.show_graph2(1)
		else: #换成图1
			self.switcher = 1
			self.canvas2._tkcanvas.place_forget()
			self.toolbar2.destroy() #删除掉原来的工具栏，不然会有两个
			self.show_graph1(1)
	                      
if __name__ == '__main__':
	root = Tk()
	root.title('趋势跟随策略')
	root.geometry('1600x900+200+50')
	root.resizable(0,0) #固定窗口大小
	a = Client(root)
	root.mainloop()