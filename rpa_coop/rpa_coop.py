import os, requests, json, time, re
import pandas as pd
from sqlalchemy import create_engine
from urllib.request import urlretrieve
import urllib.parse
import site
user_site_packages = site.getusersitepackages()
user_site_packages = user_site_packages.replace('Roaming', 'Local\\Programs').replace('site-packages','Lib\\site-packages')



class Fluid:

    def __init__(self, cod_usuario_fluid=os.getenv('fluid_cod_user')):
        self.id_usuario = cod_usuario_fluid
        self.token_fluid = os.getenv('token_api_fluid')
        self.organizacao = os.getenv('fluid_organizacao')
        self.headers = {'organization': self.organizacao,'authorization': self.token_fluid}
        self.url_api = os.getenv('fluid_url_api')
        self.url_request = os.getenv('fluid_url_request')
        self.user_fluid = os.getenv('fluid_user_web')
        self.senha_fluid = os.getenv('pw_fluid')
        self.ip_planning = os.getenv('ip_planning')
        self.user_planning = os.getenv('user_planning')
        self.pwd_planning = os.getenv('pw_bd_planning')
        
 
    def anexar_arquivo_fluid(self, cod_processo:str, path_file:str, tipo_arquivo:str):
        '''
            num_processo = '497305'\n
            path_file = 'C:\\Temp\\teste.xlsx'\n
            id_doc_fluid = '417'\n
            api_upload_anexo_fluid( num_processo, path_file, id_doc_fluid )
        '''
        nome_arquivo = os.path.basename(path_file).split('/')[-1]
        url = f'{self.url_api}/processos/anexar' 
        payload = {"processo": cod_processo, "nome": nome_arquivo, "tipo": tipo_arquivo}
        res_fase1 = requests.request("POST", url, json=payload, headers=self.headers)
        time.sleep(10)
        cod_res_api = str(res_fase1.status_code)
        print('anexar arquivo fase1 retornou: ', cod_res_api)
        
        payload = res_fase1.json()
        url = payload['url']
        response = requests.post(url, files={
                                            "AWSAccessKeyId": payload['fields'][0]['AWSAccessKeyId'],
                                            "key": payload['fields'][0]['key'],
                                            "policy": payload['fields'][0]['policy'],
                                            "signature": payload['fields'][0]['signature'],
                                            "file": open(path_file, "rb")})
        time.sleep(10)
        cod_res_api = str(response.status_code)
        print('anexar arquivo fase2 retornou: ', cod_res_api)
        # observacao, os time.sleep(10) sao uma segurança para não protocolar antes de terminar o upload e corromper o arquivo.
        # caso o arquivo seja muito grande pode ir testando com uma espera maior, ou fazer um if de espera por tamanho de arquivo.
        time.sleep(10)
        
        
    def ler_dados_de_excel_no_fluid(self, num_processo: str):
        endpoint = f"{self.url_api}/processos/download"
        data = json.dumps({"hashs":[], "processo": num_processo})
        res_dicionario = requests.post(url=endpoint, data=data, headers=self.headers, verify=True)
        print("Get_link anexos fluid: ", res_dicionario.status_code)
        if str(res_dicionario.status_code) == '200':
            res_json = res_dicionario.json()
            url = res_json[0]['url']
            response = requests.get(url)
            time.sleep(1)
            df  = pd.read_excel(response.content)
            print(df)
            return df
    
    
    def download_anexo_fluid(self, num_processo: str):
        endpoint = f"{self.url_api}/processos/download"
        data = json.dumps({"hashs":[], "processo": num_processo})
        res_dicionario = requests.post(url=endpoint, data=data, headers=self.headers, verify=True)
        print("Get_link anexos fluid: ", res_dicionario.status_code)
        if str(res_dicionario.status_code) == '200':
            res_json = res_dicionario.json()
            url = res_json[0]['url']
            print()
            destino = f'c:\\temp\\planilha_anexo_fluid.xlsx'
            urlretrieve(url, destino)
            time.sleep(5)
            print('baixou o arquivo:', destino)
            return destino
        else:
            destino = 'arquivo nao encontrado para download'
            print(destino)
            return destino
        
        
    def download_multiplos_anexos_fluid(self, num_processo: str, pasta_destino: str):       
        endpoint = f"{self.url_api}/processos/download"
        data = json.dumps({"hashs":[], "processo": num_processo})
        res_dicionario = requests.post(url=endpoint, data=data, headers=self.headers, verify=True)
        print("Get_link anexos fluid: ", res_dicionario.status_code)
        if str(res_dicionario.status_code) == '200':
            res_json = res_dicionario.json()
            print()
            df_files = pd.DataFrame(res_json)
            destino = str(pasta_destino)
            files = os.listdir(destino)  
            [os.remove(f'{destino}{file}') for file in files]
            time.sleep(5)
            new_files = []
            df_files = df_files[['nome','url']]
            print(df_files)
            
            for nome, url in df_files.values:
                loc = url.find('?')
                extensao = url[loc-4:loc].replace('.','')
                path_file = f'{destino}{nome}.{extensao}'
                urlretrieve(url, path_file)  
                time.sleep(5)
                print('baixou o arquivo em:', path_file)
                new_files.append(path_file)
            return new_files
        else:
            print('arquivo nao encontrado para download')
            
             
    def cancelar_processo_fluid(self, num_processo_fluid):
        ##### Armazenar sessao de login em cookie
        sessao = requests.Session() 
        autenticacao = {'usuario': self.user_fluid, 'senha': self.senha_fluid}
        url_login = f'{self.url_request}/usuario'       
        sessao.post(url_login, data=autenticacao)
        ##### Cancelamento 
        dados = {'mensagem': 'Cancelamento Administrativo', 'parecer': '197', 'tipo_verificacao': '1', 'pes_senha': self.senha_fluid}
        url_cancelamento = f'{self.url_request}/processos/cancelar/parecer/id/{num_processo_fluid}'
        sessao.post(url_cancelamento, data=dados)
    
    
    def depara(self, ua):
        '''
            passamos como parâmetro o cod_agencia\n
            a função retorma o cod_agencia_fluid, codigo cadastrado no fluid
        '''      
        server = self.ip_planning
        user_planning = self.user_planning
        pwd_planning = self.pwd_planning 
        db = 'fluid'
        engine = create_engine(f'mysql+mysqlconnector://{user_planning}:{pwd_planning}@{server}/{db}', pool_recycle=3600)
        sql_select_query = f"SELECT cod_fluid FROM fluid.depara_ag_x_cod_fluid WHERE cod_ag = '{ua}'" 
        try: df_depara = pd.read_sql(sql_select_query, con=engine)
        except: df_depara = pd.read_sql(sql_select_query, con=engine)
        if len(df_depara) > 0:
            for i in df_depara.values:
                cod_fluid = str(i[0])
                return str(cod_fluid)
        else:
            cod_fluid = 0
            return str(cod_fluid)
        
        
    def nodo_e_arvore_para_novo_processo(self, id_tipo_processo):
        '''
            retorna ( id_arvore, nodo_inicial ), referente a arvore VIGENTE\n
            caso não exista vigente, retorna ( id_arvore, nodo_inicial ) referente árvore EM CRIAÇÃO
        '''
        ##### Armazenar sessao de login em cookie
        minha_Session = requests.Session() 
        autenticacao = {'usuario': self.user_fluid, 'senha': self.senha_fluid}
        url_login = f'{self.url_request}/usuario'
        minha_Session.post(url_login, data=autenticacao)
        # ##### get id da arvore
        url_cod_tipo_processo = f'{self.url_request}/cadastro/workflow/versoes/id/{id_tipo_processo}'
        page = minha_Session.get(url_cod_tipo_processo)
        string_html = str(page.content)
        try:
            arr = string_html.split('<tr>')
            tag = [x for x in arr if 'Vigente' in x]
            id_arvore = str(re.findall('\d{3,6}', tag[0])[0])
        except:
            arr = string_html.split('<tr>')
            tag = [x for x in arr if 'Em cria' in x]
            id_arvore = str(re.findall('\d{3,6}', tag[0])[0])
        # ##### get id primeiro nodo
        url_arvore = f'{self.url_request}/cadastro/workflow/index/id/{id_arvore}'
        page = minha_Session.get(url_arvore)
        string_html = str(page.content)
        nodos = re.findall('work_id_pai: \"\d{3,6}\"', string_html)
        nodo_inicial = str(nodos[0].replace('work_id_pai: "','').replace('"',''))
        return id_arvore, nodo_inicial


    def get_sla(self, id_tipo_processo):
        ##### Armazenar sessao de login em cookie
        sessao = requests.Session() 
        autenticacao = {'usuario': self.user_fluid, 'senha': self.senha_fluid}
        url_login = f'{self.url_request}/usuario'
        sessao.post(url_login, data=autenticacao)
        ##### Usar a sessao para acessar outra url da página, autenticando com o cookie
        url_tempos = f'{self.url_request}/cadastro/tipo-processo/tempos/id/{id_tipo_processo}'
        page = sessao.get(url_tempos)
        sla_string = re.findall('(?<=value=").+?(?=" checked)', str(page.text))[0]
        tempo_sla = sla_string.split('"')
        sla = str(tempo_sla[-1])
        return sla
    
    
    def get_nodo_possiveis_destinos(self, cod_processo: str, nome_do_nodo='selecionado_proximo_nodo'):
        '''
            retorna id_nodo, acao\n
            Exemplos: \n
            id_nodo, acao = get_nodo_possiveis_destinos('485012') \n
            id_nodo, acao = get_nodo_possiveis_destinos('485012', 'Devolver ao parecer anterior') \n
            id_nodo, acao = get_nodo_possiveis_destinos('485012', 'Devolver à confecção') \n
            id_nodo, acao = get_nodo_possiveis_destinos('485012', 'Concluir') \n
        '''
        id_nodo, acao, nodo_nome= 0, 0, 'vazio'
        url = f'{self.url_api}/processos/visualizar/{cod_processo}/{self.id_usuario}'
        headers = {"Content-Type": "application/json; charset=utf-8",  "organization": self.organizacao, "Authorization": self.token_fluid }
        response = requests.get(url, headers=headers)
        cod_res_api = str(response.status_code)
        
        if cod_res_api != '200':
            time.sleep(5)
            response = requests.get(url, headers=headers)
            cod_res_api = str(response.status_code)
            
        if cod_res_api == '200': 
            res_json = response.json()
            nome_local = res_json['local']
            local_id = res_json['local_id']
            nodo_atual = res_json['nodo']
            df = pd.DataFrame(res_json['acoes'])
            df.rename(columns={'descricao': 'nome_do_nodo', 'destino': 'codigo_nodo_destino'}, inplace=True)
            print(df)
            for x in df.itertuples():
                nodo_nome = str(x.nome_do_nodo)
                id_nodo = int(x.codigo_nodo_destino)
                acao = int(x.acao)
                if str(nome_do_nodo) == 'selecionado_proximo_nodo' and acao == 0: break
                if nome_do_nodo.upper() in nodo_nome.upper(): break
                else:
                    id_nodo = 0
                    acao = 0
            print()
            print(f'NODO ATUAL ... nodo_atual:   {nodo_atual}, local_atual: {nome_local}, id_local_atual: {local_id}')
            print(f'SELECIONADO... nodo_destino: {id_nodo}, nome_destino: {nodo_nome}, cod_acao: {acao}')
            print()
            return id_nodo, acao
        else:
            msg = str(f'codigo de retorno da api fluid: {cod_res_api}')
            # print(msg)
            # print(response.text)  
            print('processo identificado como novo') 
            print()
            return msg, acao 
        
    
    def criar_processo_rascunho(self, id_tipo_processo:str, id_empresa_origem=1, id_empresa_destino=1, responsavel_destino=2735):
        '''
            id_processo, nodo_inicial = post_criar_processo(id_tipo_processo)\n
            ou\n
            id_processo, nodo_inicial = post_criar_processo(id_tipo_processo, id_empresa_origem=cod_agencia, id_empresa_destino=cod_agencia)
        '''
        url_final = f'{self.url_api}/processos/novo'
        headers = {"Content-Type": "application/json; charset=utf-8", "organization": self.organizacao, "Authorization": self.token_fluid }
        
        if id_empresa_origem != 1: id_empresa_origem = self.depara(id_empresa_origem)
        if id_empresa_destino != 1: id_empresa_destino = self.depara(id_empresa_destino)
        
        id_versao_arvore, nodo_inicial = self.nodo_e_arvore_para_novo_processo(str(id_tipo_processo)) # pega a arvore vigente, ou em criação
        tempo_minutos = self.get_sla(id_tipo_processo)
        
        obj_acao = {
            "tipo_processo": id_tipo_processo, # id do tipo de processo fluid
            "tempo": tempo_minutos, # tempo em minutos
            "responsavel_criacao": self.id_usuario, # id do usuário fluid
            "responsavel_origem": self.id_usuario, # id do usuário fluid
            "responsavel_destino": responsavel_destino,
            "empresa_origem": id_empresa_origem, 
            "empresa_destino": id_empresa_destino,
            "versao_processo": id_versao_arvore # versao da arvore do processo, abra a arvore e veja no final da url o id
            }
        
        # no Método POST passar os parametros {url, headers, json}
        response = requests.post(url_final, headers=headers, json=obj_acao)
        cod_res_api = str(response.status_code)
        print('codigo de retorno da api fluid: ', cod_res_api)  
        
        if cod_res_api == '200':
            res_dict = response.json()
            id_processo = int(res_dict['id'])
            # print(id_processo)
            return id_processo, nodo_inicial
        else:   
            print(response.text)
            return 0, 0


    def get_relatorio_fluid(self, id_relatorio_fluid, data_inicio, data_final, situacao=2):
        '''
            data inicio = dd/mm/yyyy\n
            data_final = dd/mm/yyyy\n
            situacao = 0 (todos os processos)\n
            situacao = 1 (processos em aberto)\n
            situacao = 2 (processos encerrados)\n
            
            df2 = get_relatorio_fluid('357', '19/01/2021', '19/12/2022')\n
            ou\n 
            df2 = get_relatorio_fluid('357', '19/01/2021', '19/12/2022', situacao = 0 )\n  
        '''
        df = pd.DataFrame()
        ##### Período do relatório
        id_relatorio = str(id_relatorio_fluid)
        rel_inicio = str(data_inicio)
        rel_final = str(data_final)

        ##### Armazenar sessao de login em cookie
        sessao = requests.Session()        
        autenticacao = {'usuario': self.user_fluid, 'senha': self.senha_fluid}
        url_login = f'{self.url_request}/usuario'
        sessao.post(url_login, data=autenticacao)

        ##### Usar a sessao para acessar outra url da página, autenticando com o cookie
        url_relatorio = f'{self.url_request}/relatorio/visualizar/processo/id/{id_relatorio}?dt_ini={rel_inicio}&dt_fim={rel_final}&situacao={situacao}&itens_pagina=10&go=true' 
        page = sessao.get(url_relatorio)
        ##### consulta 10 linhas para capturar o total de linhas ( mostrado no final da página no texto "Mostrando 1 à 292 de 292 itens" )
        total_linhas = re.findall("((?<=Mostrando 1).+?(?= itens</))", str(page.content))
        if total_linhas:
            linhas = str(total_linhas[0])[16:]
            # consulta novo relatorio com o valor total de linhas encontradas
            url_relatorio = f'{self.url_request}/relatorio/visualizar/processo/id/{id_relatorio}?dt_ini={rel_inicio}&dt_fim={rel_final}&situacao={situacao}&itens_pagina={linhas}&go=true'
            page = sessao.get(url_relatorio)
            tabs = pd.read_html(page.content)   
            df = tabs[0] 
            print(df)
            return df
        else:
            print('relatório nao retornou dados para o período')
            return df
        
        
    def get_dados_processo(self, cod_processo):
        '''
            retorna valores de campo comuns e campos tabela, existentes no processo fluid\n
            retorna no formato de um dataframe do pandas
        '''
        df1 = pd.DataFrame()
        url = f'{self.url_api}/processos/visualizar/{cod_processo}/{self.id_usuario}'
        headers = { "Content-Type": "application/json; charset=utf-8", "organization": self.organizacao, "Authorization": self.token_fluid }
        response = requests.get(url, headers=headers)
        cod_res_api = str(response.status_code)
        if cod_res_api != '200':
            time.sleep(5)
            response = requests.get(url, headers=headers)
            cod_res_api = str(response.status_code)
        
        if cod_res_api == '200':
            campos = response.json()
            df1 = pd.DataFrame(campos['atributos'])
            df1["id"] = df1["id"].astype('str')
            
            cont = 0
            for x in df1.itertuples():
                if '[[' in str(x.valor):
                    campo_tabela = campos['atributos'][cont]['valor']
                    L1 = []
                    [L1.append(j) for i in campo_tabela for j in i]
                    df2 = pd.DataFrame(L1)
                    df1 = pd.concat([df1, df2])
                    df1[['nome']] = df1[['nome']].fillna('Campo Tabela')
                    print()
                cont = cont + 1         
        else:
            cod_res_api = str(response.status_code)
            print('codigo de retorno da api fluid: ', cod_res_api) 
            print(cod_res_api.text)             
        return df1


    def get_processos_fluid(self, array_cod_tipo_processos=[0], id_local_de_processo=542):  
        ''' 
            #### Exemplos:
            - Todos tipo de processos, para usuario e local_id do robô \n
            - df_processos = get_processos_fluid() \n
            - Processos específicos, para usuario e local_id do robô \n
            - df_processos = get_processos_fluid( [941] ) \n
            - df_processos = get_processos_fluid( [852, 941, 792] ) \n
            - df_processos = get_processos_fluid( range(100,800) ) \n
            - Processos , usuario e local_id específicados. \n
            - df_processos = get_processos_fluid( [150, 160],  id_usuario=2535, id_local_de_processo=1 ) \n
        '''
        # entrada do parametro, pode ser int ou str, porque tratei na linha abaixo.
        if array_cod_tipo_processos[0] != 0:
            fluxos_permitidos = [str(x) for x in array_cod_tipo_processos]
        url = f'{self.url_api}/processos/inbox/{self.id_usuario}/01'
        headers = {"Content-Type": "application/json; charset=utf-8", "organization": self.organizacao, "Authorization": self.token_fluid }

        response = requests.get(url, headers=headers)
        cod_res_api = str(response.status_code) 
        
        if cod_res_api != '200':
            time.sleep(5)
            response = requests.get(url, headers=headers)
            cod_res_api = str(response.status_code)
    
        df1 = pd.DataFrame()
        
        if cod_res_api == '200':
            response_dict = response.json() 
            processos = response_dict['processos']
            df = pd.DataFrame(processos)
            df = df[['numero', 'tipo_id','tipo', 'local_id', 'local']] 
            df = df.astype('str')
            if array_cod_tipo_processos[0] != 0:
                df = df.query(f'tipo_id in {fluxos_permitidos}')
            df = df.query(f'local_id == "{id_local_de_processo}"') # Local de processo 542 - Sede Automacao
            df1 = df[:]
            df1.rename(columns={'numero': 'processo_fuid', 'tipo_id': 'id_fluxo_fluid', 'tipo': 'nome_fluxo_fluid'}, inplace=True)
        else:
            print('codigo de retorno da api fluid: ', cod_res_api) 
            print(response.text)
        return df1
    
    
    def gravar_dados_campos_tabela(self, cod_processo:int, id_tipo_processo:int, id_tabela:int, id_campos_tabela:list, campo_e_valor:list, abertura_de_processo=False):
        '''
        CHAMANDO A FUNÇÃO E PASSANDO OS PARÂMETROS \n
        id_tipo_processo = int(945) \n
        cod_processo = '497305' \n
        id_tabela = 3815 - eh o id do campo('Quantidade') qtd linhas da tabela \n
        id_campos_tabela = [5221, 2012] - ids dos campos referente a uma linha da tabela \n

        Passar uma lista de dicionarios, {id_campo: 'valor_a_preencher'} \n
        campo_e_valor = [{5221: 'Galileo Galilei', 2012: '111.222.333-55'}, \n
                        {5221: 'Isaac Newton.', 2012: '333.222.453-77'}, \n
                        {5221: 'Nikola Tesla.', 2012: '555.023.333-99'}] \n

        gravar_dados_campo_tabela(cod_processo, id_tipo_processo, id_tabela, id_campos_tabela, campo_e_valor) \n
        '''

        url = f'{self.url_api}/processos/salvar-campo-tabela'
        headers = {"organization": self.organizacao, "Authorization": self.token_fluid }
        
        lista_de_campos = [] 
        for x in id_campos_tabela:
            dic = {"ttableId": x, "tipoCalc": 0, "value": ""}       
            lista_de_campos.append(dic)
            
        cont = 1
        dict_valores = {}
        for i in campo_e_valor:
            aux = []
            for j in i:
                dict_aux = {}
                print(j, i[j])
                dict_aux["value"] = i[j] 
                dict_aux["ttableId"] = j 
                aux.append(dict_aux)
            cont = cont-1
            indice = str(cont)
            dict_valores[f'{indice}'] = aux
        
        nodo, acao = self.get_nodo_possiveis_destinos(cod_processo)
        if 'codigo de retorno' in str(nodo) or abertura_de_processo:
            id_arvore, nodo = self.nodo_e_arvore_para_novo_processo(id_tipo_processo)
            acao = 0
            
        param = { 
                "processo": cod_processo, 
                "destino": nodo, 
                "usuario": self.id_usuario, 
                "campo": { 
                    "valueTable": dict_valores,
                    "ttableId": id_tabela,
                    "quant": 0,
                    "calcTable": lista_de_campos  
                    }
        } 
                
        res = requests.post(url, headers=headers, json=param)
        print('codigo de retorno da api fluid: ', res.status_code)  
    
    
    def gravar_dados_campos_comuns(self, cod_processo:str, id_tipo_processo:str, dict_campos:dict, abertura_de_processo=False):
        '''
            Dicionario {ID:'valor', ID:'valor'} \n
            Conteúdo que vai escrever nos campos \n  
            campos = {5170: '3', \n
                    5171:'2500', \n
                    5177:'123123', \n
                    5175: 'sede', \n
                    5184: '03/02/2023'} \n
            id_tipo_processo = int(945) \n
            cod_processo = '497305' \n
            gravar_dados_multiplos_campos(cod_processo, id_tipo_processo, campos) \n
        '''   
        nodo, acao = self.get_nodo_possiveis_destinos(cod_processo)
        if 'codigo de retorno' in str(nodo) or abertura_de_processo:
            id_arvore, nodo = self.nodo_e_arvore_para_novo_processo(id_tipo_processo)
            acao = 0
        
        url = f'{self.url_api}/processos/salvar-campos'
        
        headers = {"organization": self.organizacao, "Authorization": self.token_fluid }
        param = { "processo": cod_processo, "destino": nodo, "usuario": self.id_usuario, "campos": dict_campos }

        res = requests.post(url, headers=headers, json=param)
        print('codigo de retorno da api fluid: ', res.status_code) 
    
    
    def protocolar_processo_fluid(self, cod_processo: str, id_tipo_processo: str,  mensagem: str, nome_do_nodo ='selecionado_proximo_nodo', abertura_de_processo= False, acao = 0, empresa_orig=1, empresa_dest=1, usuario_destino=2735):
        ''' 
            post_protocolar_processo_fluid(processo, id_tipo_processo, msg, nome_nodo_destino, empresa_orig, empresa_dest) \n
            post_protocolar_processo_fluid('497305', '945', 'automação realizada') \n
            post_protocolar_processo_fluid('497305', '945', 'automação realizada', empresa_orig=68, empresa_dest=68) \n
            post_protocolar_processo_fluid('497305', '945', 'automação realizada', 'Devolver') \n
            post_protocolar_processo_fluid('497305', '945', 'automação realizada', 'Concluir') \n
            
        '''
        url = f'{self.url_api}/processos/protocolar'
        headers = { "Content-Type": "application/json; charset=utf-8", "organization": self.organizacao, "Authorization": self.token_fluid }
        id_empresa_origem = 1
        id_empresa_destino = 1
        if empresa_orig != 1: id_empresa_origem = self.depara(id_empresa_origem)
        if empresa_dest != 1: id_empresa_destino = self.depara(id_empresa_destino)
        
        nodo, acao = self.get_nodo_possiveis_destinos(cod_processo, nome_do_nodo)
        if 'codigo de retorno' in str(nodo) or abertura_de_processo:
            id_arvore, nodo = self.nodo_e_arvore_para_novo_processo(id_tipo_processo)
            acao = 0
        
        obj_acao = {
            "acao": acao, # ação 0, protocolar normal com mensagem
            "processo": cod_processo,
            "destino": nodo, # nodo destino da arvore do processo, para onde vai qdo protocolar
            "parecer": mensagem, # mensagem para escrever no parecer ao protocolar
            "parecer_restrito": 0,
            "usuario": self.id_usuario, # id usuario fluid que esta realizando a operacao por api
            "empresa_origem": empresa_orig, # empresa 1
            "empresa_destino": empresa_dest, # usar zero para sede, e para agencia passar cod_fluid referente a agencia , fazer depara. 
            "usuario_destino": usuario_destino
            }

        response = requests.post(url, headers=headers, json=obj_acao)    
        cod_res_api = str(response.status_code)
        print('codigo de retorno da api fluid: ', cod_res_api) 
    
        if cod_res_api != '204':
            time.sleep(5)
            response = requests.post(url, headers=headers, json=obj_acao)
            cod_res_api = str(response.status_code)
            
        if (cod_res_api == '204'):
            print(response.text)
        else:
            print('codigo de retorno da api fluid: ', cod_res_api) 
            print(response.text)



