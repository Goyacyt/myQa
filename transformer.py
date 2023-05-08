import sys

def MR2(context,distance,pattern,threshold):
    context=context.split('.')
    context=context[:-1]
    if pattern=="leastone":
        if len(distance)>1:
            del context[distance[len(distance)-1][0]]
    elif pattern=="threshold":
        for i in range(len(distance)):
            if distance[i][1]<threshold:
                del context[distance[i][0]]
    elif pattern=="proportion":
        """TODO"""
    else:
        print("MR type not realized or wrong spelled")
        sys.exit()
    str='.'
    context=str.join(context)
    context=context+'.'
    return context

def MR1(context,pattern):
    #TODO:
    return context