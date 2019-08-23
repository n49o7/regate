"""
Conduct sexy data anlaysis.
"""

import pandas as pd
import numpy as np
import altair as alt

def valid(row):
    """ Sum the angles to check for errors while recording """
    try:
        int(row['w_azi']), int(row['b_rte']), int(row['w_ang'])
        return True if int(row['w_azi']) - int(row['b_rte']) == int(row['w_ang']) else False
    except:
        return False

def ang_a(a):
    """ Return the absolute value of the wind angle, between 0 and 180 """
    return int( np.degrees(np.arccos(np.cos(np.radians( int(a) % 360 )))) )

def changed(r):
    """ Count the number of sailing parameters changed compared to the previous row """
    p = ['b_sails', 'w_ang', 'w_spd', 'b_spd']
    x = r.name-1
    q =  data.loc[x,:]
    x = set( [q[i] for i in p] )
    y = set( [r[i] for i in p] )
    return len(x ^ y)/2

# def make_data_old(recent=False):
#     global data
#     data = pd.read_csv('data_raw.csv',sep=",",encoding='utf-8')
#     if recent == True:
#         data = data[data['chrono'] > '3d 00h 39\' 00"']
#     data['spd_perc'] = np.round( data['b_spd'] / data['w_spd'], 2)
#     data['valid'] = data.apply(valid, axis=1)
#     data = data[data['valid'] == True].iloc[:,:-1].reset_index()
#     data['w_ang_a'] = data['w_ang'].apply(ang_a)
#     data['w_spd_r'] = data['w_spd'].apply(round)
#     if recent == True:
#         data = data[data['b_spd'] > 0]
#         data.to_csv('data_recent.csv', encoding='utf-8', sep=',', index=False)
#     else:
#         # data['ch_spd'] = -data['b_spd'].diff().eq(0)
#         data['changed'] = data[1:].apply(changed, axis=1)
#         data = data[data['changed'] >= 2].iloc[:,:-1].reset_index(drop=True)
#         data.to_csv('data_clean.csv', encoding='utf-8', sep=',', index=False)

make_data()

def make_data():
    global data
    data = pd.read_csv('data_raw.csv',sep=",",encoding='utf-8')
    data['spd_perc'] = np.round( data['b_spd'] / data['w_spd'], 2)
    data['valid'] = data.apply(valid, axis=1)
    data = data[data['valid'] == True].iloc[:,:-1].reset_index()
    data['w_ang_a'] = data['w_ang'].apply(ang_a)
    data['w_spd_r'] = data['w_spd'].apply(round)
    # data.to_csv('data_semiclean.csv', encoding='utf-8', sep=',', index=False)
    data['changed'] = data[1:].apply(changed, axis=1)
    data = data[data['changed'] >= 2].iloc[:,:-1].reset_index(drop=True)
    data.to_csv('data_clean.csv', encoding='utf-8', sep=',', index=False)

def append_data():
    global base
    base = pd.read_csv('data_clean.csv',sep=",",encoding='utf-8')
    data = pd.read_csv('data_raw.csv',sep=",",encoding='utf-8')
    last_chrono = data[-1:]['chrono']
    recent = data[data['chrono'] > last_chrono]
    base.append(recent)

def make_charts(begin, end):
    winds = [i for i in range(begin, end+1)]
    for w in winds:
        # print('chart_' + str(w) + ' : wind ∈ [' + str(w-.5) + ', ' + str(w+.5) + '[')
        # if
        chart = alt.Chart(data[data['w_spd_r'] == w]).mark_point().encode(
            alt.X('w_ang_a', scale=alt.Scale(domain=(0,180))),
            alt.Y('b_spd', scale=alt.Scale(domain=(0,14))),
            # x='w_ang_a',
            # y='b_spd',
            color='b_sails').properties(
            title='wind '+str(w)+'kn',
            width=640,
            height=360,
            background='#FFF')
        name = 'charts/chart_'+str(w)+'kn.png'
        chart.save(name, scale_factor=2.0)


make_charts(1,40)

# make_data()
data = pd.read_csv('data_clean.csv')
data['w_spd_r'] = data['w_spd'].apply(round)

def best_sail(w_ang_a, w_spd_r):
    # i = data.query('w_spd_r == '+str(w_spd_r)+' & w_ang_a == '+str(w_ang_a))['b_spd'].idxmax()
    try:
        q = 'w_ang_a == '+str(w_ang_a)+' & w_spd_r == '+str(w_spd_r)
        i = data.query(q)['b_spd'].idxmax()
        j = data.loc[i,'b_sails']
    except:
        j = "no data"
    return j

