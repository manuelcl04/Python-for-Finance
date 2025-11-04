#dashboards financieros version github

#incluir en el mismo chunk la carga de los paquetes que usamos (no instalacion)

import plotly as pl
import plotly.express as px
import numpy as np
import pandas as pd
import pathlib
import dash
import dash_bootstrap_components as dbc
#para hacer dashboards
from dash import Dash,dcc,html,Input,Output
from dash import dash_table



#paso 1 inciar dash
app=dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


#Github: agregar linea de server que usa git
server=app.server

app.title="Dashboard Financiero"

df=pf.read_csv("empresas.csv")

sales_list=["Total Revenues","Cost of Revenues","Gross Profit","Total Operating Expenses",
            "Operating Income","Net Income", "Shares Outstanding","Close Stock Price",
            "Market Cap","Multiple of Revenue"]

#app layout
app.layout=html.Div([
    #linea al incio del dashboard con todos los dropdowns y filtros:
    html.Div([html.Div([
        #html del primer dropdown para elegir las empresas a visualizat
        html.Div(dcc.Dropdown(
            id="stockdropdown",value=["Amazon","Tesla","Microsoft","Apple","Google"],multi=True,
            options=[{"label":x,"value":x}for x in sorted(df.Company.unique())]),
                 className="six columns", style={"width":"50%"}),

        #html del segundo dropdown para elegir variable numerica a ver en el dashboard
        html.Div(dcc.Dropdown(
            id="numericdropdown",value="Total Revenues",clearable=False,
            options=[{"label":x,"value":x} for x in sales_list]),className="six columns",
                 style={"width":"50%"})],className="row")], className="custom-dropdown"),

    #html de las graficas
    html.Div([dcc.Graph(id="bar",figure={})]),

    html.Div([dcc.Graph(id="boxplot",figure={})]),

    html.Div([html.Div(id="table-container_1",style={"marginBottom":"15px","marginTop":"0px"})]),
])

#paso 3 callback para actualizar las graficas y la tabla

@app.callback(
    #output: las 2 graficas actializadas y la tabla
    [Output("bar","figure"),Output("boxplot","figure"),Output("table-container_1","children")],
    [Input("stockdropdown","value"),Input("numericdropdown","value")]
)

#paso 4: definicion de las funciones para armar las graficas y la tabla

def display_value(selected_stock,selected_numeric):
  if len(selected_stock)==0:
    dfv_fltrd=df[df["Company"].isin(["Amazon","Tesla","Microsoft","Apple","Google"])]
  else:
    dfv_fltrd=df[df["Company"].isin(selected_stock)]#seleccionar empresas

  #primera grafica de lineas con empresas selecionadas

  fig=px.line(dfv_fltrd,color="Company",x="Quarter",markers=True,y=selected_numeric,
              width=1000,height=500)

  #hacer titulo de la grafica variable

  fig.update_layout(title=f"{selected_numeric} de {selected_stock}",
                    xaxis_title="Quarters")

  fig.update_traces(line=dict(width=2))#ancho de lineas, si no, usa default

  #segunda grafica: boxplot

  fig2=px.box(dfv_fltrd,color="Company",x="Company",y=selected_numeric,width=1000,height=500)
  fig2.update_layout(title=f"{selected_numeric} de {selected_stock}") #titulo variable

  #tabla: modificar dataframe para poder hacerla tabla
  df_reshaped=dfv_fltrd.pivot(index="Company",columns="Quarter",values=selected_numeric)
  df_reshaped2=df_reshaped.reset_index()

  #return de la funcion indicando como a desplegar la tabla

  return (fig,fig2,
          dash_table.DataTable(columns=[{"name":i,"id":i} for i in df_reshaped2.columns],
                               data=df_reshaped2.to_dict("records"),
                               export_format="csv", #para descar datos filtrados
                               fill_width=True,#que ocupe el ancho del dahs
                               style_cell={"font-size":"12px"},
                               style_table={"backgroundColor":"blue",
                                            "color":"white"},#los encabezados tendran fondo azul y texto blanco
                               style_data_conditional=[{"backgroundColor":"white","color":"black"}]
                               ))
#paso 5: correr el app
#GITHUB: en la version para git hay que agregar el host
if __name__=="__main__":
    app.run(debug=False, host="0.0.0.0",port=10000)
