from collections import Counter

#二叉树的基本概念
class Treenode:
    def __init__(self,val,left=None,right=None):
        self.val,self.left,self.right=val,left,right
    def traverse(self,method:int):
        #method=0,1,2分别表示前序、中序和后序
        if method==0:print(self.val,end=' ')
        if self.left:self.left.traverse(method)
        if method==1:print(self.val,end=' ')
        if self.right:self.right.traverse(method)
        if method==2:print(self.val,end=' ')
    def level_order(self):
        pass
    def __lt__(self,another):
        return self.val<another.val
    def __str__(self):
        return str(self.val)
    
#所有有关树的概念和表示方法的题目都可以使用递归，没有必要单独说明
#二叉树的应用
class Heap(list):
    def __init__(self):
        super().__init__([0])
    def heapify(self):
        for i in range((len(self)-1)>>1,0,-1):
            self.moveup(i)
    def moveup(self,pos):
        x=self[pos]
        while True:
            newpos=pos<<1
            if newpos|1<len(self) and self[newpos+1]<self[newpos]:newpos|=1
            if newpos>=len(self) or x<self[newpos]:
                self[pos]=x
                break
            self[pos]=self[newpos]
            pos=newpos
    def movedown(self,pos):
        x=self[pos]
        while pos>1:
            newpos=pos>>1
            if self[newpos]<x:break
            self[pos]=self[newpos]
            pos=newpos
        self[pos]=x
    def popleft(self):
        res=self[1]
        if len(self)>2:
            self[1]=self.pop()
            self.moveup(1)
        else:self.pop()
        return res
    def add(self,elem):
        self.append(elem)
        self.movedown(len(self)-1)

class BST:
    def __init__(self):
        self.head:Treenode=None
    def insert(self,elem):
        ptr=self.head
        while True:
            if elem<=ptr.val:
                if ptr.left:ptr=ptr.left
                else:
                    ptr.left=Treenode(elem)
                    return
            elif ptr.right:ptr=ptr.right
            else:
                ptr.right=Treenode(elem)
                return
    def check(self,elem):
        ptr=self.head
        while True:
            if elem==ptr.val:return True
            if elem<ptr.val:
                if not ptr.left:return False
                ptr=ptr.left
                continue
            elif not ptr.right:return False
            ptr=ptr.right
    
class Solution:
    #1.后序表达式建树 1 2 3 + -/1 2 + 3 -
    def parse_tree(self,lst:list[str]):
        stack:list[Treenode]=[]
        head=Treenode(lst[-1])
        stack.append(head)
        for i in lst[-2::-1]:
            stack.append(Treenode(i))
            if stack[-2].right:stack[-2].left=stack[-1]
            else:stack[-2].right=stack[-1]
            if i.replace('.','').isdigit():
                stack[-1].val=float(i)
                stack.pop()
                while stack and stack[-1].left and stack[-1].right:
                    stack.pop()
        return head
    #Huffman编码树
    #函数将返回一个字典和字典下对应的编码,对具体返回的顺序不做要求，只需要是符合条件的Huffman编码
    def huffman_encoding(self,s:str):
        heap=Heap()
        for letter,freq in Counter(s).items():
            heap.append((freq,Treenode({letter})))
        heap.heapify()
        while len(heap)>=3:
            f1,t1=heap.popleft()
            f2,t2=heap.popleft()
            heap.add((f1+f2,Treenode(t1.val|t2.val,left=t1,right=t2)))
        head=heap.popleft()[1]
        decoding_dic={}
        encoding_dic={}
        def dfs(node:Treenode,code:str):
            nonlocal decoding_dic
            if not node.left:
               encoding_dic[node.val.copy().pop()]=code
               decoding_dic[code]=node.val.copy().pop()
               return
            dfs(node.left,code+'0')
            dfs(node.right,code+'1')
        dfs(head,'')
        return decoding_dic,''.join(encoding_dic[i] for i in s)
#avl不整，时间来不及
