def MR2(context,distance,pattern):
    context=context.split('.')
    context=context[:-1]
    if pattern=="leastone":
        if len(distance)>1:
            del context[distance[len(distance)-1][0]]
    str='.'
    context=str.join(context)
    return context

def MR1(context,pattern):
    #TODO:
    return context