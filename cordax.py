import streamlit as st
from streamlit import caching
import pandas as pd 
import numpy as np
from itertools import cycle
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import streamlit.components.v1 as components
import base64
import json
import smtplib
import time
import datetime
import time
from datetime import  date, datetime, time
import pytz

from google.cloud import firestore
from google.oauth2 import service_account

######################################################################################################
				#Configurações da página
######################################################################################################

st.set_page_config(
     page_title="Cordax",
     layout="wide",
)

######################################################################################################
				#Configurando acesso ao firebase
######################################################################################################
textkey_2 = """{\n  \"type\": \"service_account\",\n  \"project_id\": \"lid-forms\",\n  \"private_key_id\": \"de4fcc45d24308eaa9101b4d4d651c0e1f1c192e\",\n  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCQL7wXeUw7bxgB\\n0kivlcQyVhrBW+ufV1cgv1ySMjqhBxuGK6/4x3Po2/a/phcPxYN7hfsmcq1ZmCMx\\nMHU2TicbRtxA0XqXCi1wfbHYUQk49fT7SJRI9R5C3cCq6hicAYXAdC0BCqvXcmB7\\n8JSRBhdiLmMziQlcb1OkKtTrMkg8/2xhPXVQ8snBzYxrcpGL70IUMW/4FKdABBxg\\ne1uV8Xs11e3pWqQVNxd6FKnanBg/88/wleMb0wZRc0ULhrVEJCFYX8ycjLgoMn4+\\nKNDXdl7zs41IoEdSqs9VTjrrJFGPE6lxUO/qb4FE76qU/4BEmyXjiggLFpu+mjOO\\n0JvN2E6xAgMBAAECggEAB0NISQcUoR0doKCG2xqtqSVvhT7hQFj7bAxc7YZMhWZL\\na3eRjnP+3C4RoKINS6o/eb42zOnTiThMdC1Z3MmUrF87jU5KoQdjtjoL9nalLXKC\\nNmgiWVxze5saRIxfKfiPqVvmFRqEVmljVSA6COYS0SC/YXitI96oYBQXk939XTPN\\nz5LxXyubM00vK1MgdCw8lMajE0l1w7FkqyupolStYeX8l23Kfp6o/Kte/IdZpWR6\\ngefnMEvVCUorNjpuFlvOQrxgm6ygAsuFglRshPqXzUS9761TyBcKPdr4znAA3gns\\nrEqi+6Lrh9xz+t5K8aHodjzvNHQ9yjAiGZHZsoO5WQKBgQDK7IXXslOz7lJ5ZLSl\\njJRtLbs6C0cOmmf+7UQXJmtsL0OHsYgWMzTtrqEo2EqCq0C8UCvCCyUs/d0LrwU4\\n40U9+CUYQMP9PtezqK23XFuLg7upJzY2AH3mNkRr8CMCuyWisw+W/o8QF6jUijtP\\nT0JIrdYyfrGUEx+JnogW4pW+pQKBgQC15j3D/0zRBaM71DjXGc9UDX2M7V56e07S\\nsEJvvzTPbh86VQ3sZTVPoC1jXhV/IzyT3+uxMvrNhEwP15pQzLkMW2J/uZzI3Q+L\\nvhUl6Lk8RIMTFFO2CkNfugPZwPmUxe9/Cu0y9AbeBR7v1zouxFkaNAEkMOrpQ3Ds\\nDwWqLbL+HQKBgAlzMlh1KYi7lIOquO7suQzMkGeHluuLLUSl8AHT/DSxjseG8Pt3\\nrwNSmpa4W9/x8bXTVfZXZofN2rlskSWxD8xu/es/OOFWR91KAa0EVA8PN3INLW0e\\nYL6T0GPmbvr1lC8bf6JcgHUTZP1g4poy6rdPwSXg2Iw4x8M06smGC8sxAoGBAKAx\\nKGwXxhq+kEb8WyJ0BHbNeqhF01KijYRW3etzxJp5LN8+UIjDiPOa6N392YiiC5Nf\\nPD5N2zprLGE3Sxulb8JGKLS7TixHIo261P0RuzAsVhLTb/V9jGAdfY6juCkhOA32\\nHXcmGXYlpF0senz9RkshSXAJ9JeBYU1C3YZFwMCxAoGAaFm980daY3c3P/6mSWC6\\nTImniGbAUbUNFxpC3VUcDTtaC4WtGNe5vcVbvPxWXqBTPo8S7q5eq0JWJipfy4Gp\\ncU3+qMM+Z9jLwasmwKAjN066BH1gPC6AB9m+T2U/N6EY1mTp+DEYfFGhwJCB9coC\\nJ2krpcK4f+zsV7XGgnwUhic=\\n-----END PRIVATE KEY-----\\n\",\n  \"client_email\": \"firebase-adminsdk-r4dlw@lid-forms.iam.gserviceaccount.com\",\n  \"client_id\": \"101767194762733526952\",\n  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-r4dlw%40lid-forms.iam.gserviceaccount.com\"\n}\n"""