# best_sail(92,22)
best_sail(0,1)
best_sail(179,38)
# data.loc[55,'b_sails']
#
# def make_perfs():
#     perfs =

# data.query('w_spd_r == 22 & w_ang_a == 92')
# data.query('w_spd_r == 22 & w_ang_a == 92')['b_spd'].idxmax()


# data['w_spd_r'].unique()

# pd.DataFrame(data=data['b_spd'].max(), index=data['w_spd_r'], columns=data['w_ang_a'])
a = pd.DataFrame(index=data['w_spd_r'].unique(), columns=data['w_ang_a'].unique())
a.sort_index(inplace=True,axis=0)
a.sort_index(inplace=True,axis=1)
a[:3]

# b = a.apply( lambda a: pd.DataFrame(a).apply(lambda b: (a.name, b.name), axis=1) )
# b[:3]
#
# c = b.applymap(lambda x: 'best_sail('+str(x[0])+','+str(x[1])+')')
# c[:3]
#
# d = b.applymap(lambda x: best_sail(int(x[0]), int(x[1])))
# d[:3]
#
# e = a

for col in a:
    for row, value in a[col].iteritems():
        # print('best_sail(',col,',',row,')')
        # print(type(col),type(row))
        # print(best_sail(col,row))
        # a.loc[row,col] = 'h'
        a.loc[row,col] = best_sail(col,row)

a[:3]

a.to_csv('perfs.csv',encoding="utf-8")

for row in col:
        e.loc[row,col] = best_sail(col,row)

# a.apply(lambda x: a.eval('w_spd_r == '+str(x.name)+' & w_ang_a == '+str(x.name)), axis=1)
# def ret(a,b):
#     return (a,b)
# def coords(a):
#     return (a.index,a.name)
# b = a.applymap(coords)
# b = a.applymap(lambda x: ret(x.name, x.index))
# .apply(lambda x: pd.DataFrame(x).apply(lambda y: LD(x.name, y.name), axis=1))
# data.query('w_spd_r == 22')

a = pd.read_csv('perfs_sail_raw.csv',encoding="utf-8",index_col=0)
a.sort_index(inplace=True,axis=0,ascending=False)
a.replace('no data','', inplace=True)
# a[:3]

b = a.reset_index().melt(id_vars=['index'])
b.columns = ['w_spd','w_ang_a','best_sail']
b['w_ang_a'] = pd.to_numeric(b['w_ang_a'], errors='ignore', downcast='integer')
b['w_spd'] = pd.to_numeric(b['w_spd'], errors='ignore', downcast='integer')
# b[:3]

import altair as alt
# alt.data_transformers.enable('csv')
# alt.limit_rows(8000)
alt.data_transformers.enable('default', max_rows=8000)
list(data['b_sails'].unique())
domain = list(data['b_sails'].unique())
range = ['#8DD3C7','#80B1D3','#B3DE69','#FDB462','#FB8072']
chart = alt.Chart(b).mark_rect().encode(
    alt.Y('w_spd', sort='ascending' ),
    # y = 'w_spd:O',
    x = 'w_ang_a:O',
    color=alt.Color('best_sail', scale=alt.Scale(domain=domain, range=range))
    # color = 'best_sail:N'
    ).properties(
    background='#FFF'
    )

chart.save('perfs_sail_raw.png', scale_factor=2.0)





def best_speed(w_ang_a, w_spd_r):
    # i = data.query('w_spd_r == '+str(w_spd_r)+' & w_ang_a == '+str(w_ang_a))['b_spd'].idxmax()
    try:
        q = 'w_ang_a == '+str(w_ang_a)+' & w_spd_r == '+str(w_spd_r)
        i = data.query(q)['b_spd'].max()
    except:
        i = "no data"
    return i

c = pd.DataFrame(index=data['w_spd_r'].unique(), columns=data['w_ang_a'].unique())
c.sort_index(inplace=True,axis=0)
c.sort_index(inplace=True,axis=1)
c[10:15]

for col in c:
    for row, value in c[col].iteritems():
        c.loc[row,col] = best_speed(col,row)

c.to_csv('perfs_speed_raw.csv',encoding='utf-8')
for col in c:
    c[col] = pd.to_numeric(c[col])
c[10:15]
d = c.interpolate(axis=1)
d = d.interpolate(axis=0)
d = d.round(2)
d[10:15]
d.to_csv('perfs_speed_interpol.csv',encoding='utf-8')
