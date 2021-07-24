import streamlit as st
import streamlit.components.v1 as components
from st_aggrid import AgGrid
import numpy as np
import pandas as pd
from influxdb import InfluxDBClient
from influxdb import DataFrameClient
import cgi, cgitb

st.set_page_config(layout="wide")

try:

	client = InfluxDBClient(host='localhost', port=8086, database='grafana_usage')
	#client = InfluxDBClient(host='10.186.96.18', port=8086, database='grafana_usage')	
	#client = DataFrameClient(host='localhost', port=8086, database='grafana_usage')
except:
	st.error('Deu ruim')



#q1 = 'SELECT * FROM (SELECT "Segundos" as "valor" FROM "L2_FELC" WHERE time > now() - 1h);'
#q1 = 'SELECT * FROM (SELECT "var1" as "valor1" FROM "teste" WHERE time > now() - 15m);'
#q2 = 'SELECT * FROM (SELECT "var2" as "valor2" FROM "teste" WHERE time > now() - 15m);'
#q3 = 'SELECT * FROM (SELECT "var1" as "valor1", "var2" as "valor2" FROM "teste" WHERE time > now() - 1h);'


#lista1  = pd.DataFrame(client.query(q1).get_points())
#lista2  = pd.DataFrame(client.query(q2).get_points())
#lista3  = pd.DataFrame(client.query(q3).get_points())

#st1, st2, st3 = st.beta_columns(3)

#lista3['data'] = pd.to_datetime(lista3['time']).dt.date
#lista3['time'] = pd.to_datetime(lista3['time']).dt.strftime("%H:%M:%S")

#st1.write(lista1)
#AgGrid(lista1)
#st2.write(lista2)
#st3.write(lista3)

#st.write('<iframe src="http://10.186.96.18:3000/grafana/d/sg72_CpMjFdsbzXA/front-end-571?orgId=1&refresh=10s"></iframe>', unsafe_allow_html=True)
#st.write('<iframe src="http://10.186.96.18:3000/grafana/d-solo/-ZYXo_qMko/teste?orgId=1&panelId=9" width="20%" height="20%" frameborder="0"></iframe>', unsafe_allow_html=True)
#st.write(f'<iframe src="http://10.186.96.18:3000/grafana/d-solo/sg72_CpMjFdsbzXA/front-end-571?orgId=1&refresh=10s&panelId=141" width="200" height="250" frameborder="0"></iframe>', unsafe_allow_html=True)

htmlfile = open('teste.html', 'r', encoding='utf-8')
source = htmlfile.read()
components.html(source)


"""
from bs4 import BeautifulSoup

teste = st.button('teste')


soup = BeautifulSoup(source, 'html.parser')
val1 = soup.input['value']
st.write(val1)

#st.write(soup.find('input')['name'], ':', soup.find('input')['value'])
#st.write([(element['name'], element['value']) for element in soup.find_all('input')])

teste2 = st.button('teste2')
from bottle import template
"""


with st.form('form1'):
	t1, t2, t3 = st.beta_columns([2,10,2])
	val1 = t1.number_input('asd A:', min_value=0.00010, max_value=0.1001, step=0.001, format='%f')
	val2 = t1.number_input('asd B:')
	val3 = t1.number_input('asd C:')
	with t2:
		#components.html(source)
		st.write('<iframe src="teste.html" width="1000" height="1000"></iframe>', unsafe_allow_html=True)
	val1 = t3.number_input('asd2 A:')
	val2 = t3.number_input('asd2 B:')
	val3 = t3.number_input('asd2 C:')	
	submit = st.form_submit_button('Alterar valores')
	
	