class Whatsapp:

    def __init__(self):
        self.url_api_whats = os.getenv('url_api_whats') 
        self.token_api_whats = os.getenv('token_api_whatsapp')
        self.template_informa_novo = os.getenv('template_informa_novo')
        self.template_informa_com_img = os.getenv('template_informa_com_img')
        self.template_informa_com_pdf = os.getenv('template_informa_com_pdf')
        self.whats_user_origem = os.getenv('whats_user_origem')
        self.cod_coop = os.getenv('cod_coop')


    def verificar_opt_in(self, celular:str):   
        url = f'{self.url_api_whats}/optin/55{celular}'
        headers = {"Content-Type": "application/json; API Key","x-api-key": self.token_api_whats}
        response = requests.get(url, headers=headers)
        cod_response  = response.status_code
        return cod_response


    def enviar_texto_whatsapp(self, celular: str, sistema_envio: str, texto:str):    
        url = f'{self.url_api_whats}/notification'
        headers = {"Content-Type": "application/json; API Key", "x-api-key": self.token_api_whats}
        body = {
            "customerCoopCode": self.cod_coop,
            "customerBranchNum": "01",
            "customerPhoneNum": "55" + celular,
            "templateName": self.template_informa_novo,
            "templateParameters": {"INFORMA": texto},
            "originCompany": "coop_" + self.cod_coop,
            "originSystem": sistema_envio,
            "originUsername": self.whats_user_origem
        }
        response = requests.post(url, headers=headers, json=body)
        cod_response  = response.status_code
        return cod_response


    def enviar_texto_e_img_whatsapp(self, celular: str, texto: str,url_imagem:str, sistema_envio: str):    
        chave = self.token_api_whats
        url = f'{self.url_api_whats}/notification'
        headers = {"Content-Type": "application/json; API Key", "x-api-key": self.token_api_whats}
        body = {
            "customerCoopCode": self.cod_coop,
            "customerBranchNum": "01",
            "customerPhoneNum": "55" + celular,
            "templateName": self.template_informa_com_img,
            "templateParameters": {"INFORMA": texto, "headerImageUrl": url_imagem},
            "originCompany": "coop_" + self.cod_coop,
            "originSystem": sistema_envio,
            "originUsername": self.whats_user_origem
        }
        response = requests.post(url, headers=headers, json=body)
        cod_response  = response.status_code
        return cod_response



    def enviar_texto_e_pdf_whatsapp(self, celular: str, texto: str,url_pdf:str,nome_do_arquivo:str, sistema_envio: str):    
        url = f'{self.url_api_whats}/notification'
        headers = {"Content-Type": "application/json; API Key", "x-api-key": self.token_api_whats}
        body = {
            "customerCoopCode": self.cod_coop,
            "customerBranchNum": "01",
            "customerPhoneNum": "55" + celular,
            "templateName": self.template_informa_com_pdf,
            "templateParameters": {
                "INFORMA": texto,
                "headerDocumentUrl": url_pdf,
                "headerDocumentCaption": nome_do_arquivo
            },
            "originCompany": "coop_" + self.cod_coop,
            "originSystem": sistema_envio
        }
        response = requests.post(url, headers=headers, json=body)
        cod_response  = response.status_code
        return cod_response



