import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import dash_daq as daq
import plotly.express as px
import numpy as np
import networkx as nx
from dash.dependencies import Input, Output
import dash_table






#Cargamos todos los datasets

path = r'C:\\Users\\jhern\\Documents\\datasets\\alvaro\\ultimos datos\\datos\\'
df = pd.read_csv(path + "mascarillas.csv", delimiter=';')
cc = pd.read_csv(path + "Centro Comercial.csv", sep=";")
h1 = pd.read_csv(path + "Hospital 1.csv", sep=";")
h2 = pd.read_csv(path + "Hospital 2.csv", sep=";")
c1 = pd.read_csv(path + "Colegio 1.csv", sep=";")
c2 = pd.read_csv(path + "Colegio 2.csv", sep=";")
farm = pd.read_csv(path + "Farmacia 1.csv", sep=";")
super1 = pd.read_csv(path + "Supermercado 1.csv", sep=";")
super2 = pd.read_csv(path + "Supermercado 2.csv", sep=";")
t1 = pd.read_csv(path + "Trabajo 1.csv", sep=";")
t2 = pd.read_csv(path + "Trabajo 2.csv", sep=";")
t3 = pd.read_csv(path + "Trabajo 3.csv", sep=";")
t4 = pd.read_csv(path + "Trabajo 4.csv", sep=";")
uni = pd.read_csv(path + "Universidad.csv", sep=";")
pred = pd.read_csv(path + "predicciones.csv", sep=";")
#pred.rename(columns={ pred.columns[0]: "fecha" }, inplace = True)
pred = pred.iloc[:-2]
for i in pred.iloc[:,1:].columns:
    pred[i] = (pred[i]*100)
pred = pred.round(2)

pred['Valor máximo del día'] = pred.max(axis=1)
pred['fecha'] = ['01-12-2020','02-12-2020','03-12-2020','04-12-2020','05-12-2020','06-12-2020','07-12-2020']

cols = pred.columns.tolist()
cols = cols[-1:] + cols[:-1]
pred = pred[cols]
# Valor fecha ultimos datos actualizados
start_date = '2020-11-30 10:00:00'
end_date = '2020-11-30 22:00:00'

#lista con los nombres de los edificios
edificios = ['Centro Comercial', 'Colegio 1', 'Colegio 2','Farmacia 1',
                                  'Hospital 1', 'Hospital 2', 'Supermercado 1', 'Supermercado 2', 'Trabajo 1',
                                  'Trabajo 2', 'Trabajo 3', 'Trabajo 4', 'Universidad']

# Datos DIARIOS

# Dataset edificio con datos solo ultima fecha actualizada DIARIO
uni_diario = uni.loc[(uni['datetime'] >= start_date) & (uni['datetime'] <= end_date)]
t4_diario = t4.loc[(t4['datetime'] >= start_date) & (t4['datetime'] <= end_date)]
t3_diario = t3.loc[(t3['datetime'] >= start_date) & (t3['datetime'] <= end_date)]
t2_diario = t2.loc[(t2['datetime'] >= start_date) & (t2['datetime'] <= end_date)]
t1_diario = t1.loc[(t1['datetime'] >= start_date) & (t1['datetime'] <= end_date)]
super1_diario = super1.loc[(super1['datetime'] >= start_date) & (super1['datetime'] <= end_date)]
super2_diario = super2.loc[(super2['datetime'] >= start_date) & (super2['datetime'] <= end_date)]
h1_diario = h1.loc[(h1['datetime'] >= start_date) & (h1['datetime'] <= end_date)]
h2_diario = h2.loc[(h2['datetime'] >= start_date) & (h2['datetime'] <= end_date)]
farm_diario = farm.loc[(farm['datetime'] >= start_date) & (farm['datetime'] <= end_date)]
c2_diario = c2.loc[(c2['datetime'] >= start_date) & (c2['datetime'] <= end_date)]
c1_diario = c1.loc[(c1['datetime'] >= start_date) & (c1['datetime'] <= end_date)]
cc_diario = cc.loc[(cc['datetime'] >= start_date) & (cc['datetime'] <= end_date)]

