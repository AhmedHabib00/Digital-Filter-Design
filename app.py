import functools
from bokeh.plotting import figure
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource,Button,TextInput,CheckboxGroup
from bokeh.io import curdoc
from bokeh.layouts import column,row
import numpy as np
from scipy.signal import zpk2tf,freqz
np.seterr(divide='ignore', invalid='ignore')
zplane = figure(plot_width=600, plot_height=600, match_aspect=True, tools='pan,wheel_zoom,undo,reset,hover')
zplane.circle(0, 0, radius=1.0, fill_color=None)
zplane.line((0, 2), (0, 0))
zplane.line((0, -2), (0, 0))
zplane.line((0, 0), (0, 2))
zplane.line((0, 0), (0, -2))

mag_fig = figure(plot_width=600, plot_height=300, match_aspect=True, title='Magnitude')
phase_fig = figure(plot_width=600, plot_height=300, match_aspect=True, title='Phase')
conj_zero_source = ColumnDataSource(data=dict(xc0=[],yc0=[]))
conj_pole_source = ColumnDataSource(data=dict(xc1=[],yc1=[]))
zero_source = ColumnDataSource(data=dict(x0=[], y0=[]))
pole_source = ColumnDataSource(data=dict(x1=[], y1=[]))
mag_source = ColumnDataSource(data=dict(m0=[], m1=[]))
phase_source = ColumnDataSource(data=dict(p0=[], p1=[]))


zero_renderer = zplane.scatter(x='x0', y='y0', source=zero_source, size=10)
pole_renderer = zplane.x(x='x1', y='y1', source=pole_source, size=15)
conj_pole_renderer = zplane.x(x='xc1',y='yc1',source=conj_pole_source,size=15)
conj_pole_renderer = zplane.circle(x='xc0',y='yc0',source=conj_zero_source,size=10)
mag_fig.line(x='m0', y='m1', source=mag_source)
phase_fig.line(x='p0', y='p1', source=phase_source)
s=1

def update(attr,old,new,s):
    conj_zero_source.data['xc0'] = []
    conj_zero_source.data['yc0'] = []
    conj_pole_source.data['xc1'] = []
    conj_pole_source.data['yc1'] = []
    zeroes = []
    poles = []
    conjzx = []
    conjzy = []
    conjpx = []
    conjpy = []
    for i in range(len(zero_source.data['x0'])):
        zeroes.append(zero_source.data['x0'][i] + zero_source.data['y0'][i] * 1j)
        if len(conj_chck.active):
            #zeroes.append(zero_source.data['x0'][i] + zero_source.data['y0'][i] * -1j)
            conjzx.append(zero_source.data['x0'][i])
            conjzy.append(-1*zero_source.data['y0'][i])


    for i in range(len(pole_source.data['x1'])):
        poles.append(pole_source.data['x1'][i] + pole_source.data['y1'][i] * 1j)
        if len(conj_chck.active):
            #poles.append(pole_source.data['x1'][i] + pole_source.data['y1'][i] * -1j)
            conjpx.append(pole_source.data['x1'][i])
            conjpy.append(-1*pole_source.data['y1'][i])

    mag_source.data = {'m0': [], 'm1': []}
    phase_source.data = {'p0': [], 'p1': []}
    num, den = zpk2tf(zeroes, poles, 1)
    w, h = freqz(num, den, worN=10000)
    mag = np.sqrt(h.real ** 2 + h.imag ** 2)
    phase = np.arctan(h.imag / h.real)
    mag_source.stream({'m0': w, 'm1': mag})
    phase_source.stream({'p0': w, 'p1': phase})
    conj_zero_source.stream({'xc0':conjzx,'yc0':conjzy})
    conj_pole_source.stream({'xc1':conjpx,'yc1':conjpy})

def conj(x):
    global s
    s=0
    conj_zero_source.data = {'xc0': [], 'yc0': []}
    conj_pole_source.data = {'xc1':[],'yc1':[]}
    #update(0,0,0,s=1)
    update(0,0,0,s=s)

