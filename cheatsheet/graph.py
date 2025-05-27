from typing import *
import heapq,sys
from collections import deque,defaultdict,Counter
class Vertex:
    #图节点和树节点共用
    def __init__(self,key):
        self.key=key
        self.nbr={}
        self.children=[]#用于最小生成树
        self.parent=self#用于并查集
    def __lt__(self,another):
        return self.key<another.key
    def find_parent(self):
        if self.parent==self:return self
        self.parent=self.parent.find_parent()
        return self.parent
    def __hash__(self):
        return hash(self.key)
class Graph:
    #基本表示
    def __init__(self):
        self.vertices={}
    def add_edge(self,outvert:Vertex,invert:Vertex,wt:int=1):
        outvert.nbr[invert.key]=(wt,invert)
    #图算法
    def topological_order_with_dfs(self):
        visited={}#dict[vertex:int]
        visiting=set()
        unvisited=set(self.vertices.values())#set[vertex]
        def inner(vert:Vertex):
            if vert in unvisited:unvisited.remove(vert)
            if vert in visiting:
                raise TypeError('No topological sort in cyclic graph')
            visiting.add(vert)
            for i in set(vert.nbr.values())&unvisited:
                inner(i)
            visiting.remove(vert)
            visited[len(visited)]=vert
        while unvisited:
            inner(unvisited.pop())
        return ' '.join(visited[i].key for i in range(len(visited)-1,-1,-1))
    def topological_order_with_Kahn(self):
        #入度表
        degree_dic=defaultdict(set)#dict[Vertex,set[Vertex]]
        queue=[]
        for i in self.vertices.values():#dict[str:Vertex]
            queue.append(i)
            for j in i.nbr.values():
                degree_dic[j].add(i)
        queue=deque(queue)
        visited={}#dict[int:Vertex]
        visited_set=set()
        cnt=0
        while queue:
            if cnt==len(queue):
                raise TypeError('No topological sort in cyclic graph')
            a=queue.popleft()
            if degree_dic[a]-visited_set==set():
                visited[len(visited)]=a
                visited_set.add(a)
                cnt=0
                continue
            cnt+=1
            queue.append(a)
        return '\n'.join(visited[i].key for i in range(len(visited)))
    def min_span_tree_prim(self,startvert:Vertex)->int:
        #prim适合稠密图
        #初始化(无向图)
        unvisited=set(self.vertices.values())
        heap=[]
        for wt,adjvert in startvert.nbr.values():
            heap.append((wt,startvert,adjvert))
        heapq.heapify(heap)
        unvisited.remove(startvert)
        treedic={startvert.key:startvert}
        cnt=0
        #每弹出一条边，需要检查边的目标节点是不是没有遍历过，
        #若是则忽略，若否则加入树节点
        while heap:
            wt,outvert,invert=heapq.heappop(heap)
            if invert in unvisited:
                cnt+=wt
                unvisited.remove(invert)
                for wt,adjvert in invert.nbr.values():
                    heapq.heappush(heap,(wt,invert,adjvert))
                treedic[outvert.key].children.append(invert)
                treedic[invert.key]=invert
        return cnt if len(treedic)==len(self.vertices) else -1
    def min_span_tree_kruskal(self):
        #适合稀疏图
        #初始化加载所有的边,不涉及比较的时候直接挂载，涉及比较的时候回溯到祖先节点
        cnt=0
        heap=[]
        for verti in self.vertices.values():
            for wtj,vertj in verti.nbr.values():
                heap.append((wtj,verti,vertj)) 
        heapq.heapify(heap)
        while heap:
            wt,verti,vertj=heapq.heappop(heap)
            if verti.find_parent()==vertj.find_parent():continue
            vertj.find_parent().parent=verti.find_parent()
            cnt+=wt
        return cnt
    def bellman_ford(self,startvert:Vertex):
        dic={vert:float('inf') for vert in self.vertices.values()}
        dic[startvert]=0
        #得到所有的边，在这里，使用遍历顶点的方法
        edges=[]
        for vert in self.vertices.values():
            for wt,adjvert in vert.nbr.values():
                edges.append((vert,adjvert,wt))
        for i in range(len(dic)-1):
            for vert,adjvert,wt in edges:
                if dic[vert]+wt<dic[adjvert]:
                    dic[adjvert]=dic[vert]+wt
        for vert,adjvert,wt in edges:
            if dic[vert]+wt<dic[adjvert]:
                print('存在负权回路')
                return
        return dic
    def spfa(self,startvert:Vertex):
        #正权回路
        dic={vert:float('inf') for vert in self.vertices.values()}
        dic[startvert]=0
        queue=deque([startvert])
        while queue:
            vert=queue.popleft()
            for wt,adjvert in vert.nbr.values():
                if dic[vert]+wt<dic[adjvert]:
                    dic[adjvert]=dic[vert]+wt
                    queue.append(adjvert)
        return dic
    def floyd_warshall(self):
        #多源最短路径,在我们的代码模版中，需要初始化一个映射；但是实际使用的时候不需要
        vertlst=list(self.vertices.values())
        vertdic={vertlst[i]:i for i in range(len(vertlst))}
        dist=[[(float('inf')if i!=j else 0) for i in range(len(vertlst))]for j in range(len(vertlst))]
        for i in range(len(vertlst)):
            for wt,j in vertlst[i].nbr.values():
                dist[i][vertdic[j]]=wt
        #核心算法,注意更新最短路径顺序
        #从0开始
        for i in range(len(vertlst)):
            for j in range(len(vertlst)):
                for k in range(len(vertlst)):
                    if j!=k and dist[k][i]+dist[i][j]<dist[k][j]:
                        dist[k][j]=dist[k][i]+dist[i][j]
        return (vertdic,dist)
    def scc_k(self)->list[set]:
        #第一次dfs
        unvisited=set(self.vertices.values())
        visited=[]
        def dfs(startvert:Vertex):
            nonlocal visited,unvisited
            if startvert in unvisited:unvisited.remove(startvert)
            for wt,adjvert in startvert.nbr.values():
                if adjvert not in unvisited:continue
                dfs(adjvert)
            visited.append(startvert)
        while unvisited:dfs(unvisited.pop())
        scclst:list[set]=[]#list[set]
        unvisited=set(self.vertices.values())
        #构建反向图的邻接表
        reverse_graph=defaultdict(set)#vert.key,set[adjvert]
        for vert in self.vertices.values():
            for wt,adjvert in vert.nbr.values():
                reverse_graph[adjvert.key].add(vert)
        def dfs2(startvert:Vertex):
            nonlocal visited,unvisited,scclst
            unvisited.remove(startvert)
            for adjvert in reverse_graph[startvert.key]:
                if adjvert not in unvisited:continue
                dfs2(adjvert)
            scclst[-1].add(startvert.key)
        while unvisited:
            if (vert:=visited.pop()) in unvisited:
                scclst.append(set())
                dfs2(vert)
        return scclst
    def scc_tarjan(self)->list[set]:
        #强联通单元,并查集写法(疑似tarjan是在研究强联通单元时发明的并查集)
        def union(vert:Vertex,par:Vertex):
            vertp=vert.find_parent()
            parp=par.find_parent()
            if vertp!=parp:vertp.parent=parp
        stack:list[Vertex]=[]
        stack_find=defaultdict(int)
        unvisited=set(self.vertices.values())
        def dfs(startvert:Vertex):
            if startvert in unvisited:unvisited.remove(startvert)
            stack.append(startvert)
            stack_find[startvert]+=1
            for wt,adjvert in startvert.nbr.values():
                if stack_find[adjvert.find_parent()]:#有环
                    for i in range(len(stack)-1,-1,-1):
                        if stack[i].find_parent()==adjvert.find_parent():break
                        union(stack[i],adjvert)
                elif adjvert in unvisited:dfs(adjvert)
            stack.pop()
            stack_find[startvert]-=1
        while unvisited:dfs(unvisited.pop())
        #后期处理
        s=defaultdict(set)
        for i in self.vertices.values():
            s[i.find_parent()].add(i.key)
        return list(s.values())

