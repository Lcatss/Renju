import copy
import time

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




#给传入的字符串打分,0表示空格，1表示己方棋子，2表示敌方棋子
def point(str1):
	str2=str1[::-1]
	if '11111' in str1 or '11111' in str2:#五连
		return 1000
	elif '011110' in str1 or '011110' in str2:#活四
		return 100
	elif '011101' in str1 or '011101' in str2:#跳活四情形1
		return 16
	else:
		for x in ('01111','10111','11011'):#冲四
			if x in str1 or x in str2:
				return 15
		if '011100' in str1 or '011100' in str2:#连活三
			return 15
		if '010110' in str1 or '010110' in str2:#跳活三
			return 10
		for x in ('01011','10011','00111','10101','10110','01110'):#眠三
			if x in str1 or x in str2:
				return 1.5
		for x in ('011000','001100'):#连活2
			if x in str1 or x in str2:
				return 1.5
		if '010100' in str1 or '010100' in str2:#跳活二
			return 1
		if '010010' in str1 or '010010' in str2:#大跳活二
			return 0.8
		for x in ('00011','01001','01010','10001','00101','00110'):#眠二
			if x in str1 or x in str2:
				return 0.15
	return 0

#判断下在某一点的分数
def one_score(node):
	player_number=node.getPlayer_number()
	score=0
	fake=node.getValue()
	i,j=node.getPlace()
	#限定这次落子可能影响的范围
	up=max(i-5,0)
	down=min(i+5,len(fake)-1)
	left=max(j-5,0)
	right=min(j+5,len(fake[0])-1)
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





#计算从根节点到这个节点改变的分数
def point_path(node):
	if node.getParent():
		return one_score(node)-point_path(node.getParent())
	else:
		return 0




########################################################







class tree():
	number=0
	def __init__(self,value,player_number):
		self.value=value
		self.parent=None
		self.children=[]
		self.place=None#记录从父节点到此节点下棋的位置
		self.player_number=player_number
		tree.number+=1
	def setChildren(self,node,place):
		self.children.append(node)
		node.setParent(self,place)
	def setParent(self,node,place):
		self.parent=node
		self.place=place
	def getChildren(self):
		return self.children
	def getValue(self):
		return self.value
	def getParent(self):
		return self.parent
	def getPlace(self):
		return self.place
	def getPlayer_number(self):
		return self.player_number
	def __str__(self):
		return str(self.value)


def enemy_number(n):
	if n==1:
		return 2
	if n==2:
		return 1

#判断一个位置离已有棋子的距离是否大于1格,i,j不能超出棋盘范围
def distance(boa,i,j):
	assert 0<=i<=len(boa) and 0<=j<=len(boa[0])
	for y in range(i-2,i+3):
		for x in range(j-2,j+3):
			try:
				if (boa[y][x]==1 or boa[y][x]==2) and x>0 and y>0:
					if not (abs(y-i)==1 and abs(x-j)==2) or (abs(y-i)==2 and abs(x-j)==1):
					   return True
			except IndexError as e:
				pass
	return False

#判断一点是否为空
def empty(boa,i,j):
	if boa[i][j]==1 or boa[i][j]==2:
		return False
	return True

#模拟落子
def fakeDown(boa,i,j,player_number):
	fake=copy.deepcopy(boa)#复制棋盘
	fake[i][j]=player_number#模拟落子
	return fake

#极大极小搜索，alpha-beta剪枝
def search(node,player_number,step,high):
	highest=-10000
	if step==0:
		here=node
		return point_path(here)
	else:
		here=node
		boa=node.getValue() 
		for x in better(boa,player_number):
			i,j=x 
			fake=fakeDown(boa,i,j,player_number)
			child=tree(fake,player_number)
			here.setChildren(child,(i,j))

			score=search(child,enemy_number(player_number),step-1,highest)
			
			if score>-high:
				return -score
			elif score>highest:
				highest=score
		return -highest


# #极大极小dfs搜索决策树
# def search(node,point,high):
#   best=None
#   highest=-10000
#   visited=0
#   if node.getChildren():
#       for child in node.getChildren():
#           score=search(child,point,highest)
#           if score>-high:
#               return -score
#           elif score>highest:
#               highest=score
#       return -highest
#   else:
#       return point(node)

#启发函数，对所有可能点进行排序，返回一个list
def better(boa,player_number):
	a=time.clock()
	L=[]
	L1=[]
	L2=[]
	for i in range(len(boa)):
		for j in range(len(boa[0])):
			if distance(boa,i,j) and empty(boa,i,j):
				fake=fakeDown(boa,i,j,player_number)
				here=tree(fake,player_number)
				here.place=(i,j)
				tree.number-=1
				L1.append((one_score(here),(i,j)))
				fake=fakeDown(boa,i,j,enemy_number(player_number))
				here=tree(fake,enemy_number(player_number))
				here.place=(i,j)
				tree.number-=1
				L2.append((one_score(here),(i,j)))

	L1.sort(reverse=True)
	L2.sort(reverse=True)
	for x in range(2):
		L.append(L1[x][1])
		L.append(L2[x][1])
	b=time.clock()
	return L





#寻找返回路径
def trace(node):
	if node.getParent():
		return trace(node.getParent())+[node]
	else:
		return [node]
# 根据搜索找到的最大分数返回第一步下的位置
def Dplace(boa,player_number,step):
	highest=-10000
	best=None
	here=tree(boa,enemy_number(player_number))
	for x in better(boa,player_number):
		i,j=x 
		fake=fakeDown(boa,i,j,player_number)
		child=tree(fake,player_number)              
		here.setChildren(child,(i,j))
		score=search(child,enemy_number(player_number),step-1,highest)
		if score>highest:
			highest=score
			best=child
	print('highest:',highest)
	return best.getPlace()

def ai(board,player):
	tree.number=0   
	start_build=time.clock()    
	i,j=Dplace(board.boa,player.number,4)
	end_build=time.clock()  
	print('节点数共计:',tree.number,'用时:',end_build-start_build)
	

	player.down(board,j,i)
	return chr(j+65)+chr(i+65)