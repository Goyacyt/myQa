import sys
import numpy as np

def MR2(context,distance,pattern,threshold,proportion):
    context=context.split('.')
    context=context[:-1]
    delnum=[]
    if pattern=="leastone":
        if len(distance)>1:
            del context[distance[len(distance)-1][0]]
    elif pattern=="threshold":
        for i in range(len(distance)):
            if distance[i][1]<threshold:
                delnum.append(distance[i][0])
                #del context[distance[i][0]]
        delnum.sort(reverse=True)
        for i in range(len(delnum)):
            del context[delnum[i]]
    elif pattern=="proportion":
        for i in range(len(distance)):
            if distance[i][1]<threshold:
                v=np.random.rand()
                #print(f"v:{v}")
                if v<proportion:
                    delnum.append(distance[i][0])
        delnum.sort(reverse=True)
        for i in range(len(delnum)):
            del context[delnum[i]]
    else:
        print("MR type not realized or wrong spelled")
        sys.exit()
    str='.'
    context=str.join(context)
    context=context+'.'
    return context,delnum

def MR1(context,pattern):
    #TODO:
    return context