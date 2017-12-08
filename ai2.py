import copy

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










    ###################################


    #ai
def ai(board,player):
    if player.number==1:
        enemy=2
    else:
        enemy=1
    my_tuple=find_best(board,player.number)#自己的分数
    enemy_tuple=find_best(board,enemy)#对手的分数
    if my_tuple[2]*2.5>=enemy_tuple[2]:#进攻
        player.down(board,my_tuple[0],my_tuple[1])
    else:#防守
        player.down(board,enemy_tuple[0],enemy_tuple[1])






#在棋盘所有空位模拟落子并寻找得分最大的空位,返回（x,y,max_score)
def find_best(board,player_number):
    max_score=0
    for i in range(board.row):
        for j in range(board.column):
            if board.boa[i][j]!=1 and board.boa[i][j]!=2:
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

                if score>=max_score:
                    max_score=score
                    x=j
                    y=i
    return (x,y,max_score)