conj_chck = CheckboxGroup(labels=['Conjugate'],active=[])
def callback():
    global s
    conj(s)
conj_chck.on_change('active', lambda attr, old, new: callback())

def delete(x):
    if x ==0:
        zero_source.data['x0']=[]
        zero_source.data['y0']=[]
        conj_zero_source.data['xc0']=[]
        conj_zero_source.data['yc0']=[]
    if x==1:
        pole_source.data['x1']=[]
        pole_source.data['y1']=[]
        conj_pole_source.data['xc1']=[]
        conj_pole_source.data['yc1']=[]
    if x==2:
        pole_source.data['x1']=[]
        pole_source.data['y1']=[]
        zero_source.data['x0']=[]
        zero_source.data['y0']=[]
        conj_pole_source.data['xc1']=[]
        conj_pole_source.data['yc1']=[]
        conj_zero_source.data['xc0']=[]
        conj_zero_source.data['yc0']=[]

    if x==3:
        x0temp = zero_source.data['x0']
        x0temp.pop(-1)
        zero_source.data['x0']=x0temp
        y0temp = zero_source.data['y0']
        y0temp.pop(-1)
        zero_source.data['y0']=y0temp
        if len(conj_chck.active):
            xc0temp = conj_zero_source.data['xc0']
            xc0temp.pop(-1)
            conj_zero_source.data['xc0'] = xc0temp
            yc0temp = conj_zero_source.data['yc0']
            yc0temp.pop(-1)
            conj_zero_source.data['yc0'] = yc0temp

    if x==4:
        x1temp = pole_source.data['x1']
        x1temp.pop(-1)
        pole_source.data['x1'] = x1temp
        y1temp = pole_source.data['y1']
        y1temp.pop(-1)
        pole_source.data['y1'] = y1temp
        if len(conj_chck.active):
            xc0temp = conj_pole_source.data['xc1']
            xc0temp.pop(-1)
            conj_pole_source.data['xc1'] = xc0temp
            yc0temp = conj_pole_source.data['yc1']
            yc0temp.pop(-1)
            conj_pole_source.data['yc1'] = yc0temp
    zplane.circle(x='x0', y='y0', source=zero_source, size=10)
    zplane.x(x='x1', y='y1', source=pole_source, size=15)
    zplane.x(x='xc1', y='yc1', source=conj_pole_source, size=15)
    zplane.circle(x='xc0', y='yc0', source=conj_zero_source, size=10)
    update(0,0,0,s)



zero_draw_tool = PointDrawTool(renderers=[zero_renderer], empty_value='black')
zplane.add_tools(zero_draw_tool)

pole_draw_tool = PointDrawTool(renderers=[pole_renderer], empty_value='black')
zplane.add_tools(pole_draw_tool)

zplane.toolbar.active_tap = zero_draw_tool
clr_zero_btn = Button(label='Clear All Zeroes',button_type='danger')
clr_zero_btn.on_click(functools.partial(delete,0))

clr_pol_btn = Button(label='Clear All Poles',button_type='danger')
clr_pol_btn.on_click(functools.partial(delete,x=1))

clr_all_btn = Button(label='Clear All',button_type='danger')
clr_all_btn.on_click(functools.partial(delete,x=2))

clr_z_btn = Button(label='Undo Zero',button_type='danger')
clr_z_btn.on_click(functools.partial(delete,x=3))

clr_p_btn = Button(label='Undo Pole',button_type='danger')
clr_p_btn.on_click(functools.partial(delete,x=4))

zero_source.on_change('data', functools.partial(update,s=s))
pole_source.on_change('data', functools.partial(update,s=s))

columns = [TableColumn(field="x", title="x")]

menu = ColumnDataSource(data=dict(x=[y for y in np.linspace(0.1,1,10)]))
table = DataTable(source=menu, columns=columns, editable=True, height=200,selectable='checkbox')
text = TextInput(value=None,title='Add a')
def update_text(attrname,old,new):
    temp = menu.data
    menu.data={k:[] for k in menu.data}
    temp['x'].append(f'{text.value}')
    streamit(temp)