# Pega as configurações do banco do segredo
key_dict = json.loads(textkey_2)
creds = service_account.Credentials.from_service_account_info(key_dict)

# Seleciona o projeto
db = firestore.Client(credentials=creds, project="lid-forms")

# Ajustando fuso

tz = pytz.timezone('America/Bahia')

###########################################################################################################################################
#####                    			funcoes                                                                            #########
###########################################################################################################################################

# Define cores para os valores validos ou invalidos
def color(val):
	if val == 'invalido':
		color = 'red'
	else:
		color = 'white'
	return 'background-color: %s' % color
	
#leitura de dados do banco
@st.cache
def load_colecoes(colecao, colunas):
	# dicionario vazio
	dicionario = {}
	index = 0
	
	try:
		# Define o caminho da coleção do firebase
		posts_ref = db.collection(colecao)	
		
		# Busca todos os documentos presentes na coleção e salva num dataframe
		for doc in posts_ref.stream():
			dic_auxiliar = doc.to_dict()
			dicionario[str(index)] = dic_auxiliar
			index += 1
		# Transforma o dicionario em dataframe
		df = pd.DataFrame.from_dict(dicionario)
		
		# troca linhas com colunas
		df = df.T
		
		# Transforma string em tipo data
		df['Data'] = pd.to_datetime(df['Data'])
		
		# Ordena os dados pela data
		df = df.sort_values(by=['Data'], ascending=False)
		
		# Remove o index
		df = df.reset_index(drop=True)
		
		# Ordena as colunas
		df = df[colunas]
		return df
	except:
		#st.info('Nao foi possivel carregar valores do banco, serao colocados valores padrao no DataFrame')
		
		fruits = ["Apple", "Pear", "Peach", "Banana"]

		colunas_dict = dict.fromkeys(colunas, "1")
		#df = pd.DataFrame.from_dict(colunas_dict)
		df = pd.DataFrame.from_dict(colunas_dict, orient='index')
		#st.write(df.T)
		return df.T
	
def ajuste_dados(df):
	# seleciona a primeira linha e a transforma em coluna
	df_row0 = df.iloc[0,:].T
	
	#filtra nome e data
	nome_last = df_row0.loc['Nome']
	data_last = df_row0.loc['Data']
	
	# remove nome e data
	df_row0 = df_row0.drop(['Data', 'Nome'], axis=0)
	
	# reseta index (index vira uma coluna)
	df_row0 = df_row0.reset_index()
	
	# Renomeia a coluna dos valores
	df_row0.rename(columns={0: "V"}, inplace=True)
	
	# Separa o index em Medidas e L (linhas)
	df = pd.DataFrame(df_row0['index'].str.split('_',1).tolist(), columns = ['Medidas','L'])
	
	# Adiciona os valores de volta no dataframe
	df['V'] = df_row0['V']

	# retorna o nome, data e dataset organizado para ser editado e exibido no html
	return nome_last, data_last, df

