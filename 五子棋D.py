
#五子棋
#Ver1.0 :新增下到有棋子的地方错误提示 
#Ver1.1.1:新增显示轮到谁下棋功能
#Ver1.1.2:修复了白棋先行以及当前下棋一方显示错误的问题
#         修复了有些区域连成5子不会判定为胜利的问题
#Ver1.1.4:新增输入判断功能，输入错误时会要求重新输入
#Ver1.1.5:加入定制棋盘大小功能
#Ver1.1.5.2:加入棋盘行数列数不超过10的提示
#Ver1.1.6.0:加入悔棋功能，改变了棋子的显示效果
#Ver1.1.7.2: 增加棋盘大小上限到63*63，行列序号改为ASCII码表，修复了之前版本白棋先行以及当前下棋一方显示错误的问题
#Ver1.2.1.0: 程序结构改为面向对象,简化坐标输入,新增必胜秘籍'daddy'
#Ver1.2.1.2: 加入下满棋子平局功能
#Ver2.0.0: 加入人机对战模式(电脑执黑棋)
#Ver2.0.0.2:修复了上个版本双人对战运行错误的bug
#Ver3.0.0(demo)界面从控制台升级为图形界面，通过点击下棋。（暂时只有电脑先手的人机对战模式，尚未加入悔棋功能）
#	已知BUG:同一地方可以重复下棋

import copy
import os
from tkinter import *
import Dtree2

#判断某一点连子数目
def many(boa,n,i,j):
	if not(boa[i][j]==n):#判断是否是该棋子
		return 0
	else:
		n1=n2=n3=n4=1
		a=i
		b=j
		for k in range(5):#竖直
			x=boa[a][b]
			a+=1
			if a>row-1:
				break
			if x==boa[a][b]:
				n1+=1
			else:
				break
		a=i
		b=j 
		for k in range(5):#水平
			x=boa[a][b]
			b+=1
			if b>column-1:
				break
			if x==boa[a][b]:
				n2+=1
			else:
				break
		a=i
		b=j
		for k in range(5):#左上到右下
			x=boa[a][b]
			a+=1
			b+=1
			if a>row-1 or b>column-1:
				break
			if x==boa[a][b]:
				n3+=1
			else:
				break
		a=i
		b=j
		for k in range(5):#右上到左下
			x=boa[a][b]
			a+=1
			b-=1
			if a>row-1 or b<0:
				break
			if x==boa[a][b]:
				n4+=1
			else:
				break
		
	return max(n1,n2,n3,n4)

#将传入的字符串进行处理，等于number的数字转化为1,不等于的转化为2，其他转化为0
def str_deal(str1,number):
	result=''
	for x in str1:
		if x=='1' or x=='2':
			if x==str(number):
				result+='1'
			else:
				result+='2'
		else:
			result+='0'
	return result




#给传入的字符串打分,0表示空格，1表示己方棋子，2表示敌方棋子，未考虑跳眠三，跳眠二，大跳活二
def point(str1):
	str2=str1[::-1]
	if '11111' in str1 or '11111' in str2:#五连
		return 1000
	elif '011110' in str1 or '011110' in str2:#活四
		return 100
	elif '011101' in str1 or '011101' in str2:#跳活四情形1
		return 16
	else:
		for x in ('011112','101112','110112','111012'):#冲四
			if x in str1 or x in str2:
				return 15
		if '011100' in str1 or '011100' in str2:#连活三
			return 15
		if '010110' in str1 or '010110' in str2:#跳活三
			return 10
		if '001112' in str1 or '001112' in str2:#眠三
			return 2
		for x in ('011000','001100'):#连活2
			if x in str1 or x in str2:
				return 2
		if '010100' in str1 or '010100' in str2:#跳活二
			return 1
		if '000112' in str1 or '000112' in str2:#眠二
			return 0.2
	return 0


	




#判断下在某一点的分数
def one_score(board,player_number,i,j):
	score=0
	fake=copy.deepcopy(board.boa)#复制棋盘
	fake[i][j]=player_number#模拟落子
	#限定这次落子可能影响的范围
	up=max(i-5,0)
	down=min(i+5,board.row-1)
	left=max(j-5,0)
	right=min(j+5,board.column-1)
	#往4个角的长度
	leftup=min(j-left,i-up)
	leftdown=min(j-left,down-i)
	rightup=min(right-j,i-up)
	rightdown=min(right-j,down-i)

	u_d=l_r=lu_rd=ru_ld=''
	#将四个方向的棋子序列转化为字符串
	for k in range(up,down+1):#竖直方向
		u_d+=str(fake[k][j])
	for k in range(left,right+1):#水平方向
		l_r+=str(fake[i][k])
	for k in range(leftup,0,-1):#左上到右下
		lu_rd+=str(fake[i-k][j-k])
	for k in range(rightdown+1):
		lu_rd+=str(fake[i+k][j+k])
	for k in range(rightup,0,-1):
		ru_ld+=str(fake[i-k][j+k])#右上到左下
	for k in range(leftdown+1):
		ru_ld+=str(fake[i+k][j-k])

	#转化为point函数能处理的格式
	u_d=str_deal(u_d,player_number)
	l_r=str_deal(l_r,player_number)
	lu_rd=str_deal(lu_rd,player_number)
	ru_ld=str_deal(ru_ld,player_number)


	#计算总分数
	for k in (u_d,l_r,lu_rd,ru_ld):
		score+=point(k)
	return score

