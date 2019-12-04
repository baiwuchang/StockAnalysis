import trend_following_strategy as td
from tkinter import *
from tkinter import ttk
import calender

BG_X = 1600 #窗口宽度
BG_Y = 1000 #窗口高度

class Client:
	def __init__(self, master):
		self.master = master
		
		self.cv = Canvas(self.master, width = BG_X, height = BG_Y, background = 'white')
		self.cv.place(relx = 0.5, rely = 0.5, x = -BG_X / 2, y = -BG_Y / 2)
		self.cv.focus_set()

		#还要把控件位置写成相对的，现在是写死的============================================================================！！！
		#开始时间label
		self.lb_start = Label(self.master, text = '开始时间', background = 'white', foreground = 'black', font = ('微软雅黑',18))
		self.lb_start.place(x = 30, y = 30,width =200, heigh = 50)
		#结束时间label
		self.lb_end = Label(self.master, text = '结束时间', background = 'white', foreground = 'black', font = ('微软雅黑',18))
		self.lb_end.place(x = 530, y = 30,width =200, heigh = 50)

		#开始时间输入框
		self.date_start_str = StringVar()
		self.date_start = ttk.Entry(root, textvariable = self.date_start_str)
		self.date_start.place(x = 200, y = 30, width = 200, heigh = 50)
		#结束时间输入框
		self.date_end_str = StringVar()
		self.date_end = ttk.Entry(root, textvariable = self.date_end_str)
		self.date_end.place(x = 700, y = 30, width = 200, heigh = 50)

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
		self.btn_run = Button(self.master, text = 'Start', background = 'yellow', foreground = 'black', font = ('微软雅黑',30))
		self.btn_run.place(width = 200, height = 70, x = 1200, y = 20)
		self.btn_run.bind('<Button-1>', self.run_strategy)

	def run_strategy(self, event):
		#运行策略
		d = self.date_start_str.get()
		start_date = d[0:4] + d[5:7] + d[8:10]
		d = self.date_end_str.get()
		end_date = d[0:4] + d[5:7] + d[8:10]
		#还要加容错，检查输入框是否有内容 以及内容格式对不对============================================================================！！！
		td.run_strategy(start_date, end_date)
		#还要把matplotlib的内容显示到原来的框内，不要弹新的框============================================================================！！！


if __name__ == '__main__':
	root = Tk()
	root.title('趋势跟随策略')
	root.geometry('1600x800+200+50')
	a = Client(root)
	root.mainloop()