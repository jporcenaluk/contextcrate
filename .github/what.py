def f(x,y,z):
    a=x+y;b=y*z;c=a-b
    if c>0:d=c*2
    else:d=c/2
    e=[]
    for i in range(10):
        if i%2==0:e.append(i*d)
        else:e.append(i+d)
    f_result=sum(e)
    g={'key1':f_result,'key2':d,'key3':c}
    def inner(val):
        return val*2 if val>5 else val/2 if val!=0 else 0
    h=[inner(g[k]) for k in g]
    result=0
    for item in h:result+=item
    return result,e,g,h

class DataProcessor:
    def __init__(self,name):self.name=name;self.data=[];self.count=0
    def add(self,val):self.data.append(val);self.count+=1;return self.count
    def process(self):
        output=[]
        for idx,item in enumerate(self.data):
            if item>10:output.append(item**2)
            elif item<0:output.append(abs(item))
            else:output.append(item*3)
        self.data=output;return output
    def get_stats(self):
        avg=sum(self.data)/len(self.data)if len(self.data)>0 else 0
        return{'avg':avg,'max':max(self.data)if self.data else None,'min':min(self.data)if self.data else None,'cnt':self.count}

x=f(5,3,2)
p=DataProcessor("test")
for i in [5,-3,15,0,8]:p.add(i)
p.process()
print(p.get_stats())