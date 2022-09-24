# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 19:10:43 2022

@author: yanan
"""

import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
from matplotlib.colors import LogNorm

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import copy
import numpy.ma as ma
import csv
from scipy.io import savemat


y_str=["2018","2019","2020","2021"]
m_str=["01","02","03","04","05","06","07","08","09","10","11","12"]
ym_str=[]
for y in y_str:
    for m in m_str:
        ym_str.append(y+m)


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


def plot_NBE_F(num_events_1d, plot_name, vmax_percent=0.2, vmin_percent=0.2):
    
    num_events_2d=num_events_1d.reshape(180,360)
    fig = plt.figure(num=None, figsize=(12, 9), dpi=120, edgecolor='k')
    
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    vmax_value=vmax_percent*np.max(num_events_1d) 
    vmin_value=vmin_percent*np.min(num_events_1d) 
    
    if abs(vmax_value)>abs(vmin_value):
        vmin_value=vmin_value*abs(vmax_value/vmin_value)
    else:
        vmax_value=vmax_value*abs(vmin_value/vmax_value)

    p44=ax.imshow(num_events_2d, origin='lower', extent=[-180,180,-90,90], transform=ccrs.PlateCarree(),
                  cmap='coolwarm',vmin=vmin_value, vmax=vmax_value)
    ax.coastlines()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=2, color='gray', alpha=0.5, linestyle='--')


    
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.xlocator = mticker.FixedLocator([-180, -90, 0, 90, 180])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 15, 'color': 'gray'}
    gl.xlabel_style = {'color': 'red', 'weight': 'bold'}
    
    
    pos22= ax.get_position()
    cax11 = fig.add_axes([pos22.x1+0.05,pos22.y0,0.01,pos22.height])
    cb11 = plt.colorbar(p44, cax=cax11, extend="both")
    #cb11 = plt.colorbar(p44, cax=cax11)
    cax11.yaxis.tick_left()
    
    if 'events' in plot_name:
        cb11.set_label('Number of events', labelpad=5)
    if 'percent' in plot_name:
        cb11.set_label('NBE percent', labelpad=5) 
    if 'peak' in plot_name:
        cb11.set_label('Peak current', labelpad=5)  
    
    ax.annotate(plot_name, xy=(0.01, 0.97), xycoords='axes fraction', fontsize = 12, color='b')
    plt.savefig(plot_name+'.png')
    
    
    
    
    
D=load_obj('C:/Users/yanan/Desktop/D.pkl')
num_events_1d=np.zeros(360*180)

# total events, each row contain a month of 1d array
n_3y=np.zeros((48,360*180))


#grab data of a month
for ii, ym_key in enumerate(ym_str):
    
    A=D[ym_key]
    for key in A.keys():
        ### number of total lightning events
        num_events_1d[key]=A[key]['n']
    
    n_3y[ii]=num_events_1d
    
    
    # write 2d array as a csv
    num_events_2d=num_events_1d.reshape(180,360)
    # with open(ym_key+".csv","w+") as my_csv:
    #     csvWriter = csv.writer(my_csv,delimiter=',')
    #     csvWriter.writerows(num_events_2d)
    ym_key="m"+ym_key
    matname=ym_key+'.mat'
    savemat(matname, {ym_key:num_events_2d})
    
    
    # num_events_1dm=ma.masked_less(num_events_1d,50) 
    
    # plot_NBE_F(num_events_1dm, ym_key+' total lightning events')
    
    
n_y18=np.sum(n_3y[0:12],axis=0)
n_y19=np.sum(n_3y[12:24],axis=0)
n_y20=np.sum(n_3y[24:36],axis=0)
n_y21=np.sum(n_3y[36:],axis=0)

n_y1819=(n_y18+n_y19)*0.5
n_y1819m=ma.masked_less(n_y1819,100)
n_y20m=ma.masked_less(n_y20,100)

y_diff=(n_y20m-n_y1819m)

plot_NBE_F(y_diff, 'Difference in number of lightning events (2020-2018/19)')