# Eliminar datos duplicados (id que se quedan en el edificio) DIARIO
cc_diario = cc_diario[cc_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
c1_diario = c1_diario[c1_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
c2_diario = c2_diario[c2_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
farm_diario = farm_diario[farm_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
h1_diario = h1_diario[h1_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
h2_diario = h2_diario[h2_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
super1_diario = super1_diario[super1_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
super2_diario = super2_diario[super2_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
t1_diario = t1_diario[t1_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
t2_diario = t2_diario[t2_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
t3_diario = t3_diario[t3_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
t4_diario = t4_diario[t4_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
uni_diario = uni_diario[uni_diario.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")

# Conteo pcr positivo y total por edificio DIARIO
cc_pos_diario = cc_diario.pcr[cc_diario.pcr == 'Positivo'].count()
cc_tot_diario = cc_diario['pcr'].count()
h1_pos_diario = h1_diario.pcr[h1_diario.pcr == 'Positivo'].count()
h1_tot_diario = h1_diario['pcr'].count()
h2_pos_diario = h2_diario.pcr[h2_diario.pcr == 'Positivo'].count()
h2_tot_diario = h2_diario['pcr'].count()
c1_pos_diario = c1_diario.pcr[c1_diario.pcr == 'Positivo'].count()
c1_tot_diario = c1_diario['pcr'].count()
c2_pos_diario= c2_diario.pcr[c2_diario.pcr == 'Positivo'].count()
c2_tot_diario = c2_diario['pcr'].count()
farm_pos_diario = farm_diario.pcr[farm_diario.pcr == 'Positivo'].count()
farm_tot_diario = farm_diario['pcr'].count()
super1_pos_diario = super1_diario.pcr[super1_diario.pcr == 'Positivo'].count()
super1_tot_diario = super1_diario['pcr'].count()
super2_pos_diario = super2_diario.pcr[super2_diario.pcr == 'Positivo'].count()
super2_tot_diario = super2_diario['pcr'].count()
t1_pos_diario = t1_diario.pcr[t1_diario.pcr == 'Positivo'].count()
t1_tot_diario = t1_diario['pcr'].count()
t2_pos_diario = t2_diario.pcr[t2_diario.pcr == 'Positivo'].count()
t2_tot_diario = t2_diario['pcr'].count()
t3_pos_diario = t3_diario.pcr[t3_diario.pcr == 'Positivo'].count()
t3_tot_diario = t3_diario['pcr'].count()
t4_pos_diario = t4_diario.pcr[t4_diario.pcr == 'Positivo'].count()
t4_tot_diario = t4_diario['pcr'].count()
uni_pos_diario = uni_diario.pcr[uni_diario.pcr == 'Positivo'].count()
uni_tot_diario = uni_diario['pcr'].count()

#Dataset Mapa DIARIO:
city_diario = pd.DataFrame(columns=('edificio', 'latitude', 'longitude', 'pcr_positivo','total_pcr', 'ia'))


city_diario = pd.DataFrame({'edificio': ['Centro comercial', 'Colegio 1', 'Colegio 2','Farmacia',
                                  'Hospital 1', 'Hospital 2', 'Supermercado 1','Supermercado 2', 'Trabajo 1',
                                  'Trabajo 2', 'Trabajo 3', 'Trabajo 4', 'Universidad'],
                     'latitude': [40.9005721185187, 40.8993711112962, 40.93063, 40.90178,
                                  40.9094666744447, 40.9057043315905, 40.9058969403664, 40.912670,
                                  40.9058969403664, 40.9231500127792, 40.9042103081665,
                                  40.9226149493595, 40.9069348463768],
                    'longitude':[-81.1537146940288, -81.111685041072,-81.11683, -81.10522,
                                 -81.0981774363991, -81.1477875742352,-81.0879678392236, -81.126400,
                                 -81.0962075852287,-81.101529087456, -81.1109704642085,
                                 -81.1216869957168, -81.1087388665002],
                    'pcr_positivo':[cc_pos_diario, c1_pos_diario, c2_pos_diario, farm_pos_diario, h1_pos_diario,h2_pos_diario, super1_pos_diario, super2_pos_diario ,t1_pos_diario ,
                                    t2_pos_diario,t3_pos_diario,t4_pos_diario,uni_pos_diario],
                    'total_pcr':[cc_tot_diario,c1_tot_diario, c2_tot_diario, farm_tot_diario, h1_tot_diario,h2_tot_diario, super1_tot_diario, super2_tot_diario, t1_tot_diario,t2_tot_diario,
                                 t3_tot_diario,t4_tot_diario,uni_tot_diario ],
                    'ia':[cc_pos_diario/cc_tot_diario, c1_pos_diario/c1_tot_diario,c2_pos_diario/c2_tot_diario,farm_pos_diario/farm_tot_diario,h1_pos_diario/h1_tot_diario,
                          h2_pos_diario/h2_tot_diario, super1_pos_diario/super1_tot_diario, super2_pos_diario/super2_tot_diario,
                          t1_pos_diario/t1_tot_diario, t2_pos_diario/t2_tot_diario, t3_pos_diario/t3_tot_diario, t4_pos_diario/t4_tot_diario, uni_pos_diario/uni_tot_diario]})


#BubbleMap DIARIO:
mapa = px.scatter_mapbox(city_diario, lat="latitude", lon="longitude", hover_name="edificio", hover_data=["edificio", "ia"],
                        color="pcr_positivo",   size_max=25,zoom=12, height=600,size=city_diario["pcr_positivo"] ,
                        color_continuous_scale=[(0.00, "green"),  (0.5, "green"),(0.5, "red"),  (1.00, "red")],
                        labels={"pcr_psitivo": "Casos positivos"}
                        )

mapa.update_layout(
    mapbox_style="open-street-map",
    height = 450
    )
mapa.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
     autosize =True)

# Datos ACUMULADOS

# Eliminamos duplicados id ACUMULADO
cc = cc[cc.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
c1 = c1[c1.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
c2 = c2[c2.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
farm = farm[farm.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
h1 = h1[h1.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
h2 = h2[h2.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
super1 = super1[super1.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
super2 = super2[super2.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
t1 = t1[t1.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
t2 = t2[t2.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
t3 = t3[t3.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
t4 = t4[t4.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")
uni = uni[uni.pcr == 'Positivo'].drop_duplicates(subset='id', keep="first")

# Conteo positivo y total ACUMULADO
cc_pos = cc.pcr[cc.pcr == 'Positivo'].count()
cc_tot = cc['pcr'].count()
h1_pos = h1.pcr[h1.pcr == 'Positivo'].count()
h1_tot = h1['pcr'].count()
h2_pos = h2.pcr[h2.pcr == 'Positivo'].count()
h2_tot = h2['pcr'].count()
c1_pos = c1.pcr[c1.pcr == 'Positivo'].count()
c1_tot = c1['pcr'].count()
c2_pos = c2.pcr[c2.pcr == 'Positivo'].count()
c2_tot = c2['pcr'].count()
farm_pos = farm.pcr[farm.pcr == 'Positivo'].count()
farm_tot = farm['pcr'].count()
super1_pos = super1.pcr[super1.pcr == 'Positivo'].count()
super1_tot = super1['pcr'].count()
super2_pos = super2.pcr[super2.pcr == 'Positivo'].count()
super2_tot = super2['pcr'].count()
t1_pos = t1.pcr[t1.pcr == 'Positivo'].count()
t1_tot = t1['pcr'].count()
t2_pos = t2.pcr[t2.pcr == 'Positivo'].count()
t2_tot = t2['pcr'].count()
t3_pos = t3.pcr[t3.pcr == 'Positivo'].count()
t3_tot = t3['pcr'].count()
t4_pos = t4.pcr[t4.pcr == 'Positivo'].count()
t4_tot = t4['pcr'].count()
uni_pos = uni.pcr[uni.pcr == 'Positivo'].count()
uni_tot = uni['pcr'].count()

# Dataset Mapa ACUMULADOS:
city_acumulado = pd.DataFrame(columns=('edificio', 'latitude', 'longitude', 'pcr_positivo','total_pcr', 'ia'))


city_acumulado = pd.DataFrame({'edificio': ['Centro comercial', 'Colegio 1', 'Colegio 2','Farmacia',
                                  'Hospital 1', 'Hospital 2', 'Supermercado 1', 'Supermercado 2', 'Trabajo 1',
                                  'Trabajo 2', 'Trabajo 3', 'Trabajo 4', 'Universidad'],
                     'latitude': [40.9005721185187, 40.8993711112962, 40.93063, 40.90178,
                                  40.9094666744447, 40.9057043315905, 40.9058969403664, 40.912670,
                                  40.9058969403664, 40.9231500127792, 40.9042103081665,
                                  40.9226149493595, 40.9069348463768],
                    'longitude':[-81.1537146940288, -81.111685041072,-81.11683, -81.10522,
                                 -81.0981774363991, -81.1477875742352,-81.0879678392236, -81.126400,
                                 -81.0962075852287,-81.101529087456, -81.1109704642085,
                                 -81.1216869957168, -81.1087388665002],
                    'pcr_positivo':[cc_pos, c1_pos, c2_pos, farm_pos, h1_pos,h2_pos, super1_pos,super2_pos,t1_pos,t2_pos,t3_pos,t4_pos,uni_pos],
                    'total_pcr':[cc_tot,c1_tot, c2_tot, farm_tot, h1_tot,h2_tot, super1_tot,super2_tot,t1_tot,t2_tot,t3_tot,t4_tot,uni_tot ],
                    'ia':[cc_pos/cc_tot, c1_pos/c1_tot,c2_pos/c2_tot,farm_pos/farm_tot,h1_pos/h1_tot,h2_pos/h2_tot,super1_pos/super1_tot, super2_pos/super2_tot,
                          t1_pos/t1_tot,t2_pos/t2_tot,t3_pos/t3_tot,t4_pos/t4_tot,uni_pos/uni_tot,]})


# BubbleMap ACUMULADOS:
mapa2 = px.scatter_mapbox(city_acumulado, lat="latitude", lon="longitude", hover_name="edificio", hover_data=["edificio", "ia"],
                        color="pcr_positivo",   size_max=25,zoom=12, height=600,size=city_acumulado["pcr_positivo"],
                        color_continuous_scale=[(0.00, "green"),  (0.5, "green"),(0.5, "red"),  (1.00, "red")],
                        labels={"pcr_psitivo": "Casos positivos"}
                        )

mapa2.update_layout(
    mapbox_style="open-street-map",
    height = 450
    )
mapa2.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
     autosize =True)

# Curva fallecidos diaria

datos_diarios = pd.read_csv(path + "datos_diarios.csv", delimiter=';')

fallecidos = datos_diarios["Fallecidos"]
fechas = datos_diarios["Fecha"]
fallecidos_diarios = np.concatenate((np.array(fallecidos[0]).reshape(1,), np.diff(fallecidos)))
fallecidos_diario = go.Figure(data=[go.Scatter(x=fechas ,y=fallecidos_diarios)])
fallecidos_diario.update_layout(title = {
                  'text': "Curva de fallecidos",
                  'y':0.95,
                  'x':0.55,
                  'xanchor': 'center',
                  'yanchor': 'top'},
                  yaxis_title = "Total diario",
                  height = 345,
                  margin=dict(l=15,r=20,b=20,t=40,pad=4))

#Curva fallecidos acumulada
df = pd.read_csv(path + "datos_diarios.csv", delimiter=';')
fallecidos = df["Fallecidos"]
fechas = df["Fecha"]
fallecidos_acumulado = go.Figure(data=[go.Scatter(x=fechas ,y=fallecidos)])
fallecidos_acumulado.update_layout(title = {
                  'text': "Curva de fallecidos",
                  'y':0.95,
                  'x':0.55,
                  'xanchor': 'center',
                  'yanchor': 'top'},
                  yaxis_title = "Total diario",
                  height = 345,
                  margin=dict(l=15,r=20,b=20,t=40,pad=4))

#curva Contagios diarios
df = pd.read_csv(path + "datos_diarios.csv", delimiter=';')
contagiados = df["Contagiados"]
contagios_diarios = go.Figure(data=[go.Scatter(x=fechas ,y=contagiados)])
contagios_diarios.update_layout(title = {
                  'text': "Evolución de los casos diarios",
                  'y':0.9,
                  'x':0.5,
                  'xanchor': 'center',
                  'yanchor': 'top'},
                  yaxis_title = "Nº de casos activos",
                  height = 175,
                  margin=dict(l=50,r=50,b=50,t=50,pad=4), yaxis_range=[-300,32000])

# curva Contagios acumulados

masc = pd.read_csv(path + "mascarillas.csv" ,delimiter=';')


def repeatingNumbers(numList) :
    i = 0
    indices = []
    while i < len(numList) - 1 :
        n = numList[i]
        startIndex = i
        while i < len(numList) - 1 and numList[i] == numList[i + 1] :
            i = i + 1

        endIndex = i

        i = i + 1
        if n == 1 :
            indices.append(startIndex)
            indices.append(endIndex)
    return indices


filas = []
indices = []
for x in range(0 ,masc.shape[0] ,1) : filas.append(masc.loc[x ,:].values.tolist())
for x in range(0 ,masc.shape[0] ,1) : indices.append(repeatingNumbers(filas[x]))

for x in range(0 ,masc.shape[0] ,1) :
    for y in range(0 ,len(indices[x]) - 1 ,2) :
        masc.iloc[x ,indices[x][y] + 1 :indices[x][y + 1] + 1] = 0

fechas = list(masc)
fechas = fechas[1 :]
for x in range(0 ,len(fechas) ,1) : masc.loc[(masc[fechas[x]] == -1) ,fechas] = 0
contagios = []
for x in range(0 ,len(fechas) ,1) : contagios.append(sum(masc.iloc[: ,x]))

fechas = fechas[1 :]
contagios = contagios[1 :]
contagiosa = np.cumsum(contagios)

contagios_acumulados = go.Figure(data=[go.Scatter(x=fechas ,y=contagiosa)])

contagios_acumulados.update_layout(title={
    'text' : "Evolución de los casos acumulados por día" ,
    'y' : 0.9 ,
    'x' : 0.5 ,
    'xanchor' : 'center' ,
    'yanchor' : 'top'} ,
    yaxis_title="Nº de casos activos" ,
    height=175 ,
    margin=dict(l=50 ,r=50 ,b=50 ,t=50 ,pad=4) ,yaxis_range=[0 ,100000])
#CONTADORES

#contador fallecidos diario

contador_fallecidos_diario = str(fallecidos_diarios[-1])

#contador contagios diario
df = pd.read_csv(path + "datos_diarios.csv", delimiter=';')
contagiados = list(df["Contagiados"])
contador_contagios_diario = str(contagiados[-1])

#contador fallecidos acumulado
fallecidos = list(df["Fallecidos"])
contador_fallecidos_acumulado = str(fallecidos[-1])

#Contador contagios acumulados
masc = masc.drop(masc.columns[[0]], axis=1)
masc["suma"] = masc.sum(axis=1)
suma_contagios = list(masc["suma"])
contador_contagios_acumulados = str(masc.shape[0] - suma_contagios.count(0))



# Gauge plot diario
valor_gauge_diario = int(contador_contagios_diario)
gauge_diario = go.Figure(go.Indicator(
    mode="gauge+number" ,
    value=(valor_gauge_diario / (masc.shape[0]) * 100) ,
    domain={'x' : [0 ,1] ,'y' : [0 ,1]} ,
    gauge={'axis' : {'range' : [None ,100]}} ,
    title={'text' : "Porcentaje de población afectada"}))
gauge_diario.update_layout(
    height=180 ,
    margin=dict(l=50 ,r=50 ,b=50 ,t=50 ,pad=4)
)

# Gauge plot acumulado
valor_gauge_acumulado = int(contador_contagios_acumulados)
gauge_acumulado = go.Figure(go.Indicator(
    mode="gauge+number" ,
    value=(valor_gauge_acumulado / (masc.shape[0]) * 100) ,
    domain={'x' : [0 ,1] ,'y' : [0 ,1]} ,
    gauge={'axis' : {'range' : [None ,100]}} ,
    title={'text' : "Porcentaje de población afectada"}))
gauge_acumulado.update_layout(
    height=180 ,
    margin=dict(l=50 ,r=50 ,b=50 ,t=50 ,pad=4)
)


# PIE CHART
datos_diarios = pd.read_csv(path + "datos_diarios.csv", sep=";")

grav = datos_diarios[["Asintomáticos", "Casos leves", "Casos graves"]]
last_row = grav.tail(1)

a = last_row["Asintomáticos"]
cl = last_row["Casos leves"]
cg = last_row["Casos graves"]

df_estados = pd.DataFrame({'Estados':['Asintomáticos', 'Casos leves', 'Casos graves'],
                          'Valor': [int(a), int(cl), int(cg)]})

piechart = px.pie(df_estados, values='Valor', names='Estados',
                color_discrete_sequence=px.colors.sequential.Sunsetdark, title="Estados de gravedad")
piechart.update_layout(title_x = 0.5, showlegend=True, legend=dict(orientation="h",
    yanchor="bottom",
    y=0,
    xanchor="center",
    x=1
))

# PIE CHART ACUMULADO
grav = pd.read_csv(path + "datos_gravedad.csv", sep=";")
df_list = grav.values.tolist()
def repeatingNumbers2(numList, numero) :
    i = 0
    indices = []
    while i < len(numList) - 1 :
        n = numList[i]
        startIndex = i
        while i < len(numList) - 1 and numList[i] == numList[i + 1] :
            i = i + 1

        endIndex = i

        i = i + 1
        if n == numero :
            indices.append(startIndex)
            indices.append(endIndex)
    return len(indices)/2
a = 0
cl = 0
cg = 0
for x in range(0,len(df_list),1):
    a = a + repeatingNumbers2(df_list[x],1)
    cl = cl + repeatingNumbers2(df_list[x],2)
    cg = cg + repeatingNumbers2(df_list[x],3)

df_estados = pd.DataFrame({'Estados':['Asintomáticos', 'Casos leves', 'Casos graves'],
                          'Valor': [int(a), int(cl), int(cg)]})

# PCR positivos
piechart_acumulado = px.pie(df_estados, values='Valor', names='Estados',
                color_discrete_sequence=px.colors.sequential.Sunsetdark, title="Estados de gravedad" )
piechart_acumulado.update_layout(title_x = 0.5, showlegend=True, legend=dict(orientation="h",
    yanchor="bottom",
    y=0,
    xanchor="center",
    x=1
))


#GRAFO
#volvemos a cargar los datos
df = pd.read_csv(path + "mascarillas.csv", delimiter=';')
cc = pd.read_csv(path + "Centro Comercial.csv", sep=";")
h1 = pd.read_csv(path + "Hospital 1.csv", sep=";")
h2 = pd.read_csv(path + "Hospital 2.csv", sep=";")
c1 = pd.read_csv(path + "Colegio 1.csv", sep=";")
c2 = pd.read_csv(path + "Colegio 2.csv", sep=";")
farm = pd.read_csv(path + "Farmacia 1.csv", sep=";")
sp1 = pd.read_csv(path + "Supermercado 1.csv", sep=";")
sp2 = pd.read_csv(path + "Supermercado 2.csv", sep=";")
t1 = pd.read_csv(path + "Trabajo 1.csv", sep=";")
t2 = pd.read_csv(path + "Trabajo 2.csv", sep=";")
t3 = pd.read_csv(path + "Trabajo 3.csv", sep=";")
t4 = pd.read_csv(path + "Trabajo 4.csv", sep=";")
uni = pd.read_csv(path + "Universidad.csv", sep=";")

cc['edificio'] = 'Centro Comercial'
h1['edificio'] = 'Hospital 1'
h2['edificio'] = 'Hospital 2'
c1['edificio'] = 'Colegio 1'
c2['edificio'] = 'Colegio 2'
farm['edificio'] = 'Farmacia'
sp1['edificio'] = 'Supermercado 1'
sp2['edificio'] = 'Supermercado 2'
t1['edificio'] = 'Trabajo 1'
t2['edificio'] = 'Trabajo 2'
t3['edificio'] = 'Trabajo 3'
t4['edificio'] = 'Trabajo 4'
uni['edificio'] = 'Universidad'

df = pd.concat([cc ,h1 ,h2 ,c1 ,c2 ,farm ,sp1 ,sp2 ,t1 ,t2 ,t3 ,t4 ,uni])

# Dataset edificio con datos solo ultima fecha actualizada
df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date) & (df['pcr'] == 'Positivo')]
df = df.drop_duplicates(subset=['id' ,'edificio'] ,keep="first")

grouped_df = df.groupby('edificio' ,as_index=False).agg({'id' : 'count'})

building_dict = grouped_df.set_index('edificio')['id'].to_dict()


# Funcion para anotar relaciones entre edificios
def edge_maker(df ,edf) :
    df1 = pd.merge(df[df['edificio'] == edf] ,df[df['edificio'] != edf] ,
                   how='inner' ,
                   on='id')
    df_aux = df1.groupby(['edificio_x' ,'edificio_y'] ,as_index=False).agg({'id' : 'count'})
    final_dict = df_aux.set_index('edificio_y')['id'].to_dict()

    return final_dict


cc_dict = edge_maker(df ,'Centro Comercial')
c1_dict = edge_maker(df ,'Colegio 1')
c2_dict = edge_maker(df ,'Colegio 2')
h1_dict = edge_maker(df ,'Hospital 1')
h2_dict = edge_maker(df ,'Hospital 2')
farm_dict = edge_maker(df ,'Farmacia')
super1_dict = edge_maker(df ,'Supermercado 1')
super2_dict = edge_maker(df ,'Supermercado 2')
t1_dict = edge_maker(df ,'Trabajo 1')
t2_dict = edge_maker(df ,'Trabajo 2')
t3_dict = edge_maker(df ,'Trabajo 3')
t4_dict = edge_maker(df ,'Trabajo 4')
uni_dict = edge_maker(df ,'Universidad')

# CREAR GRAFO
G = nx.Graph()

# Añadir nodo por cada edificio
for char in building_dict.keys() :
    if building_dict[char] > 0 :
        G.add_node(char ,size=building_dict[char])


# Añadir las relaciones entre los edificios
def add_edges(this_dict ,graph ,edf) :
    for char in this_dict.keys() :
        if this_dict[char] > 0 :
            graph.add_edge(char ,edf ,weight=this_dict[char])


add_edges(c1_dict ,G ,'Centro Comercial')
add_edges(c1_dict ,G ,'Colegio 1')
add_edges(c2_dict ,G ,'Colegio 2')
add_edges(h1_dict ,G ,'Hospital 1')
add_edges(h2_dict ,G ,'Hospital 2')
add_edges(farm_dict ,G ,'Farmacia')
add_edges(super1_dict ,G ,'Supermercado 1')
add_edges(super2_dict ,G ,'Supermercado 2')
add_edges(t1_dict ,G ,'Trabajo 1')
add_edges(t2_dict ,G ,'Trabajo 2')
add_edges(t3_dict ,G ,'Trabajo 3')
add_edges(t4_dict ,G ,'Trabajo 4')
add_edges(uni_dict ,G ,'Universidad')

pos_ = nx.spring_layout(G ,k=0.5 ,iterations=50)


# Funcion para crear relacion entre nodo x e y, con un texto y grosor especifico
def make_edge(x ,y ,text ,width) :
    return go.Scatter(x=x ,
                      y=y ,
                      line=dict(width=width ,
                                color='lightslategray') ,
                      hoverinfo='none' ,
                      mode='lines')


# Para cada relacion, hacer un trazo
edge_trace = []
for edge in G.edges() :

    if G.edges()[edge]['weight'] > 0 :
        char_1 = edge[0]
        char_2 = edge[1]
        x0 ,y0 = pos_[char_1]
        x1 ,y1 = pos_[char_2]
        text = char_1 + '--' + char_2 + ': ' + str(G.edges()[edge]['weight'])

        trace = make_edge([x0 ,x1 ,None] ,[y0 ,y1 ,None] ,text ,
                          width=G.edges()[edge]['weight'] * 0.05)
        edge_trace.append(trace)

# Trazo de los nodos
node_trace = go.Scatter(x=[] ,
                        y=[] ,
                        text=[] ,
                        textposition="top center" ,
                        textfont_size=10 ,
                        mode='markers+text' ,
                        hoverinfo='text' ,
                        marker=dict(
                            showscale=True ,
                            colorscale='RdYlBu' ,
                            reversescale=True ,
                            color=[] ,
                            size=15 ,
                            colorbar=dict(
                                thickness=10 ,
                                title='Nº de Casos Positivos' ,
                                xanchor='left' ,
                                titleside='right'
                            ) ,
                            line=dict(width=0)))

# Para cada nodo, coger posicion y añadir al node_trace
for node in G.nodes() :
    x ,y = pos_[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['text'] += tuple(['<b>' + node + '</b>'])

for node in G.nodes() :
    node_trace['marker']['color'] += tuple([G.nodes()[node]['size']])

# Diseño
layout = go.Layout(
    showlegend=False ,
    xaxis={'showgrid' : False ,'zeroline' : False ,'showticklabels' : False} ,  # no gridlines
    yaxis={'showgrid' : False ,'zeroline' : False ,'showticklabels' : False} ,  # no gridlines
    hovermode='closest'
)

# Crear figura
grafo = go.Figure(layout=layout)
# Añadir los trazos de las relaciones
for trace in edge_trace :
    grafo.add_trace(trace)
# Añadir trazo de los nodos
grafo.add_trace(node_trace)

grafo.update_layout(showlegend=False)
grafo.update_xaxes(showticklabels=False)
grafo.update_yaxes(showticklabels=False)

# APP

app = dash.Dash(
    __name__ ,external_stylesheets=[dbc.themes.DARKLY] ,
    meta_tags=[
        {
            "name" : "viewport" ,
            "content" : "width=device-width" ,
        }
    ] ,
)

server = app.server

app.config["suppress_callback_exceptions"] = True

colors = {
    'background' : '#111111' ,
    'text' : '#7FDBFF'
}

app.layout = html.Div([
    dcc.Location(id='url' ,refresh=False) ,
    html.Div(id='page-content' ,
             style={
                 'textAlign' : 'center'})
])

index_page = html.Div([
    html.H1('Dashboard Covid-19', style={'color': '#FFFFFF', 'background-color': '#5e03fc'}),
    html.H2('Menú', style={'color': '#FFFFFF', 'background-color': '#5e03fc', 'textAlign': 'center'}),
    dcc.Link('Dashboard valores actuales', href='/page-1', style={'font-weight': 'bold', 'font-size': '26px'}),
    html.Br(),
    dcc.Link('Dashboard valores acumulados', href='/page-2', style={'font-weight': 'bold', 'font-size': '26px'}),
    html.Br(),
    dcc.Link('Grafo movilidad',href='/page-3', style={'font-weight': 'bold', 'font-size': '26px'}),
    html.Br(),
    dcc.Link('Predicciones',href='/page-4', style={'font-weight': 'bold', 'font-size': '26px'})
])

page_1_layout = html.Div([

    html.H1("Dashboard Covid-19 datos diarios, Noviembre 30, 2020" ,style={'color' : '#FFFFFF' ,'background-color' : '#5e03fc'}) ,
    dcc.Link('Volver al menú' ,href='/') ,
    html.Br() ,
    html.Br() ,

    html.Div([
        html.Div([
            html.Div([

                html.Abbr("\u003F" ,title="Contador del número total de fallecidos por Covid-19 en el último día actualizado" ,
                          style={'float' : 'right'}) ,
                daq.LEDDisplay(
                    id="dead" ,
                    label="Fallecidos" ,
                    labelPosition='top' ,
                    color='black' ,
                    value=contador_fallecidos_diario
                )
            ] ,style={'width' : '48%' ,'float' : 'left' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,

            html.Div([
                html.Abbr("\u003F" ,title="Contador del número total de contagiados por Covid-19 en el último día actualizado" ,
                          style={'float' : 'right'}) ,
                daq.LEDDisplay(
                    id="ninmun" ,
                    label="Contagiados" ,
                    labelPosition='top' ,
                    color='black' ,
                    value=contador_contagios_diario
                )
            ] ,style={'width' : '48%' ,'float' : 'right' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,

        ] ,style={'width' : '100%' ,'display' : 'inline-block'}) ,
        html.Br() ,

        html.Div([
            html.Abbr("\u003F" ,title="Curva de fallecimientos diarios por Covid-19 desde el 01/03/2020" ,
                      style={'display' : 'right'}) ,
            dcc.Graph(
                id='fallecidos' ,
                figure=fallecidos_diario
            )
        ] ,style={'width' : '100%' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,
        html.Br() ,
        html.Div([
            html.Abbr("\u003F" ,title="Porcentaje total de la población contagiada por el Covid-19 en el último día actualizado" ,
                      style={'display' : 'right'}) ,
            dcc.Graph(
                id='gauge' ,
                figure=gauge_diario
            )

        ] ,style={'width' : '100%' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,

    ] ,style={'width' : '29%' ,'float' : 'left' ,'display' : 'inline-block'}) ,
    html.Div([
        html.Div([
            html.Div([
                html.Abbr("\u003F" ,title="Mapa de burbujas mostrando el número de positivos que ha habido en cada edificio en el último día actualizado: se muestran en rojo aquellos que superan la media de positivos que han transitado los edificios, y en verde aquellos por debajo" ,
                          style={'display' : 'right'}) ,
                dcc.Graph(
                    id='graph3' ,
                    figure=mapa
                )
            ] ,style={'width' : '66%' ,'float' : 'left' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,
            html.Div([
                html.Abbr("\u003F" ,title="Total de personas contagiadas por el Covid-19 en el último día actualizado mostrado en porcentajes de cada estado de gravedad: casos graves, leves y asintomáticos" ,
                          style={'display' : 'right'}) ,
                dcc.Graph(
                    id='piechart' ,
                    figure=piechart
                )
            ] ,style={'width' : '32%' ,'float' : 'right' ,'display' : 'inline-block' ,"border" : "2px black solid"})
        ] ,style={'width' : '100%' ,'display' : 'inline-block'}) ,
        html.Div([
            html.Abbr("\u003F" ,title="Curva de los contagios diarios por Covid-19 desde el 01/03/2020" ,
                      style={'display' : 'right'}) ,
            dcc.Graph(
                id='graph2' ,
                figure=contagios_diarios
            )
        ] ,style={'width' : '100%' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,
        html.Div([
            html.Div([
                html.H5("Datos por simulación, fuente: Python")
            ] ,style={'width' : '49%' ,'float' : 'left' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,
            html.Div([
                html.H5("Ultima actualización de datos: " + datos_diarios["Fecha"].iloc[-1 ,])
            ] ,style={'width' : '49%' ,'float' : 'right' ,'display' : 'inline-block' ,"border" : "2px black solid"})
        ])

    ] ,style={'width' : '70%' ,'float' : 'right' ,'display' : 'inline-block'})

])

page_2_layout = html.Div([

    html.H1("Dashboard Covid-19 datos acumulados" ,style={'color' : '#FFFFFF' ,'background-color' : '#5e03fc'}) ,
    dcc.Link('Volver al menú' ,href='/') ,
    html.Br() ,
    html.Br() ,

    html.Div([
        html.Div([
            html.Div([
                html.Abbr("\u003F" ,title="Contador del número de fallecimientos acumulados por Covid-19 desde el 01/03/2020 hasta la fecha con los últimos datos actualizados") ,
                daq.LEDDisplay(
                    id="dead" ,
                    label="Fallecidos" ,
                    labelPosition='top' ,
                    color='black' ,
                    value=contador_fallecidos_acumulado
                )
            ] ,style={'width' : '48%' ,'float' : 'left' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,

            html.Div([
                html.Abbr("\u003F" ,title="Contador del número de contagios acumulados por Covid-19 desde el 01/03/2020 hasta la fecha con los últimos datos actualizados") ,
                daq.LEDDisplay(
                    id="ninmun" ,
                    label="Contagiados" ,
                    labelPosition='top' ,
                    color='black' ,
                    value=contador_contagios_acumulados
                )
            ] ,style={'width' : '48%' ,'float' : 'right' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,

        ] ,style={'width' : '100%' ,'display' : 'inline-block'}) ,
        html.Br() ,

        html.Div([
            html.Abbr("\u003F" ,title="Curva de fallecimientos acumulados por Covid-19 desde el 01/03/2020") ,
            dcc.Graph(
                id='graph4' ,
                figure=fallecidos_acumulado
            )
        ] ,style={'width' : '100%' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,
        html.Br() ,
        html.Div([
            html.Abbr("\u003F" ,title="Porcentaje total acumulado de la población contagiada por el Covid-19 desde el 01/03/2020 hasta la fecha con los últimos datos actualizados") ,
            dcc.Graph(
                id='gauge' ,
                figure=gauge_acumulado
            )

        ] ,style={'width' : '100%' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,

    ] ,style={'width' : '29%' ,'float' : 'left' ,'display' : 'inline-block'}) ,
    html.Div([
        html.Div([
            html.Div([
                html.Abbr("\u003F" ,title="Mapa de burbujas mostrando el número de positivos que ha habido en cada edificio desde el 01/03/2020 hasta la fecha con los últimos datos actualizados: Se muestran en rojo aquellos que superan la media de positivos acumulados que han transitado los edificios, y en verde aquellos por debajo.") ,
                dcc.Graph(
                    id='graph3' ,
                    figure=mapa2
                )
            ] ,style={'width' : '66%' ,'float' : 'left' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,
            html.Div([
                html.Abbr("\u003F" ,title="Total acumulado de personas contagiadas por el Covid-19 en el último día actualizado mostrado en porcentajes de cada estado de gravedad: casos graves, leves y asintomáticos") ,
                dcc.Graph(
                    id='piechart' ,
                    figure=piechart_acumulado
                )
            ] ,style={'width' : '32%' ,'float' : 'right' ,'display' : 'inline-block' ,"border" : "2px black solid"})
        ] ,style={'width' : '100%' ,'display' : 'inline-block'}) ,
        html.Div([
            html.Abbr("\u003F" ,title="Curva de los contagios acumulados por Covid-19 desde el 01/03/2020 hasta la fecha con los últimos datos actualizados") ,
            dcc.Graph(
                id='graph2' ,
                figure=contagios_acumulados
            )
        ] ,style={'width' : '100%' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,
        html.Div([
            html.Div([
                html.H5("Datos por simulación, fuente: Python")
            ] ,style={'width' : '49%' ,'float' : 'left' ,'display' : 'inline-block' ,"border" : "2px black solid"}) ,
            html.Div([
                html.H5("Ultima actualización de datos: " + datos_diarios["Fecha"].iloc[-1 ,])
            ] ,style={'width' : '49%' ,'float' : 'right' ,'display' : 'inline-block' ,"border" : "2px black solid"})
        ])

    ] ,style={'width' : '70%' ,'float' : 'right' ,'display' : 'inline-block'})

])

page_3_layout = html.Div([

    html.H1("Grafo movilidad Covid-19" ,style={'color' : '#FFFFFF' ,'background-color' : '#5e03fc'}) ,
    dcc.Link('Volver al menú' ,href='/') ,
    html.Br(),
    html.Br(),
    html.Abbr("\u003F" ,title="Grafo de movilidad: muestra el flujo de personas cuyas mascarillas han dado positivo en Covid-19 entre los distintos edificios, durante la última feha actualizada. El grosor de las aristas es proporcional al transito que hay entre los respectivos edificios. El color de los nodos es acorde al total de positivos que ha habido en ese edificio en la última fecha actualizada."),
    dcc.Graph(
        id='grafo' ,
        figure=grafo
    )
])
#Los dos valores mas altos de la tabla
def style_row_by_top_values(preds, nlargest=2):
    numeric_columns = preds.select_dtypes('number').columns
    styles = []
    for i in range(len(preds)):
        row = preds.loc[i, numeric_columns].sort_values(ascending=False)
        for j in range(nlargest):
            styles.append({
                'if': {
                    'filter_query': '{{id}} = {}'.format(i),
                    'column_id': row.keys()[j]
                },
                'backgroundColor': '#ff0000',
                'color': 'white'
            })
    return styles

pred['id'] = pred.index


page_4_layout = html.Div([

    html.H1("Predicciones Covid-19" ,style={'color' : '#FFFFFF' ,'background-color' : '#5e03fc'}) ,
    dcc.Link('Volver al menú' ,href='/'),
    html.Br(),
    html.Br(),
    html.Div([
            html.H5('Seleccione una edificio'),
            dcc.Dropdown(
                id='dropdown1',
                options=[{'label': i, 'value': i} for i in edificios],
                value='Centro Comercial',
                style={
                    'color': '#000000'
                }
            ),


            html.H2("Evolución de la predicción de casos positivos"),
            html.Abbr("\u003F" ,title="Gráfico de barras para cada edificio mostrando el número de contagios que se predice que habrá en cada uno, durante los siete días próximos a la última fecha actualizada") ,
            dcc.Graph(
                id='graph'
            ),

    ], style={'width': '48%','display': 'inline-block'}),
    html.Br(),
    html.Br(),
    html.H2("Tabla de predicciones"),
    html.Abbr("\u003F" ,title="Tabla con las predicciones de los próximos siete días para cada edificio") ,
    html.Div([
              html.Div([
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in pred.columns if i != 'id'],
                            data=pred.to_dict('records'),
                            sort_action='native',
                            style_cell = {'backgroundColor': '#484848'},
                            style_data_conditional=style_row_by_top_values(pred),


                        )]),

    ])
])

@app.callback(Output('graph', 'figure'),
              Input('dropdown1', 'value'))

def update_fig1(drop1):
    y = str(drop1)
    fig = px.bar(pred ,x='fecha' ,y=y,color=y,
                 color_continuous_scale=px.colors.sequential.YlOrRd)

    return fig


@app.callback(dash.dependencies.Output('page-content' ,'children') ,
              [dash.dependencies.Input('url' ,'pathname')])
def display_page(pathname) :
    if pathname == '/page-1' :
        return page_1_layout
    elif pathname == '/page-2' :
        return page_2_layout
    elif pathname == '/page-3' :
        return page_3_layout
    elif pathname == '/page-4' :
        return page_4_layout
    else :
        return index_page


if __name__ == '__main__' :
    app.run_server(debug=True ,use_reloader=False)