class Sms:
    def __init__(self):
        self.url_api_sms = os.getenv('url_api_sms') 
        self.token_api_sms = os.getenv('token_api_sms')
        self.cod_coop = os.getenv('cod_coop')
        self.sms_from = os.getenv('sms_from')

    def enviar_SMS(self, celular: str, texto:str):    
        # nao utilize acentuacao na mensagem do sms, pois exige o valor de 2 mensagens.
        headers = {"Content-Type": "application/json; charset=utf-8", "X-API-TOKEN": self.token_api_sms}
        body = {
            "from": self.sms_from,
            "to": "55" + celular,
            "contents": [
                {"type": "text", "text": texto}   
                ]
            }
        response = requests.post(self.url_api_sms, headers=headers, json=body)
        cod_response  = response.status_code
        return cod_response
    
   
    
class Dados:

    def __init__(self):
        self.ip_planning = os.getenv('ip_planning')
        self.user_planning = os.getenv('user_planning')
        self.pw_bd_planning = urllib.parse.quote_plus(os.getenv('pw_bd_planning'))
        
        self.ip_grafana = os.getenv('ip_grafana')
        self.user_grafana = os.getenv('user_grafana')
        self.pw_bd_grafana = urllib.parse.quote_plus(os.getenv('pw_bd_grafana'))
        
        self.ip_sistema_senhas = os.getenv('ip_sistema_senhas')
        self.user_sistema_senhas = os.getenv('user_sistema_senhas')
        self.database_sistema_senhas = os.getenv('database_sistema_senhas')
        self.pw_bd_sistema_senhas = urllib.parse.quote_plus(os.getenv('pw_bd_sistema_senhas'))
        
        self.ip_denodo = os.getenv('ip_denodo')
        self.user_denodo = os.getenv('user_denodo')
        self.pw_denodo = urllib.parse.quote_plus(os.getenv('pw_denodo'))

        

    def criar_engine(self, db='planning'):
        '''
        retorna conexao com o banco de dados \n
        schema planinng: db = ('planning', 'fluid', 'cronos') \n
        schema sistema_senhas: db = 'sistema_senhas' \n
        schema grafana: db = 'grafana' \n
        schema denodo: db = ('ldw', 'seguros', 'cooperativa', 'auditoria_7000') \n
        '''
        if db=='planning' or db=='fluid' or db=='cronos':
            return create_engine(f'mysql+mysqlconnector://{self.user_planning}:{self.pw_bd_planning}@{self.ip_planning}/{db}', pool_recycle=3600)
        elif db=='ldw' or db=='seguros' or db=='cooperativa' or db=='auditoria_7000':
            return create_engine(f'denodo://{self.user_denodo}:{self.pw_denodo}@{self.ip_denodo}:9996/{db}')
        elif db == 'grafana':
            return create_engine(f'mysql+mysqlconnector://{self.user_grafana}:{self.pw_bd_grafana}@{self.ip_grafana}/{db}')
        elif db == 'sistema_senhas':
            db = self.database_sistema_senhas
            return create_engine(f'mysql+mysqlconnector://{self.user_sistema_senhas}:{self.pw_bd_sistema_senhas}@{self.ip_sistema_senhas}/{db}')
        else:
            #raise Exception('Ops, Nome do Banco de dados é desconhecido, db desconhecido')
            engine = create_engine(f'mysql+mysqlconnector://{self.user_sistema_senhas}:{self.pw_bd_sistema_senhas}@{self.ip_sistema_senhas}/{db}')
            
        


    def consultar_banco_dados(self, conexao_engine, query_sql:str):
        '''
        retorna um DataFrame pandas \n
        exemplo de query: \n
        SELECT * FROM rpa_historico WHERE cod_rpa = "3000" \n
        '''
        df = pd.read_sql(query_sql, conexao_engine)
        return df
    
    
    def select_banco_dados(self, conexao_engine, query_sql:str):
        '''
        retorna um DataFrame pandas \n
        exemplo de query: \n
        SELECT * FROM rpa_historico WHERE cod_rpa = "3000" \n
        '''
        df = pd.read_sql(query_sql, conexao_engine)
        return df

        
        
    def update_banco_dados(self, conexao_engine, query_sql):
        '''
        realizar update na tabela do banco de dados \n
        exemplo de query: \n
        "UPDATE rpa_fila SET nome_rpa = 'teste_01' WHERE id_fila = 9161" \n
        '''
        conexao_engine.execute(query_sql)
        
        
    def insert_banco_dados(self, conexao_engine, query_sql):
        '''
        realiza insert na tabela do banco de dados \n
        exemplo de query: \n
        "INSERT INTO rpa_fila(cod_rpa, nome_rpa, status) VALUES (6001, NULL, 'novo')" \n
        OBS. passar todas as colunas, exceto a primmeira caso seja auto-incremento
        '''
        conexao_engine.execute(query_sql)
                
        
    def incluir_tabela_planning(self, df,nome_da_tabela:str):
        engine = dados.criar_engine()
        df.to_sql(nome_da_tabela,engine,if_exists='append', index = False)
        print('Inserção realizada com sucesso')



