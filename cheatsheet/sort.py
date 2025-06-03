#机考除了归并排序之外不太可能用到，但还是整一下...
class Solution:
    def merge_sort(self,lst:list):
        cnt=0
        tmp=[0 for i in range(len(lst))]
        def inner(a:int,b:int):
            if a==b:return
            nonlocal lst,cnt
            m=(a+b)//2
            inner(a,m)
            inner(m+1,b)
            i,j=a,m+1
            while i<=m and j<=b:
                if lst[i]>lst[j]:
                    cnt+=m+1-i
                    tmp[i+j-m-1]=lst[j]
                    j+=1
                else:
                    tmp[i+j-m-1]=lst[i]
                    i+=1
            lst[a:b+1]=tmp[a:i+j-m-1]+lst[i:m+1]+lst[j:b+1]
        inner(0,len(lst)-1)
        return lst,cnt
    def bubble_sort(self,lst:list):
        for i in range(len(lst)-1):
            s=False
            for j in range(len(lst)-1,i,-1):
                if lst[j]<lst[j-1]:
                    lst[j],lst[j-1]=lst[j-1],lst[j]
                    s=True
            if not s:break
        return lst
    def selection_sort(self,lst:list):
        for i in range(len(lst)-1):
            ptr=i
            for j in range(i,len(lst)):
                if lst[j]<lst[ptr]:ptr=j
            lst[i],lst[ptr]=lst[ptr],lst[i]
        return lst
    def insertion_sort(self,lst:list):
        for i in range(1,len(lst)):
            for j in range(i,0,-1):
                if lst[j-1]<=lst[j]:break
                lst[j-1],lst[j]=lst[j],lst[j-1]
        return lst
    def quick_sort(self,lst:list):
        def inner(left,right):
            nonlocal lst
            if left>=right:return
            pivot=lst[right]
            lptr,rptr=left,right-1
            while lptr<rptr:
                if lst[lptr]<=pivot:lptr+=1
                elif lst[rptr]>=pivot:rptr-=1
                else:lst[lptr],lst[rptr]=lst[rptr],lst[lptr]
            lst[rptr],lst[right]=pivot,lst[rptr]
            inner(left,rptr-1)
            inner(rptr+1,right)
        inner(0,len(lst)-1)
        return lst
    def shell_sort(self,lst:list):
        def inner(start:int,interval:int):
            nonlocal lst
            for i in range(start+interval,len(lst),interval):
                for j in range(i,start,-interval):
                    if lst[j]>=lst[j-interval]:break
                    lst[j],lst[j-interval]=lst[j-interval],lst[j]
        interval=(len(lst)>>1)
        while interval:
            for i in range(interval):
                inner(i,interval)
            interval>>=1
        return lst
