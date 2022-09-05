import os
import re
import numpy as np
import copy

parent_dir="/data2/Pulse/"
y_str=["2018","2019","2020"]

# find filenames of state files in the folder by year
fname_list=[]
for y in y_str:
    fname_list_year=[]
    data_dir=parent_dir+y+'/'
    for path, subdirs, files in os.walk(data_dir):
        for name in files:
            if name[-6:]=='.state':
                    name=os.path.join(path, name).replace("\\" , "/")
                    # specify the fname format (/data2/Pulse/20xx/xx/LtgFlashPortions20...) to exclude some folders contain duplicate files, 
                    # following example here: https://www.adamsmith.haus/python/answers/how-to-check-if-a-string-matches-a-pattern-in-python
                    
                    if (bool(re.match(f"/data2/Pulse/{y}/[0-9][0-9]/LtgFlashPortions20+", name))):
                        fname_list_year.append(name)

    print(f"number of state files in the {data_dir} is {len(fname_list_year)}")

    if len(fname_list_year) not in [365,366]:
        raise Exception("Number of state files for this year is wrong, neither 365 nor 366")

    fname_list=fname_list+fname_list_year

fname_list.sort()
print(f"Total number of state files is {len(fname_list)}")


# initiate the dictionary
# D < yearmonth< cell_idx < lat lon IC_count CG_count

# # create first layer dict key names, which are yearmonth
# D={}
# y_str=["2018","2019","2020"]
# m_str=["01","02","03","04","05","06","07","08","09","10","11","12"]
# ym_str=[]
# for y in y_str:
#     for m in m_str:
#         ym_str.append(y+m)

# cell_idx=list(np.arange(180*360)) # each cell correspond to a dict

# sub_key_names=['lon','lat','n_IC','n_CG']
# sub_items_list=[-999,-999,0,0]
# sub_dict={sub_key: sub_item for sub_key,sub_item in zip(sub_key_names,sub_items_list)} 
# D={cell_no: copy.deepcopy(sub_dict) for cell_no in cell_idx} 

# xx=np.arange(-180,180)
# yy=np.arange(-90,90)

# A=np.zeros((len(yy),len(xx)))
# X=np.zeros((len(yy),len(xx)))
# Y=np.zeros((len(yy),len(xx)))

# n=-1
# for i,y in enumerate(yy):
#     for j,x in enumerate(xx):
#         n=n+1
#         A[i,j]=n
#         X[i,j]=x
#         Y[i,j]=y
        
# X1=X.ravel()
# Y1=Y.ravel()
# A1=A.ravel()





# # assign the lat and lon to each cell
# for key in D.keys():
#     D[key]['lon']=X1[key]
#     F[key]['lat']=Y1[key]