#计算敌我在这一点的分数并且相加
def find_best(board,player_number):    
	if board.n==1:
		return (board.row//2,board.column//2,0)
	if player_number==1:
		enemy=2
	else:
		enemy=1
	max_score=0
	for i in range(board.row):
		for j in range(board.column):
			if board.boa[i][j]!=1 and board.boa[i][j]!=2:
				my_score=one_score(board,player_number,i,j)
				enemy_score=one_score(board,enemy,i,j)
				score=my_score*2.5+enemy_score
				if score>=max_score:
					max_score=score
					x=j
					y=i
	return (x,y,max_score)

#棋盘类
class Board():
	def __init__(self,row,column):
		self.row=row
		self.column=column
		self.boa=[[0 for i in range(column)] for j in range (row)]
		self.history=[]
		self.n=1#步数
		self.flag=0#胜方 0无，1黑，2白,3平
	#初始化棋盘
	def reset(self):
		for i in self.row:
			for j in self.column:
				self.boa[i][j]=0
		self.history.append(copy.deepcopy(self.boa))
#玩家类
class Player():
	#玩家序号
	def __init__(self,number):
		self.number=number

	#下棋
	def down(self,board,x,y):
		board.boa[y][x]=self.number
		board.history.append(copy.deepcopy(board.boa))
		board.n=board.n+1
		
class GUI():
	def __init__(self,row,column,mode):
		self.row=row
		self.column=column
		self.mode=mode
		self.board=Board(self.row,self.column)
		self.player1=Player(1)
		self.player2=Player(2)
		self.root=Tk()
		self.root.title('五子棋')

		self.canvas=Canvas(self.root,width=self.column*50+10,height=self.row*50+10,bg='Green')#创建画布
		for i in range(self.row):
			self.canvas.create_line((30,i*50+30),(50*(self.column-1)+30,i*50+30),width=2)#画线
		for i in range(self.column):
			self.canvas.create_line((i*50+30,30),(i*50+30,50*(self.row-1)+30),width=2)
		self.canvas.bind('<Button-1>',self.down)#绑定左键点击事件
		self.canvas.pack()
		if self.mode=='1':#人机对战
			Dtree2.ai(self.board,self.player1)#第一步
			self.show()

		self.root.mainloop()
	def show(self):	
		self.canvas.delete("all")
		for i in range(self.row):
			self.canvas.create_line((30,i*50+30),(50*(self.column-1)+30,i*50+30),width=2)#画线
		for i in range(self.column):
			self.canvas.create_line((i*50+30,30),(i*50+30,50*(self.row-1)+30),width=2)
		
		for i in range(self.row):#画棋子
			for j in range(self.column):
				if self.board.boa[i][j]==1:
					self.canvas.create_oval(((j)*50+8,(i)*50+8),((j+1)*50+2,(i+1)*50+2),fill='black')#黑棋
				elif self.board.boa[i][j]==2:
					self.canvas.create_oval(((j)*50+8,(i)*50+8),((j+1)*50+2,(i+1)*50+2),fill='white')#白棋
		self.canvas.update()
	def down(self,event):
		if self.board.flag==0:
			x=round((event.x-30)/50)
			y=round((event.y-30)/50)
			if self.board.n%2==1:
				self.player1.down(self.board,x,y)
			else:
				self.player2.down(self.board,x,y)
			self.show()
			self.judge()
			if self.mode=='1':
				Dtree2.ai(self.board,self.player1)
				self.show()
				self.judge()
		#判断胜负
	def judge(self):
		for i in range(0,self.row):
			for j in range(0, self.column):
				how_many=many(self.board.boa,1,i,j)
				if how_many==5:
					self.board.flag=1
					self.canvas.create_text(self.column//2*50,self.row//2*50,fill='Red',text='黑方胜利')
				how_many=many(self.board.boa,2,i,j)
				if how_many==5:
					self.board.flag=2
					self.canvas.create_text(self.column//2*50,self.row//2*50,fill='Red',text='白方胜利')

		n=0#棋盘上的棋子数量
		for i in range(0,self.row):
			for j in range(0,self.column):
				if(self.board.boa[i][j]==1 or self.board.boa[i][j]==2):
					n=n+1

		if n==self.row*self.column:
			self.flag=3
			self.canvas.create_text(self.column//2*50,self.row//2*50,fill='Red',text='平局')

row=int(input('请输入棋盘行数（不超过63,建议不超过26）：'))#行，列
assert type(row)==int and 0<=row<=63
column=int(input('请输入棋盘列数（不超过63，建议不超过26）：'))
assert type(column)==int and 0<=row<=63
mode='1'

gui=GUI(row,column,mode)







		
		
		
		
	
	
