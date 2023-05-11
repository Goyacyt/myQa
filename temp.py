import matplotlib.pyplot as plt
import numpy as np
from distance import *

def main():
    fig, ax = plt.subplots(1, 2)

    # 左侧边栏，如果不需要，在plt.table中注释即可
    # rowLabels 与 rowColours中的数据长度要保持一致，同时和数据中的元素个数保持一致--len(data)
    rowLabels = ['' for i in range(10)]
    for i in range(10):
        rowLabels[i]=str(i/10)[:3]+"-"+str((i+1)/10)[:3]
    print(rowLabels)
    #rowColours = ["#EBB25E", "#F0C9C0", "#F0C9C0", "#F0C9C0", "#F0C9C0", "#F0C9C0", "#F0C9C0", "#F2F2F2"]

    # 列表头颜色，需要和单条数据长度保持一致--len(data[0])
    """colColors = ["#377eb8"]
    colColors.extend(["#00ccff"] * 20)"""

    # 左侧结果图数据

    data,sen_num=threshold()
    rdata=[]
    for i in range(len(data)):
        rdata.append([str(i/10)[:3]+"-"+str((i+1)/10)[:3],data[i],str(data[i]/sen_num)[:5]+'%'])

    #column_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"]
    column_labels=["value","Amount","Proporation"]

    # 取消坐标轴
    ax[0].axis('off')
    ax[0].table(cellText=rdata,
                colLabels=column_labels,
            cellLoc='center',
            rowLoc='center',
            loc="center")
    """
    #数据转置，右侧图数据
    transpose_data = np.array(data)
    transpose_data = np.transpose(transpose_data).tolist()
    # print(transpose_data)
    # 取消坐标轴
    ax[1].axis('off')
    ax[1].table(cellText=transpose_data,
            colLabels=rowLabels,
            colColours=rowColours,
            rowColours=colColors,
            rowLabels=column_labels,
            cellLoc='center',
            rowLoc='center',
            loc="center")
    # 将图标保存到硬盘
    # plt.savefig('fix.jpg', dpi=300)"""
    plt.show()

if __name__=='__main__':
    res=0
    year=7300
    for i in range(30):
        res+=year
        year*=1.03
    print(year,res)