###########################################################################################################################################
#####                    			cofiguracoes aggrid							                #######
###########################################################################################################################################
def config_grid(height, df, lim_min, lim_max, customizar):
	sample_size = 12
	grid_height = height

	return_mode = 'AS_INPUT'
	return_mode_value = DataReturnMode.__members__[return_mode]
	#return_mode_value = 'AS_INPUT'

	update_mode = 'VALUE_CHANGED'
	update_mode_value = GridUpdateMode.__members__[update_mode]
	#update_mode_value = 'VALUE_CHANGED'

	#enterprise modules
	enable_enterprise_modules = False
	enable_sidebar = False

	#features
	fit_columns_on_grid_load = customizar
	enable_pagination = False
	paginationAutoSize = False
	use_checkbox = False
	enable_selection = False
	selection_mode = 'single'
	rowMultiSelectWithClick = False
	suppressRowDeselection = False

	if use_checkbox:
		groupSelectsChildren = True
		groupSelectsFiltered = True

	#Infer basic colDefs from dataframe types
	gb = GridOptionsBuilder.from_dataframe(df)
	
	
	#customize gridOptions
	if customizar:
		gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
		gb.configure_column("Medidas", editable=False)
		gb.configure_column('L', editable=False)
		gb.configure_column('V', type=["numericColumn"], precision=5)

		#configures last row to use custom styles based on cell's value, injecting JsCode on components front end
		func_js = """
		function(params) {
		    if (params.value > %f) {
			return {
			    'color': 'black',
			    'backgroundColor': 'orange'
			}
		    } else if(params.value <= %f) {
			return {
			    'color': 'black',
			    'backgroundColor': 'orange'
			}
		    } else if((params.value <= %f) && (params.value >= %f)) {
			return {
			    'color': 'black',
			    'backgroundColor': 'white'
			}
		    } else {
			return {
			    'color': 'black',
			    'backgroundColor': 'red'
			} 
		    } 
		};
		"""%(lim_max, lim_min, lim_max, lim_min)
		
		cellsytle_jscode = JsCode(func_js)

		gb.configure_column('V', cellStyle=cellsytle_jscode)

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
	return gridOptions, grid_height, return_mode_value, update_mode_value, fit_columns_on_grid_load, enable_enterprise_modules

###########################################################################################################################################
#####                    			Teste											########
###########################################################################################################################################

# definicao das telas da aplicacao
telas = ['Kiss Block (1)','Kiss Block (2)','Bubble Form (1)','Bubble Form (2)','Bubble Form (3)','1st Rivet (1)','1st Rivet (2)','2nd Rivet (1)','2nd Rivet (2)','Score (1)','Score (2)','Panel Form (1)','Panel Form (2)','Panel Form (3)','Panel Form (4)','Strake (1)','Strake (2)']

# Menu externo ao formulario
aba, i01 = st.beta_columns([4,14])	
sel_tela = aba.selectbox('Selecione o ferramental', options=telas)
nomes = ['Mario', 'Carvalho']
# Input de informacoes de nome e data
nome = i01.selectbox('Nome do colaborador:', nomes)
	
