import os
import re
import numpy as np
import copy
import enipy3 as lx
import pickle

def event_count_by_cell(lat_cg,lon_cg,key1,key3,D):
    cell_idx=(lat_cg+90)*360+(lon_cg+180)
    unique_cell_idx, counts = np.unique(cell_idx, return_counts=True)
    for idx,cnt in zip(unique_cell_idx,counts):
        D[key1][idx][key3]+=cnt
    return D

def save_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


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
print(fname_list[0:5])
print(f"Total number of state files is {len(fname_list)}")


# initiate the dictionary (3 layers)
# D < yearmonth< cell_idx < lat lon IC_count CG_count

# create first layer dict key names, which are yearmonth
D={}
m_str=["01","02","03","04","05","06","07","08","09","10","11","12"]
ym_str=[]
for y in y_str:
    for m in m_str:
        ym_str.append(y+m)

cell_idx=list(np.arange(180*360)) # each cell correspond to a dict

# layer 3 dict initilization
l3_key_names=['lon','lat','n_ic','n_cg','n_wln','n']
l3_items_list=[-999,-999,0,0,0,0]
l3_dict={l3_key: l3_item for l3_key,l3_item in zip(l3_key_names,l3_items_list)} 

# layer 2 dict initilization, each key is the cell no
l2_dict={cell_no: copy.deepcopy(l3_dict) for cell_no in cell_idx} 

xx=np.arange(-180,180)
yy=np.arange(-90,90)

A=np.zeros((len(yy),len(xx)))
X=np.zeros((len(yy),len(xx)))
Y=np.zeros((len(yy),len(xx)))

n=-1
for i,y in enumerate(yy):
    for j,x in enumerate(xx):
        n=n+1
        A[i,j]=n
        X[i,j]=x
        Y[i,j]=y
        
X1=X.ravel()
Y1=Y.ravel()
A1=A.ravel()

# assign the lat and lon to each cell
for key in l2_dict.keys():
    l2_dict[key]['lon']=X1[key]
    l2_dict[key]['lat']=Y1[key]

# the layer1 dict, each key is year+month,e.g., "201801"
D={ym: copy.deepcopy(l2_dict) for ym in ym_str}
print("The dictionary has been initialized")


## example file path '/data2/Pulse/2018/01/LtgFlashPortions20180102.state'
# fill the dictionary！
for f in fname_list:
    str_split=f.split('/') # e.g., ['', 'data2', 'Pulse', '2018', '01', 'LtgFlashPortions20180102.state']
    key1=str_split[3]+str_split[4] # e.g., '201801'

    a=lx.Report(f)

    # remove duplications, #sometimes wwlln events mixed in and have some duplicates
    t=a.time
    lat=a.lat
    lon=a.lon
    cg_ic=a.type
    pc=a.amplitude
    
    A=np.hstack((t.reshape(-1,1),lat.reshape(-1,1),lon.reshape(-1,1),cg_ic.reshape(-1,1),pc.reshape(-1,1))) 
    A1=np.unique(A,axis=0)

    lat=A1[:,1]
    lon=A1[:,2]
    cg_ic=A1[:,3]

    #floor the lat and lon for easy cell_idx calculation
    lat=np.floor(lat)
    lon=np.floor(lon)

    # 0: CG, 1: IC, 40: WWLLN
    lat_cg=lat[cg_ic==0]
    lon_cg=lon[cg_ic==0]
    
    lat_ic=lat[cg_ic==1]
    lon_ic=lon[cg_ic==1]

    lat_wln=lat[cg_ic==40]
    lon_wln=lon[cg_ic==40]

    # count CG:
    D=event_count_by_cell(lat_cg,lon_cg,key1,"n_cg",D)
    D=event_count_by_cell(lat_ic,lon_ic,key1,"n_ic",D)
    D=event_count_by_cell(lat_wln,lon_wln,key1,"n_wln",D)
    D=event_count_by_cell(lat,lon,key1,"n",D)

    # keep track of files processed
    f_idx=fname_list.index(f)+1
    print(f"{f_idx}/{len(fname_list)} finished, {f}")

save_obj (D,'D.pkl')

    # print(np.asarray((unique, counts)).T)

    # print(len(lat),sum(counts))