def streamit(temp):
    menu.stream({'x':temp['x']})
text.on_change('value',update_text)
table_row = TextInput(value = '', title = "Row index:")
table_cell_column_1 = TextInput(value = '', title = "A:")

def function_source(attr, old, new):
    try:
        all_pass_psrc.data = {k: [] for k in all_pass_psrc.data}
        all_pass_zsrc.data = {k: [] for k in all_pass_zsrc.data}
        pass_filter_src.data = {l: [] for l in pass_filter_src.data}
        selected_index = menu.selected.indices[-1]
        a= float(menu.data['x'][selected_index])
        all_pass_psrc.data['xp1'].append(a)
        all_pass_psrc.data['yp1'].append(0)
        all_pass_zsrc.data['xp0'].append(1/a)
        all_pass_zsrc.data['yp0'].append(0)
        table_row.value = str(selected_index)
        table_cell_column_1.value = str(menu.data["x"][selected_index])
        all_pass(float(menu.data['x'][selected_index]))

    except IndexError:
        pass
pz = figure(plot_width=600, plot_height=300, match_aspect=True, title='pz')
pz.circle(0, 0, radius=1.0, fill_color=None)
pz.line((0, 2), (0, 0))
pz.line((0, -2), (0, 0))
pz.line((0, 0), (0, 2))
pz.line((0, 0), (0, -2))
allpass_phase_fig = figure(plot_width=600, plot_height=300, match_aspect=True, title='Filter')
all_pass_zsrc = ColumnDataSource(data=dict(xp0=[], yp0=[]))
all_pass_psrc = ColumnDataSource(data=dict(xp1=[], yp1=[]))
pass_renderer1 = pz.x(x='xp0',y='yp0',source=all_pass_zsrc,size=15)
pass_renderer2 = pz.circle(x='xp1',y='yp1',source=all_pass_psrc,size=10)
pass_filter_src = ColumnDataSource(data=dict(x=[], y=[]))
pass_renderer = allpass_phase_fig.line(x='x',y='y',source=pass_filter_src)
def all_pass(a):
    zeroes = []
    poles = []
    for i in range(len(all_pass_zsrc.data['xp0'])):
        zeroes.append(all_pass_zsrc.data['xp0'][i] + all_pass_zsrc.data['yp0'][i] * 1j)
    for i in range(len(all_pass_psrc.data['xp1'])):
        poles.append(all_pass_psrc.data['xp1'][i] + all_pass_psrc.data['yp1'][i] * 1j)
    pass_num,pass_den = zpk2tf(zeroes,poles,1)
    w, h = freqz(pass_num,pass_den,worN=10000)
    allpassphase = np.arctan(h.imag/h.real)
    all_pass_zsrc.stream({'xp0':[1/a],'yp0':[0]})
    all_pass_psrc.stream({'xp1':[a],'yp1':[0]})
    pass_filter_src.stream({'x':w,'y':allpassphase})

    xtemp0 = zero_source.data['x0']
    ytemp0 = zero_source.data['y0']
    xtemp1 = pole_source.data['x1']
    ytemp1 = pole_source.data['y1']
    if a not in xtemp1:
        xtemp1.append(a)
        ytemp1.append(0)
        xtemp0.append(1 / a)
        ytemp0.append(0)

    else:
        xtemp1.pop(-1)
        ytemp1.pop(-1)
        xtemp0.pop(-1)
        ytemp0.pop(-1)
    zero_source.data['x0'] = xtemp0
    zero_source.data['y0'] = ytemp0
    pole_source.data['x1'] = xtemp1
    pole_source.data['y1'] = ytemp1



menu.selected.on_change('indices', function_source)


curdoc().theme = "dark_minimal"
curdoc().add_root(row(column(row(zplane,column(mag_fig,phase_fig),column(text, table,table_row, table_cell_column_1)),row(column(clr_p_btn,clr_zero_btn,conj_chck),column(clr_z_btn,clr_pol_btn,clr_all_btn), column(pz),column(allpass_phase_fig)))))