# Tela Score1	
if sel_tela == 'Kiss Block (1)':

	#input de limites e das colunas do data frame

	val_max = [50, 50, 50, 50, 50]
	val_min = [0.1, 0.1, 0.1, 0.1, 0.1]
	colunas =    ['Nome','Data','SLC_A','SLC_B','SLC_C','SLC_D','SUBB_A','SUBB_B','SUBB_C','SUBB_D','TP_A','TP_B','TP_C','TP_D','SUC_A','SUC_B','SUC_C','SUC_D','SLRI_A','SLRI_B','SLRI_C','SLRI_D']
		  	
	# carrega dados do banco de dados
	df_firebase = load_colecoes('teste', colunas)

	# filtra o ultimo dado para exibir para o usuario
	nome_last, data_last, df = ajuste_dados(df_firebase)

	# carrega pagina html
	htmlfile = open('score_1.html', 'r', encoding='utf-8')
	source = htmlfile.read()
	
	# carrega imagem da tela do cordax
	file_ = open("score_1.png", "rb")
	contents = file_.read()
	data_url = base64.b64encode(contents).decode("utf-8")
	file_.close()
	
	# cria dicionario vazio
	dic = {} 

	# define as colunas da pagina
	t1, html, t2 = st.beta_columns([4,10,4])
	
	df_validacao = pd.DataFrame()
	titulo = ['SPACER LOWER CAP', 'SPACER UPPER BLANK BEAD', 'TOOLING PLATE', 'SPACER UPPER CAP', 'SPACER LOWER RIVET INSERT']
	medida = ['SLC','SUBB','TP','SUC','SLRI']
	index = 0 
	limits = 0	
	for (mi, ma, med, tit) in zip(val_min, val_max, medida, titulo):
		
		if index < 4:
			with t1:
				gridOptions, grid_height, return_mode_value, update_mode_value, fit_columns_on_grid_load, enable_enterprise_modules = config_grid(147, df, mi, ma, True)
				t1.write(tit)
				response = AgGrid(
				    df[df['Medidas'] == med], 
				    gridOptions=gridOptions,
				    height=grid_height, 
				    width='100%',
				    data_return_mode=return_mode_value, 
				    update_mode=update_mode_value,
				    fit_columns_on_grid_load=fit_columns_on_grid_load,
				    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
				    enable_enterprise_modules=enable_enterprise_modules)
				df_auxiliar = response['data']
				df_validacao = pd.concat([df_validacao, df_auxiliar])
				if (df_auxiliar['V'].astype(float) > ma).any() | (df_auxiliar['V'].astype(float) < mi).any():
					limits = 1

		else:
			with t2:
				gridOptions, grid_height, return_mode_value, update_mode_value, fit_columns_on_grid_load, enable_enterprise_modules = config_grid(147, df, mi, ma, True)
				t2.write(tit)
				response = AgGrid(
				    df[df['Medidas'] == med], 
				    gridOptions=gridOptions,
				    height=grid_height, 
				    width='100%',
				    data_return_mode=return_mode_value, 
				    update_mode=update_mode_value,
				    fit_columns_on_grid_load=fit_columns_on_grid_load,
				    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
				    enable_enterprise_modules=enable_enterprise_modules)
				df_auxiliar = response['data']
				df_validacao = pd.concat([df_validacao, df_auxiliar])
				if (df_auxiliar['V'].astype(float) > ma).any() | (df_auxiliar['V'].astype(float) < mi).any():
					limits = 1
		index += 1
		
	df_validacao['V'] = pd.to_numeric(df_validacao['V'], errors='coerce')
	
	if df_validacao['V'].isnull().sum() > 0:
		t2.error('Caracter invalido no campo Valor')
	else:
		t2.write('Avalicao das medidas')
			
		df_group = df_validacao[['L', 'V']].groupby(['L']).sum() 
		df_group['Max'] = [ 123, 4321, 123, 4321]
		df_group['Min'] = [ 13, 43, 3, 1]
		df_group['Resultado'] = np.where(((df_group['V'] < df_group['Max']) & (df_group['V'] > df_group['Min'])), 'valido', 'invalido')
		t2.write(df_group.style.applymap(color, subset=['Resultado']))
		
		dados_invalidos = 'invalido' in df_group.values
		if not dados_invalidos and limits == 0:
			# Preparando dados para escrita no banco
			
			dic = {}
			for index, row in df_validacao.iterrows():
				chave = row['Medidas'] + '_' + row['L']
				dic[chave] = str(row['V'])
			dic['Nome'] = nome
			dic['Data'] = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
			#st.write(dic)
			
			submitted = t2.button('Salvar configuracao?') 
			if submitted:

				# Limpa cache
				caching.clear_cache()
				
				# Transforma dados do formulário em um dicionário
				keys_values = dic.items()
				new_d = {str(key): str(value) for key, value in keys_values}

				# Verifica campos não preenchidos e os modifica
				for key, value in new_d.items():
					if (value == '') or value == '[]':
						new_d[key] = '-'

				# Armazena no banco
				try:
					doc_ref = db.collection("teste").document()
					doc_ref.set(new_d)
					t2.success('Dados armazenados com sucesso!')
				except:
					t2.error('Falha ao armazenar formulário, tente novamente ou entre em contato com suporte!')		

	# HTML: html com imagens e dados				
	with html:
		components.html(source.format(image=data_url,
					       v0=df.iloc[0,2],
					       v1=df.iloc[1,2],
					       v2=df.iloc[2,2],
					       v3=df.iloc[3,2],
					       v4=df.iloc[4,2],
					       v5=df.iloc[5,2],
					       v6=df.iloc[6,2],
					       v7=df.iloc[7,2],
					       v8=df.iloc[8,2],
					       v9=df.iloc[9,2],
					       v10=df.iloc[10,2],
					       v11=df.iloc[11,2],
					       v12=df.iloc[12,2],
					       v13=df.iloc[13,2],
					       v14=df.iloc[14,2],
					       v15=df.iloc[15,2],
					       v16=df.iloc[16,2],
					       v17=df.iloc[17,2],
					       v18=df.iloc[18,2],
					       v19=df.iloc[19,2],
					       nome = 'Ultima alteracao feita por: ' + nome_last,
					       data = 'Data: ' + str(data_last)),
					        height=875)
	
	st.subheader('Historico de medidas')			        
	gridOptions, grid_height, return_mode_value, update_mode_value, fit_columns_on_grid_load, enable_enterprise_modules = config_grid(250, df_firebase, 0, 0, False)
	response = AgGrid(
		    df_firebase, 
		    gridOptions=gridOptions,
		    height=grid_height, 
		    width='100%',
		    data_return_mode=return_mode_value, 
		    update_mode=update_mode_value,
		    fit_columns_on_grid_load=fit_columns_on_grid_load,
		    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
		    enable_enterprise_modules=enable_enterprise_modules)

