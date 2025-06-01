#链表
class ListNode:
    def __init__(self,val,nxt=None,prv=None):
        self.val=val
        self.nxt=nxt
        self.prv=prv
class LinkedList:
    #双向链表，可模拟栈、队列等线性结构
    def __init__(self):
        self.head=None
        self.tail=None
    #其余两个方向同理,prv往head方向，nxt往tail方向
    #某一固定方向删除元素、添加元素等，参照该代码
    #注意避免低级错误，别少删一条边或者少增一条边
    def add(self,node:ListNode,innernode:ListNode=None):
        #把节点node添加到innernode之后，别忘了
        if not self.head:self.head=node
        if self.tail==innernode:self.tail=node
        n:ListNode=innernode.nxt
        node.nxt=n
        node.prv=innernode
        if innernode:innernode.nxt=node
        if n:n.prv=node
    def remove(self,node:ListNode):
        #从链表中删除某个给定节点
        if node.prv:node.prv.nxt=node.nxt
        else:self.head=node.nxt
        node.prv=None
        if node.nxt:node.nxt.prv=node.prv
        else:self.tail=node.prv
        node.nxt=None
#前序表达式 - 1 + 2 3
#中序表达式 1 -(2 + 3)
#后序表达式 1 2 3 + -

#补充一个小知识:在Python中算符的优先级是：
#**>~ + -（指正负）>* / % //>+ -（加减）> "<< >>"（用二进制的时候注意避免低级错误:算2k+1时应是(k<<1)+1而非k<<1+1,后者是k<<2）
#> & > ^| (6^4&3==6(!=2))> "<= < > >=" > == != >:=等赋值运算符 (a:=5==5 a==True使用赋值表达式时需要加括号！)
#>is/is not>in/not in >not>and>or
class Solution:
    #本章常见算法合集
    def parse_exp(self,s:str):
        #如果表达式是错的，则系统会报错,一元运算符用"#"标注,并且不考虑赋值运算符和is not以及not in
        lst:list[str]=[]
        l=0
        #拆分表达式：把小数点看做数值的一部分，遇到数值放到辅助栈中，直到遇到非数值为止；
        while l<len(s):
            if s[l].isdigit() or s[l]=='.':
                for r in range(l,len(s)):
                    if not s[r].isdigit() and s[r]!='.':break
                if s[r].isdigit():r+=1
                lst.append(s[l:r])
                l=r
            #遇到括号，单独处理
            elif s[l] in '()':
                lst.append(s[l])
                l+=1
            elif s[l]==' ':l+=1
            #遇到字母，则找到下一个空格或者非字母字符作为分隔符
            elif s[l].isalpha():
                for r in range(l,len(s)):
                    if not s[r].isalpha():break
                lst.append(s[l:r])
                l=r
            #遇到运算符，如果后一个是运算符，那么如果下一个不是~+-则认为是与前一个符号共同构成运算符，
            elif s[l+1] not in '(. )~+-' and not s[l+1].replace(".",'').isalnum():
                lst.append(s[l:l+2])
                l+=2
            #下一个是其他则认为是一元运算符
            else:
                lst.append(s[l])
                l+=1
        #处理一元运算符,not
        for i in range(len(lst)-1):
            if lst[i]=='not':lst[i]='#not'
            if not lst[i].replace('.','').isalnum() and not lst[i+1].replace('.','').isalnum() and lst[i]  not in '()' and lst[i+1] not in '()':
                lst[i+1]='#'+lst[i+1]
        return lst
    def inorder_to_postorder(self,s:str):
        #我们考虑的后序表达式，把一元运算符紧邻地写在变量之前
        #运算符能打掉同级运算符和比他高级的运算符，同时，右括号能打掉左括号之前的所有运算符
        lst=Solution().parse_exp(s)
        pred={'**':1,"#~":2,"#+":2,'#-':2,"*":3,'/':3,'%':3,'//':3,'+':4,'-':4,'>>':5,'<<':5,'&':6,
              '^':7,'|':7,'<=':8,'<':8,'>':8,'>=':8,'==':9,'!=':9,'#not':10,'and':11,'or':12}
        ops=[]
        res=[]
        for i in lst:
            if i==')':#括号
                while ops[-1]!='(':res.append(ops.pop())
                ops.pop()
                continue
            if i=='(':
                ops.append(i)
                continue
            if i not in pred and i!='(':#操作数
                res.append(i)
                continue
            tmp=pred[i]
            while ops and ops[-1]!='(' and pred[ops[-1]]<tmp:#其余运算符
                res.append(ops.pop())
            ops.append(i)
        newlst=[]
        for i in res:
            if i[0]!='#':
                newlst.append(i)
                continue
            newlst.append(i[1:]+newlst.pop())
        return ' '.join(newlst)

print(Solution().inorder_to_postorder("2>>1+~3*(5--6)<=2**3&4 and(not False or True and True)"))