class Acc:
    import pyautogui as p
    import subprocess
    import pyperclip
    
    def __init__(self):
        pass

    
    def open_acclient(self, siat_siac_sacg, transacional=True):
        # Open AC Client
        try:
            self.p.sleep(1)
            os.system('taskkill /F /FI "WindowTitle eq C:\\ProgramData\\ac\\teoff-exe*" /T')
        except Exception:
            pass
        
        try:
            os.system('taskkill /F /IM javaw_ac.exe')
            self.p.sleep(1)
        except Exception:
            pass
        
        user_acc = os.getenv('user_acc')
        pw_acclient = os.getenv('pw_acclient')
         
        self.subprocess.Popen("C:\\Users\\Public\\Desktop\\AC Client.lnk",shell=True)
        self.p.sleep(15)
        

        # pegar retangulo da janela pelo titulo parcial
        janela = self.p.getWindowsWithTitle('Aplicações Core - Login')[0]
        janela.activate()

        self.p.press('tab')
        self.p.press('tab')
        # digitar usuario
        self.p.typewrite(user_acc)
        self.p.press('tab')
        self.p.typewrite(pw_acclient)
        self.p.press('tab')
        self.p.press('enter')
        print('passou do login')

        self.p.sleep(12)
        # pegar retangulo da janela pelo titulo parcial
        janela = self.p.getWindowsWithTitle('AC Client')[0]
        janela.activate()
        janela.left
        self.p.sleep(1)
        self.p.press('pgdn')

        # Selecionar o MENU SIAT
        posicao = 0
        pasta_imagens = user_site_packages +  '\\rpa_coop\\img\\'
                   
        
        if 'SACG' in str(siat_siac_sacg).upper():
            try:
                posicao = self.p.locateOnScreen(pasta_imagens + 'sacg_branco.png')
            except:
                posicao = self.p.locateOnScreen(pasta_imagens + 'sacg_verde.png')
        elif 'SIAT' in str(siat_siac_sacg).upper():
            try:
                posicao = self.p.locateOnScreen(pasta_imagens + 'siat_branco.png')
            except:
                posicao = self.p.locateOnScreen(pasta_imagens + 'siat_verde.png')
        elif 'SIAC' in str(siat_siac_sacg).upper():
            try:
                posicao = self.p.locateOnScreen(pasta_imagens + 'siac_amarelo.png')
            except:
                posicao = self.p.locateOnScreen(pasta_imagens + 'siac_verde.png')
        time.sleep(1)
        self.p.click(posicao)
        print('selecionou o menu: siat, siac, sacg')
        time.sleep(3)
        
        if transacional:
            self.p.moveTo(janela.left + 48, janela.top + 165)
            time.sleep(1)
            self.p.doubleClick()
        else:
            self.p.moveTo(janela.left + 48, janela.top + 245)
            self.p.doubleClick()
        time.sleep(7)
        
           
    def select_menu_letras(self, letras):
        self.p.sleep(1)
        janela = self.p.getWindowsWithTitle('teoff-exe')[0]
        janela.activate()
        # Selecionar o Menu de opções
        self.p.sleep(1)
        if len(letras) == 2:
            self.p.typewrite(letras[0])
            self.p.sleep(1)
            self.p.typewrite(letras[1])
            self.p.sleep(1)
        elif len(letras) == 3:
            self.p.typewrite(letras[0])
            self.p.sleep(1)
            self.p.typewrite(letras[1])
            self.p.sleep(1)
            self.p.typewrite(letras[2])
            self.p.sleep(1)   
        elif len(letras) == 4:
            self.p.typewrite(letras[0])
            self.p.sleep(1)
            self.p.typewrite(letras[1])
            self.p.sleep(1)
            self.p.typewrite(letras[2])
            self.p.sleep(1)
            self.p.typewrite(letras[3])
            self.p.sleep(1)
        elif len(letras) == 5:
            self.p.typewrite(letras[0])
            self.p.sleep(1)
            self.p.typewrite(letras[1])
            self.p.sleep(1)
            self.p.typewrite(letras[2])
            self.p.sleep(1)
            self.p.typewrite(letras[3])
            self.p.sleep(1)
            self.p.typewrite(letras[4])
            self.p.sleep(1)
        elif len(letras) == 6:
            self.p.typewrite(letras[0])
            self.p.sleep(1)
            self.p.typewrite(letras[1])
            self.p.sleep(1)
            self.p.typewrite(letras[2])
            self.p.sleep(1)
            self.p.typewrite(letras[3])
            self.p.sleep(1)
            self.p.typewrite(letras[4])
            self.p.sleep(1)
            self.p.typewrite(letras[5])
            self.p.sleep(1)
        elif len(letras) == 7:
            self.p.typewrite(letras[0])
            self.p.sleep(1)
            self.p.typewrite(letras[1])
            self.p.sleep(1)
            self.p.typewrite(letras[2])
            self.p.sleep(1)
            self.p.typewrite(letras[3])
            self.p.sleep(1)
            self.p.typewrite(letras[4])
            self.p.sleep(1)
            self.p.typewrite(letras[5])
            self.p.sleep(1)
            self.p.typewrite(letras[6])
            self.p.sleep(1)
        else:
            print('ops funcao entende apenas 2, 3, 4, 5, 6 ou 7 letras')
            
                
    def get_text(self, ini_linha=22, fim_linha=632, topo1=407, topo2=407):
        time.sleep(1)
        janela = self.p.getWindowsWithTitle('teoff-exe')[0]
        time.sleep(1)
        janela.activate()
        self.p.moveTo(janela.left + ini_linha, janela.top + topo1)
        self.p.sleep(1)
        self.p.dragTo(janela.left + fim_linha, janela.top + topo2, 0.8, button='left')
        self.p.moveTo(janela.left + ini_linha, janela.top + topo2)
        self.p.rightClick()
        capturado = self.pyperclip.paste()
        print(f'texto capturado:{capturado}')
        return capturado            
            
            
    def exist_text(self, texto_esperado, max_tentativas=7, segundos_entre_tentativas=3, ini_linha=22, fim_linha=632, topo1=407, topo2=407, continua_seerro=False):
        time.sleep(1)
        self.pyperclip.copy('')
        tentativas = 0
        time.sleep(1)
        captura = self.get_text(ini_linha, fim_linha, topo1, topo2)
        resultado = True
        while not texto_esperado in captura and tentativas < max_tentativas:
            print('esperando texto: ', texto_esperado)
            self.p.sleep(segundos_entre_tentativas)
            captura = self.get_text(ini_linha, fim_linha, topo1, topo2)
            tentativas += 1
            if tentativas == max_tentativas:
                resultado = False
        print(resultado)
        if resultado == False and continua_seerro == False:
            raise Exception(f'Execução pausada. O texto: "{texto_esperado}" não foi localizado durante a execução do robô.')
        return resultado
 
       
       
            
            
            
            