# Tela Bubble form 2
if sel_tela == 'Bubble Form (2)':

	#input de limites e das colunas do data frame
	val_max = [50, 50, 50, 50, 50, 50, 50, 50]
	val_min = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
	colunas = ['Nome', 'Data', 'SURI_A', 'SURI_B', 'SURI_C', 'SURI_D', 'SUC_A', 'SUC_B', 'SUC_C', 'SUC_D', 'WSUC_A', 'WSUC_B', 'WSUC_C', 'WSUC_D','SMID_A', 'SMID_B', 'SMID_C', 'SMID_D',
	 'SLRI_A', 'SLRI_B', 'SLRI_C', 'SLRI_D', 'TP_A', 'TP_B', 'TP_C', 'TP_D', 'SLC_A',  'SLC_B', 'SLC_C', 'SLC_D', 'WSLC_A', 'WSLC_B',  'WSLC_C', 'WSLC_D']
		  	
	# carrega dados do banco de dados
	df_firebase = load_colecoes('teste_2', colunas)

	# filtra o ultimo dado para exibir para o usuario
	nome_last, data_last, df = ajuste_dados(df_firebase)

	# carrega pagina html
	htmlfile = open('bubble_form_2.html', 'r', encoding='utf-8')
	source = htmlfile.read()
	
	# carrega imagem da tela do cordax
	file_ = open("bubble_form_2.png", "rb")
	contents = file_.read()
	data_url = base64.b64encode(contents).decode("utf-8")
	file_.close()
	
	# cria dicionario vazio
	dic = {} 
	
	# define as colunas da pagina
	t1, html, t2 = st.beta_columns([4,10,4])
	
	df_validacao = pd.DataFrame()
	titulo = ['SPACER UPPER RIVET INSERT', 'SPACER UPPER CAP','WEAR SPACER UPPER CAP', 'SPACER MONTHI, D', 'SPACER LOWER RIVET INSERT', 'TOOLING PLATE', 'SPACER LOWER CAP', 'WEAR SPACER LOWER CAP']
	medida = ['SURI', 'SUC', 'WSUC', 'SMID', 'SLRI', 'TP', 'SLC', 'WSLC']
	index = 0 
	limits = 0	
	for (mi, ma, med, tit) in zip(val_min, val_max, medida, titulo):
		
		if index < 4:
			with t1:
				gridOptions, grid_height, return_mode_value, update_mode_value, fit_columns_on_grid_load, enable_enterprise_modules = config_grid(147, df, mi, ma, True)
				t1.write(tit)
				response = AgGrid(
				    df[df['Medidas'] == med], 
				    gridOptions=gridOptions,
				    height=grid_height, 
				    width='100%',
				    data_return_mode=return_mode_value, 
				    update_mode=update_mode_value,
				    fit_columns_on_grid_load=fit_columns_on_grid_load,
				    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
				    enable_enterprise_modules=enable_enterprise_modules)
				df_auxiliar = response['data']
				df_validacao = pd.concat([df_validacao, df_auxiliar])
				if (df_auxiliar['V'].astype(float) > ma).any() | (df_auxiliar['V'].astype(float) < mi).any():
					limits = 1

		else:
			with t2:
				gridOptions, grid_height, return_mode_value, update_mode_value, fit_columns_on_grid_load, enable_enterprise_modules = config_grid(147, df, mi, ma, True)
				t2.write(tit)
				response = AgGrid(
				    df[df['Medidas'] == med], 
				    gridOptions=gridOptions,
				    height=grid_height, 
				    width='100%',
				    data_return_mode=return_mode_value, 
				    update_mode=update_mode_value,
				    fit_columns_on_grid_load=fit_columns_on_grid_load,
				    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
				    enable_enterprise_modules=enable_enterprise_modules)
				df_auxiliar = response['data']
				df_validacao = pd.concat([df_validacao, df_auxiliar])
				if (df_auxiliar['V'].astype(float) > ma).any() | (df_auxiliar['V'].astype(float) < mi).any():
					limits = 1
		index += 1
		
	df_validacao['V'] = pd.to_numeric(df_validacao['V'], errors='coerce')
	
	if df_validacao['V'].isnull().sum() > 0:
		t2.error('Caracter invalido no campo Valor')
	else:
		t2.write('Avalicao das medidas')
			
		df_group = df_validacao[['L', 'V']].groupby(['L']).sum() 
		df_group['Max'] = [ 123, 4321, 123, 4321]
		df_group['Min'] = [ 13, 43, 3, 1]
		df_group['Resultado'] = np.where(((df_group['V'] < df_group['Max']) & (df_group['V'] > df_group['Min'])), 'valido', 'invalido')
		t2.write(df_group.style.applymap(color, subset=['Resultado']))
		
		dados_invalidos = 'invalido' in df_group.values
		if not dados_invalidos and limits == 0:
			# Preparando dados para escrita no banco
			
			dic = {}
			for index, row in df_validacao.iterrows():
				chave = row['Medidas'] + '_' + row['L']
				dic[chave] = str(row['V'])
			dic['Nome'] = nome
			dic['Data'] = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
			#st.write(dic)
			
			submitted = t2.button('Salvar configuracao?') 
			if submitted:

				# Limpa cache
				caching.clear_cache()
				
				# Transforma dados do formulário em um dicionário
				keys_values = dic.items()
				new_d = {str(key): str(value) for key, value in keys_values}

				# Verifica campos não preenchidos e os modifica
				for key, value in new_d.items():
					if (value == '') or value == '[]':
						new_d[key] = '-'

				# Armazena no banco
				try:
					doc_ref = db.collection("teste_2").document()
					doc_ref.set(new_d)
					t2.success('Dados armazenados com sucesso!')
				except:
					t2.error('Falha ao armazenar formulário, tente novamente ou entre em contato com suporte!')		

	# HTML: html com imagens e dados				
	with html:
		components.html(source.format(image=data_url,
					       v0=df.iloc[0,2],
					       v1=df.iloc[1,2],
					       v2=df.iloc[2,2],
					       v3=df.iloc[3,2],
					       v4=df.iloc[4,2],
					       v5=df.iloc[5,2],
					       v6=df.iloc[6,2],
					       v7=df.iloc[7,2],
					       v8=df.iloc[8,2],
					       v9=df.iloc[9,2],
					       v10=df.iloc[10,2],
					       v11=df.iloc[11,2],
					       v12=df.iloc[12,2],
					       v13=df.iloc[13,2],
					       v14=df.iloc[14,2],
					       v15=df.iloc[15,2],
					       v16=df.iloc[16,2],
					       v17=df.iloc[17,2],
					       v18=df.iloc[18,2],
					       v19=df.iloc[19,2],
					       v20=df.iloc[20,2],
					       v21=df.iloc[21,2],
					       v22=df.iloc[22,2],
					       v23=df.iloc[23,2],
					       v24=df.iloc[24,2],
					       v25=df.iloc[25,2],
					       v26=df.iloc[26,2],
					       v27=df.iloc[27,2],
					       v28=df.iloc[28,2],
					       v29=df.iloc[29,2],
					       v30=df.iloc[30,2],
					       v31=df.iloc[31,2],		       
					       nome = 'Ultima alteracao feita por: ' + nome_last,
					       data = 'Data: ' + str(data_last)),
					        height=875)
	
	st.subheader('Historico de medidas')			        
	gridOptions, grid_height, return_mode_value, update_mode_value, fit_columns_on_grid_load, enable_enterprise_modules = config_grid(250, df_firebase, 0, 0, False)
	response = AgGrid(
		    df_firebase, 
		    gridOptions=gridOptions,
		    height=grid_height, 
		    width='100%',
		    data_return_mode=return_mode_value, 
		    update_mode=update_mode_value,
		    fit_columns_on_grid_load=fit_columns_on_grid_load,
		    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
		    enable_enterprise_modules=enable_enterprise_modules)
        
	#st.write(df_firebase.T)





