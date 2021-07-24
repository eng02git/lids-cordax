import streamlit as st
import pandas as pd 
import numpy as np
from itertools import cycle
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import streamlit.components.v1 as components
import base64

st.set_page_config(
     page_title="Cordax",
     layout="wide",
)


###########################################################################################################################################
#####                    			dados aleatorios                                                                   #########
###########################################################################################################################################
np.random.seed(42)

@st.cache(allow_output_mutation=True)
def fetch_data(samples):
    deltas = cycle([
            pd.Timedelta(weeks=-2),
            pd.Timedelta(days=-1),
            pd.Timedelta(hours=-1),
            pd.Timedelta(0),
            pd.Timedelta(minutes=5),
            pd.Timedelta(seconds=10),
            pd.Timedelta(microseconds=50),
            pd.Timedelta(microseconds=10)
            ])
    dummy_data = {
        "date_time_naive":pd.date_range('2021-01-01', periods=samples),
        "apple":np.random.randint(0,100,samples) / 3.0,
        "banana":np.random.randint(0,100,samples) / 5.0,
        "chocolate":np.random.randint(0,100,samples),
        "group": np.random.choice(['A','B'], size=samples),
        "date_only":pd.date_range('2020-01-01', periods=samples).date,
        "timedelta":[next(deltas) for i in range(samples)],
        "date_tz_aware":pd.date_range('2022-01-01', periods=samples, tz="Asia/Katmandu")
    }
    return pd.DataFrame(dummy_data)

###########################################################################################################################################
#####                    			cofiguracoes aggrid									#######
###########################################################################################################################################

sample_size = 12
grid_height = 380

return_mode = 'FILTERED'
return_mode_value = DataReturnMode.__members__[return_mode]

update_mode = 'MODEL_CHANGED'
update_mode_value = GridUpdateMode.__members__[update_mode]

#enterprise modules
enable_enterprise_modules = True
enable_sidebar = True

#features
fit_columns_on_grid_load = False
enable_pagination = False
paginationAutoSize = False
use_checkbox = True
enable_selection = True
selection_mode = 'multiple'
rowMultiSelectWithClick = False
suppressRowDeselection = False

if use_checkbox:
	groupSelectsChildren = True
	groupSelectsFiltered = True

valor = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
linhas = [ 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D']
medidas = ['SPACER LOWER CAP',
	  	'SPACER LOWER CAP',
	  	'SPACER LOWER CAP',
	  	'SPACER LOWER CAP',
	  	'SPACER UPPER BLANK BEAD',
	  	'SPACER UPPER BLANK BEAD',
	  	'SPACER UPPER BLANK BEAD',
	  	'SPACER UPPER BLANK BEAD',
	  	'TOOLING PLATE',
	  	'TOOLING PLATE',
	  	'TOOLING PLATE',
	  	'TOOLING PLATE']

d = {'Medidas': medidas, 'Linha': linhas, 'Valor': valor}
df = pd.DataFrame(data=d)

#Infer basic colDefs from dataframe types
gb = GridOptionsBuilder.from_dataframe(df)

#customize gridOptions
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
gb.configure_column("Medidas", editable=False)
#gb.configure_column("date_tz_aware", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd HH:mm zzz', pivot=True, editable=False)
#gb.configure_column("apple", type=["numericColumn","numberColumnFilter","customNumericFormat"], precision=2, aggFunc='sum')
#gb.configure_column("banana", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='avg')
#gb.configure_column("chocolate", type=["numericColumn", "numberColumnFilter", "customCurrencyFormat"], custom_currency_symbol="R$", aggFunc='max')

#configures last row to use custom styles based on cell's value, injecting JsCode on components front end
cellsytle_jscode = JsCode("""
function(params) {
    if (params.value > 10) {
        return {
            'color': 'white',
            'backgroundColor': 'darkred'
        }
    } else {
        return {
            'color': 'black',
            'backgroundColor': 'white'
        }
    }
};
""")

gb.configure_column("Valor", cellStyle=cellsytle_jscode)

if enable_sidebar:
    gb.configure_side_bar()

if enable_selection:
    gb.configure_selection(selection_mode)
    if use_checkbox:
        gb.configure_selection(selection_mode, use_checkbox=True, groupSelectsChildren=groupSelectsChildren, groupSelectsFiltered=groupSelectsFiltered)
    if ((selection_mode == 'multiple') & (not use_checkbox)):
        gb.configure_selection(selection_mode, use_checkbox=False, rowMultiSelectWithClick=rowMultiSelectWithClick, suppressRowDeselection=suppressRowDeselection)

if enable_pagination:
    if paginationAutoSize:
        gb.configure_pagination(paginationAutoPageSize=True)
    else:
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=paginationPageSize)

gb.configure_grid_options(domLayout='normal')
gridOptions = gb.build()

#grid_response = AgGrid(
#    df, 
#    gridOptions=gridOptions,
#    height=grid_height, 
#    width='100%',
#    data_return_mode=return_mode_value, 
#    update_mode=update_mode_value,
#    fit_columns_on_grid_load=fit_columns_on_grid_load,
#    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
#    enable_enterprise_modules=enable_enterprise_modules,
#    )

#df = grid_response['data']
#selected = grid_response['selected_rows']
#selected_df = pd.DataFrame(selected)

#st.write(selected_df)

###########################################################################################################################################
#####                    			Teste											########
###########################################################################################################################################

htmlfile = open('teste.html', 'r', encoding='utf-8')
source = htmlfile.read()

file_ = open("Untitled.png", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

dic = {} 

telas = ['Kiss Block (1)',
	'Kiss Block (2)',
	'Bubble From (1)',
	'Bubble From (2)',
	'Bubble From (3)',
	'1st Rivet (1)',
	'1st Rivet (2)',
	'2nd Rivet (1)',
	'2nd Rivet (2)',
	'Score (1)',
	'Score (2)',
	'Panel Form (1)',
	'Panel Form (2)',
	'Panel Form (3)',
	'Panel Form (4)',
	'Strake (1)',
	'Strake (2)']
	
sel_tela = st.selectbox('Selecione o ferramental', options=telas)

nomes = ['Mario', 'Carvalho']
	
if sel_tela == 'Kiss Block (1)':	
	with st.form('form2'):
		

		
		i01, i02 = st.beta_columns([10,4])
		dic['I01'] = i01.selectbox('Nome do colaborador:', nomes) 
		dic['I02'] = i02.date_input('Data:')
		t1, t2 = st.beta_columns([10,4])
		
						
		with t1:
			components.html(source.format(image=data_url, teste=0.0001), height=1500)
			
		with t2:
			grid_response = AgGrid(
			    df, 
			    gridOptions=gridOptions,
			    height=grid_height, 
			    width='100%',
			    data_return_mode=return_mode_value, 
			    update_mode=update_mode_value,
			    fit_columns_on_grid_load=fit_columns_on_grid_load,
			    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
			    enable_enterprise_modules=enable_enterprise_modules,
			    )

		submit = t2.form_submit_button('Alterar valores')


