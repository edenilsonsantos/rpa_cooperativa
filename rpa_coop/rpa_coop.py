import os, requests, json, time, re
from datetime import date, datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
from urllib.request import urlretrieve
import urllib.parse
import site
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

user_site_packages = site.getusersitepackages()
user_site_packages = user_site_packages.replace('Roaming', 'Local\\Programs').replace('site-packages','Lib\\site-packages')


def gerador_pwd(palavra_chave:str, select_atributo='usuario', retorna_atributo=True, retorna_dicionario=False ,print_atributo=False, mostrar_todas_credenciais=False):
    '''
    usuario = gerador_pwd('fluid', 'usuario')\n
    print(usuario)\n
    '''
    import os
    import socket
    from cryptography.fernet import Fernet 
    import site
    user_site_packages = site.getusersitepackages()
    user_site_packages = user_site_packages.replace('Roaming', 'Local\\Programs').replace('site-packages','Lib\\site-packages')
    
    if retorna_dicionario: retorna_atributo = False
    
    db='fluid'
    ip_planning = str(os.getenv('ip_planning'))
    user_planning = str(os.getenv('user_planning'))
    pw_bd_planning = str(urllib.parse.quote_plus(os.getenv('pw_bd_planning')))     
    
    
    palavra_chave_ = str(palavra_chave).lower().strip() 
    p0 = os.getenv('userdomain')
    p1 = p0
    p2 = socket.gethostname()
    p3 = socket.gethostbyname(p2)
    p3 = p3[::-1]
    p3 = p3.replace('.','')[-6:]
    p1 = p1[0]
    if os.path.exists('c:\\temp\\'): p2 = p0[1:]
    p4 = str(socket.getfqdn()[-14:]).replace('.','')
    p5 = os.name
    p6 = ''
    
    for x in p4: p6 = p6 + str(ord(x))
    key = '2'+ ((p1 + p2)[::-1] * (2^3)) + (p3) + p4 + p6[:7] + p5 + ((p2[::-1])[:3]) + '__' + ((p2[::-1])[:3]).capitalize() + '='
    
    file = open(f'{user_site_packages}\\rpa_coop\\img\\hash', 'r')
    hash = file.read()
    file.close
    fernet = Fernet(key) 
    msg_encripted = hash
    msg = bytes(msg_encripted, "utf-8") 
    hash_validador = fernet.decrypt(msg).decode("utf-8")
    
    
    if mostrar_todas_credenciais:
        sql = f"SELECT * FROM rpa_cofre_senhas"
        conex = create_engine(f'mysql+mysqlconnector://{user_planning}:{pw_bd_planning}@{ip_planning}/{db}', pool_recycle=3600)
        credenciais = pd.read_sql_query(sql, conex)
        credenciais = credenciais[['usuario', 'palavra_chave', 'sistema', 'tipo']]
        print('\nPALAVRAS CHAVES EXISTENTES - PARA ACESSO AS CREDENCIAIS')
        print(credenciais[['palavra_chave', 'sistema']])
        return credenciais
    else:  
        sql = f'SELECT * FROM rpa_cofre_senhas WHERE palavra_chave like "%{palavra_chave_}%"'
        conex = create_engine(f'mysql+mysqlconnector://{user_planning}:{pw_bd_planning}@{ip_planning}/{db}', pool_recycle=3600)
        df = pd.read_sql_query(sql, conex)
        # print(df)
        credencial_atributos = {}
        df = df.drop(columns='id')
        valor = df.iloc[0,:].apply(str).values
        valor = str(valor[1])
        fernet = Fernet(hash_validador) 
        msg_encripted = valor
        msg = bytes(msg_encripted, "utf-8") 
        try:
            valor = fernet.decrypt(msg).decode("utf-8")
            df['senha'] = valor
        except:
            pass
        credencial_atributos = df.to_dict(orient='records')
        credenciais = credencial_atributos[0]
        valor = credenciais.get(select_atributo)
        result = f'{select_atributo} : {valor}'
        if print_atributo: print(result)
        if retorna_atributo: return valor
        return credenciais


class Adobe:
    def __init__(self):
        self.token_api_adobe = str(gerador_pwd('api_adobe', 'senha'))
        self.url_api_adobe = str(gerador_pwd('api_adobe', 'ip_host'))
        
        
    def alterar_status_usuario(self, email_usuario:str, status_usuario:str):
        '''status_usuario: ACTIVE, INACTIVE'''
        token_get_user = self.token_api_adobe
        url = f'{self.url_api_adobe}users'
        headers = { "Authorization": f"{token_get_user}"}
        response = requests.get(url, headers=headers)
        df = pd.DataFrame(response.json()['userInfoList'])
        for x in df.itertuples():
            if str(x.email) == str(email_usuario):
                id_usuario = str(x.id)
                break
            else:
                id_usuario = 'Não encontrado'

        if id_usuario == 'Não encontrado': raise Exception('Usuário não encontrado')
        url = f'{self.url_api_adobe}users/{id_usuario}/state'
        headers = { "Authorization": f"{token_get_user}"}
        body = {"state": f"{status_usuario}", "comment": "desativado por rpa"}
        response = requests.put(url, headers=headers, json=body)
        return response
        
                
class Dados:
    
    def __init__(self):
        self.ip_planning = str(os.getenv('ip_planning'))
        self.user_planning = str(os.getenv('user_planning'))
        self.pw_bd_planning = str(urllib.parse.quote_plus(os.getenv('pw_bd_planning'))) 
        
        self.user_planning_controles = str(gerador_pwd('user_planning_controles', 'senha'))
        self.pw_planning_controles = str(gerador_pwd('pw_planning_controles', 'senha'))
        
        self.ip_grafana = str(gerador_pwd('grafana', 'ip_host'))
        self.user_grafana = str(gerador_pwd('grafana', 'usuario'))
        self.pw_bd_grafana = str(urllib.parse.quote_plus(gerador_pwd('grafana', 'senha')))
        
        self.ip_sistema_senhas = str(gerador_pwd('sistema_senhas', 'ip_host'))
        self.user_sistema_senhas = str(gerador_pwd('sistema_senhas', 'usuario'))
        self.database_sistema_senhas = str(gerador_pwd('sistema_senhas', 'db_name'))
        self.pw_bd_sistema_senhas = str(urllib.parse.quote_plus(gerador_pwd('sistema_senhas', 'senha')))
        
        self.ip_denodo = str(gerador_pwd('denodo_web', 'ip_host'))
        self.user_denodo = str(gerador_pwd('denodo_web', 'usuario'))
        self.pw_denodo = str(urllib.parse.quote_plus(gerador_pwd('denodo_web', 'senha')))
        
        self.token_api_denodo = str(gerador_pwd('token_api_denodo', 'senha'))
        self.url_api_denodo = str(gerador_pwd('token_api_denodo', 'ip_host'))

        
    def criar_engine(self, db:str, user_db='user_opcional', password_db='senha_opcional', ip_ou_host_db='ip_host_opcional', porta='3306', library_sql='mysqlconnector'):
        '''
        retorna conexao com db, db='parametro_obrigatorio' \n
        schema planinng: db = ('planning', 'fluid', 'cronos', 'controles_internos') \n
        schema sistema_senhas: db = 'sistema_senhas' \n
        schema grafana: db = 'grafana' \n
        schema denodo: db = ('ldw', 'seguros', 'cooperativa', 'auditoria_7000') \n
        '''
        if (db == 'planning') or (db == 'fluid') or (db == 'cronos') or (db == 'controles_internos') or (db == 'bok_credito') or (db == 'pufv') or (db == 'boas_vindas'):
            if db == 'controles_internos':
                conexao = create_engine(f'mysql+mysqlconnector://{self.user_planning_controles}:{self.pw_planning_controles}@{self.ip_planning}/{db}', pool_recycle=3600)
            else:
                conexao = create_engine(f'mysql+mysqlconnector://{self.user_planning}:{self.pw_bd_planning}@{self.ip_planning}/{db}', pool_recycle=3600)
        elif (db == 'ldw') or (db == 'seguros') or (db == 'cooperativa') or (db == 'auditoria_7000'):
            conexao = create_engine(f'denodo://{self.user_denodo}:{self.pw_denodo}@{self.ip_denodo}:9996/{db}')
        elif (db == 'grafana'):
            conexao = create_engine(f'mysql+mysqlconnector://{self.user_grafana}:{self.pw_bd_grafana}@{self.ip_grafana}/{db}')
        elif (db == 'sistema_senhas'):
            banco = self.database_sistema_senhas
            conexao = create_engine(f'mysql+mysqlconnector://{self.user_sistema_senhas}:{self.pw_bd_sistema_senhas}@{self.ip_sistema_senhas}:3307/{banco}')
            # conexao = mysql.connect(host=self.ip_sistema_senhas, port=3307, database=banco, user=self.user_sistema_senhas, password=self.pw_bd_sistema_senhas)
        else:
            conexao = create_engine(f'mysql+{library_sql}://{user_db}:{password_db}@{ip_ou_host_db}:{porta}/{db}')
        return conexao
            
                         
    def criar_conexao(self, db:str, user_db='user_opcional', password_db='senha_opcional', ip_ou_host_db='ip_host_opcional', porta='3306', library_sql='mysqlconnector'):
        '''
        retorna conexao com db, db='parametro_obrigatorio' \n
        schema planinng: db = ('planning', 'fluid', 'cronos', 'controles_internos') \n
        schema sistema_senhas: db = 'sistema_senhas' \n
        schema grafana: db = 'grafana' \n
        schema denodo: db = ('ldw', 'seguros', 'cooperativa', 'auditoria_7000') \n
        '''
        if (db == 'planning') or (db == 'fluid') or (db == 'cronos') or (db == 'controles_internos') or (db == 'bok_credito') or (db == 'pufv') or (db == 'boas_vindas'):
            if db == 'controles_internos':
                conexao = create_engine(f'mysql+mysqlconnector://{self.user_planning_controles}:{self.pw_planning_controles}@{self.ip_planning}/{db}', pool_recycle=3600)
            else:
                conexao = create_engine(f'mysql+mysqlconnector://{self.user_planning}:{self.pw_bd_planning}@{self.ip_planning}/{db}', pool_recycle=3600)
        elif (db == 'ldw') or (db == 'seguros') or (db == 'cooperativa') or (db == 'auditoria_7000'):
            conexao = create_engine(f'denodo://{self.user_denodo}:{self.pw_denodo}@{self.ip_denodo}:9996/{db}')
        elif (db == 'grafana'):
            conexao = create_engine(f'mysql+mysqlconnector://{self.user_grafana}:{self.pw_bd_grafana}@{self.ip_grafana}/{db}')
        elif (db == 'sistema_senhas'):
            banco = self.database_sistema_senhas
            conexao = create_engine(f'mysql+mysqlconnector://{self.user_sistema_senhas}:{self.pw_bd_sistema_senhas}@{self.ip_sistema_senhas}:3307/{banco}')
            # conexao = mysql.connect(host=self.ip_sistema_senhas, port=3307, database=banco, user=self.user_sistema_senhas, password=self.pw_bd_sistema_senhas)
        else:
            conexao = create_engine(f'mysql+{library_sql}://{user_db}:{password_db}@{ip_ou_host_db}:{porta}/{db}')
        return conexao
            
        
    def api_consulta_denodo(self, database:str, tabela:str, colunas:str, filtro_where="opcional"):
        '''
        filtro = "coluna2 eq 'SIM' and coluna3 eq 'Ativo'" \n
        df = dados.api_consulta_denodo('ldw', 'nome_da_tabela', 'coluna1, coluna5', filtro) \n\n
        
        # operadores para filtro where: \n
        eq = igual \n
        lt = menor que \n
        le = menor ou igual \n
        ne = diferente \n
        ge = maior ou igual \n
        gt = maior que \n       
        
        '''
        df = pd.DataFrame()
        requests.packages.urllib3.disable_warnings()
        if filtro_where == "opcional":
            url = f"{self.url_api_denodo}/{database}/views/{tabela}?$select={colunas}"
        else:
            url = f"{self.url_api_denodo}/{database}/views/{tabela}?$select={colunas}&$filter={filtro_where}"
        payload={}
        headers = {'Accept': 'application/xhtml+xml;q=0.9,application/json', 'Authorization': self.token_api_denodo}
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        # print(response.text.encode('utf8'))
        rows = json.loads(response.content)
        try:
            df = pd.DataFrame(rows['elements'])
        except:
            print('erro ao converter para DataFrame, json retornou: \n', response.text.encode('utf8'))
        return df   
        
     
    def consultar_banco_dados(self, conexao_engine, query_sql:str, retorna_DataFrame=True):
        '''
        retorna um DataFrame pandas \n
        exemplo de query: \n
        SELECT * FROM rpa_historico WHERE cod_rpa = "3000" \n
        '''
        if retorna_DataFrame:
            df_rows = pd.read_sql_query(query_sql, conexao_engine)
        else:
            df_rows = conexao_engine.execute(query_sql)
        return df_rows
    
    
    def select_banco_dados(self, conexao_engine, query_sql:str, retorna_DataFrame=True):
        '''
        retorna um DataFrame pandas \n
        exemplo de query: \n
        SELECT * FROM rpa_historico WHERE cod_rpa = "3000" \n
        '''
        if retorna_DataFrame:
            df_rows = pd.read_sql_query(query_sql, conexao_engine)
        else:
            df_rows = conexao_engine.execute(query_sql)
        return df_rows

           
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
                
        
    def insert_DataFrame_to_db(self, df, engine, nome_da_tabela:str, if_existir='append', mostrar_index=False):
        df.to_sql(nome_da_tabela, engine, if_exists=if_existir, index = mostrar_index)
        print('Inserção realizada com sucesso')


    def delete_linhas_banco_dados(self, conexao_engine, query_sql):
        '''
        realiza delete na tabela do banco de dados \n
        exemplo de query: \n
        "DELETE FROM rpa_fila WHERE id_fila = 9161" \n
        '''
        aux_query = str(query_sql).upper()
        if 'WHERE' in aux_query:
            conexao_engine.execute(query_sql)
            print('Exclusão realizada com sucesso')
        else:
            print('Não foi possível realizar a exclusão, é necessário informar o WHERE na query')
            

class Fluid:
    
    def __init__(self):
        
        self.id_usuario = str(gerador_pwd('fluid_cod_user', 'senha'))
        self.token_fluid = str(gerador_pwd('token_api_fluid', 'senha'))
        self.organizacao = str(gerador_pwd('fluid_organizacao', 'senha'))
        self.headers = {'organization': self.organizacao,'authorization': self.token_fluid}
        self.url_api = str(gerador_pwd('fluid_url_api', 'senha'))
        self.url_request = str(gerador_pwd('fluid_url_request', 'senha'))
        self.user_fluid = str(gerador_pwd('fluid_user_web', 'senha'))
        self.senha_fluid = str(gerador_pwd('usuario_fluid', 'senha'))
        
        self.ip_planning = str(os.getenv('ip_planning'))
        self.user_planning = str(os.getenv('user_planning'))
        self.pw_bd_planning = str(urllib.parse.quote_plus(os.getenv('pw_bd_planning'))) 
        
        
        
        
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
        if cod_res_api != '200':
            raise Exception(f'Erro ao preparar anexo fluid, processo: {cod_processo}')
        
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

        # observacao, os time.sleep(10) sao uma segurança para não protocolar antes de terminar o upload e corromper o arquivo.
        # caso o arquivo seja muito grande pode ir testando com uma espera maior, ou fazer um if de espera por tamanho de arquivo.
        time.sleep(10)
        if cod_res_api != '204':
            raise Exception(f'Erro ao anexar arquivo no fluid, processo: {cod_processo}')
        else:
            print(f'Arquivos anexados com sucesso no processo: {cod_processo}')
            return cod_res_api
        
        
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
            if '\\' in pasta_destino[-1]:   
                os.system(f'mkdir {pasta_destino}anexos_processo_{num_processo}')
                destino = f'{pasta_destino}anexos_processo_{num_processo}'   
            else:    
                os.system(f'mkdir {pasta_destino}\\anexos_processo_{num_processo}')  
                destino = f'{pasta_destino}\\anexos_processo_{num_processo}\\'
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
        print('cancelado processo {num_processo_fluid}')
    
    
    def depara(self, ua):
        '''
            passamos como parâmetro o cod_agencia\n
            a função retorma o cod_agencia_fluid, codigo cadastrado no fluid
        '''      
        # self.ip_planning = str(os.getenv('ip_planning'))
        # self.user_planning = str(os.getenv('user_planning'))
        # self.pw_bd_planning = str(urllib.parse.quote_plus(os.getenv('pw_bd_planning'))) 
        ua =  str(ua).upper()
        db = 'fluid'
        engine = create_engine(f'mysql+mysqlconnector://{self.user_planning}:{self.pw_bd_planning}@{self.ip_planning}/{db}', pool_recycle=3600)
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
        time.sleep(1)
        url_cod_tipo_processo = f'{self.url_request}/cadastro/workflow/versoes/id/{id_tipo_processo}'
        page = minha_Session.get(url_cod_tipo_processo)
        time.sleep(1)
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
            # print('processo identificado como novo') 
            # print()
            return msg, acao 
        
    
    def criar_processo_rascunho(self, id_tipo_processo:str, id_empresa_origem=1, id_empresa_destino=1, id_usuario=0, responsavel_destino=0, arvore=0):
        '''
            id_processo, nodo_inicial = post_criar_processo(id_tipo_processo)\n
            ou\n
            id_processo, nodo_inicial = post_criar_processo(id_tipo_processo, id_empresa_origem=cod_agencia, id_empresa_destino=cod_agencia)
        '''
        url_final = f'{self.url_api}/processos/novo'
        headers = {"Content-Type": "application/json; charset=utf-8", "organization": self.organizacao, "Authorization": self.token_fluid }
        
        if id_empresa_origem != 1: id_empresa_origem = self.depara(id_empresa_origem)
        if id_empresa_destino != 1: id_empresa_destino = self.depara(id_empresa_destino)
        if id_usuario == 0: id_usuario = self.id_usuario
        if responsavel_destino == 0: responsavel_destino = self.id_usuario
        
        time.sleep(1)
        id_versao_arvore = 0
        if arvore == 0:
            id_versao_arvore, nodo_inicial = self.nodo_e_arvore_para_novo_processo(str(id_tipo_processo)) # pega a arvore vigente, ou em criação
        else:
            id_versao_arvore = arvore
        tempo_minutos = self.get_sla(id_tipo_processo)
        
        obj_acao = {
            "tipo_processo": id_tipo_processo, # id do tipo de processo fluid
            "tempo": tempo_minutos, # tempo em minutos
            "responsavel_criacao": id_usuario, # id do usuário fluid
            "responsavel_origem": id_usuario, # id do usuário fluid
            "responsavel_destino": responsavel_destino,
            "empresa_origem": id_empresa_origem, 
            "empresa_destino": id_empresa_destino,
            "versao_processo": id_versao_arvore # versao da arvore do processo, abra a arvore e veja no final da url o id
            }
        
        # no Método POST passar os parametros {url, headers, json}
        response = requests.post(url_final, headers=headers, json=obj_acao)
        cod_res_api = str(response.status_code) 
        
        if cod_res_api == '200':
            res_dict = response.json()
            id_processo = int(res_dict['id'])
            print(f'Processo fluid {id_processo} criado com sucesso')
            return id_processo
        else:   
            raise Exception(f'Erro ao criar processo novo no fluid: {response.text}')
 

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
        
        
    def get_dados_processo(self, cod_processo, return_response=False, imprimir_json=False, gerar_arquivo_temp=False):
        '''
            retorna valores de campo comuns e campos tabela, existentes no processo fluid\n
            retorna no formato de um dataframe do pandas
        '''
        df1 = pd.DataFrame()
        url = f'{self.url_api}/processos/visualizar/{cod_processo}/{self.id_usuario}'
        headers = { "Content-Type": "application/json; charset=utf-8", "organization": self.organizacao, "Authorization": self.token_fluid }
        response = requests.get(url, headers=headers)
        
        if imprimir_json:
            print(response.text)
        if gerar_arquivo_temp:
            file = open(f'c:\\temp\\dados_processo_{cod_processo}.json', 'w')
            file.write(response.text)
            file.close()
        cod_res_api = str(response.status_code)
        if cod_res_api != '200':
            time.sleep(5)
            response = requests.get(url, headers=headers)
            cod_res_api = str(response.status_code)
            
        if return_response: return response
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


    def get_processos_fluid(self, array_cod_tipo_processos=[0], id_local_de_processo=542, return_response=False):  
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
    
        if return_response: return response
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
    
    
    def gravar_dados_campos_tabela(self, cod_processo:int, id_tipo_processo:int, id_tabela:int, id_campos_tabela:list, campo_e_valor:list, id_nodo=0, abertura_de_processo=False):
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
        time.sleep(1)
        
        if id_nodo == 0:
            nodo, acao = self.get_nodo_possiveis_destinos(cod_processo)
            if 'codigo de retorno' in str(nodo) or abertura_de_processo:
                id_arvore, nodo = self.nodo_e_arvore_para_novo_processo(id_tipo_processo)
                acao = 0
        else:
            nodo = id_nodo
            
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
        if res.status_code != 204:
            raise Exception(f'Erro ao gravar dados no processo {cod_processo}: {res.text}')
        else:
            print(f'Dados gravados com sucesso no processo fluid {cod_processo}')
            return res.status_code
    
    
    def gravar_dados_campos_comuns(self, cod_processo:str, id_tipo_processo:str, dict_campos:dict, abertura_de_processo=False, id_nodo=0):
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
        time.sleep(1)
        if id_nodo == 0:
            nodo, acao = self.get_nodo_possiveis_destinos(cod_processo)

            if 'codigo de retorno' in str(nodo) or abertura_de_processo:
                id_arvore, nodo = self.nodo_e_arvore_para_novo_processo(id_tipo_processo)
                acao = 0
        else:
            nodo = id_nodo
        
        url = f'{self.url_api}/processos/salvar-campos'
        
        headers = {"organization": self.organizacao, "Authorization": self.token_fluid }
        param = { "processo": cod_processo, "destino": nodo, "usuario": self.id_usuario, "campos": dict_campos }

        res = requests.post(url, headers=headers, json=param)
   
        if res.status_code != 204:
            raise Exception(f'Erro ao gravar dados no processo {cod_processo}: {res.text}')
        else:
            print(f'Dados gravados com sucesso no processo fluid {cod_processo}')
            return res.status_code
    
    
    def protocolar_processo_fluid(self, cod_processo: str, id_tipo_processo: str,  mensagem: str, id_empresa_origem='1', id_empresa_destino='1', nome_do_nodo ='selecionado_proximo_nodo', abertura_de_processo= False, cod_nodo=0, cod_acao = 0, id_usuario=0, usuario_destino=0):
        ''' 
            post_protocolar_processo_fluid(processo, id_tipo_processo, msg, nome_nodo_destino, empresa_orig, empresa_dest) \n
            post_protocolar_processo_fluid('497305', '945', 'automação realizada') \n
            post_protocolar_processo_fluid('497305', '945', 'automação realizada', empresa_orig=68, empresa_dest=68) \n
            post_protocolar_processo_fluid('497305', '945', 'automação realizada', 'Devolver') \n
            post_protocolar_processo_fluid('497305', '945', 'automação realizada', 'Concluir') \n
            
        '''
        
        if id_usuario == 0: id_usuario = self.id_usuario
        if usuario_destino == 0: usuario_destino = self.id_usuario
        
        url = f'{self.url_api}/processos/protocolar'
        headers = { "Content-Type": "application/json; charset=utf-8", "organization": self.organizacao, "Authorization": self.token_fluid }
        if id_empresa_origem  != 1: id_empresa_origem = self.depara(id_empresa_origem)
        if id_empresa_destino != 1: id_empresa_destino = self.depara(id_empresa_destino)
        
        if cod_nodo == 0:
            nodo, acao = self.get_nodo_possiveis_destinos(cod_processo, nome_do_nodo)
            if 'codigo de retorno' in str(nodo) or abertura_de_processo:
                id_arvore, nodo = self.nodo_e_arvore_para_novo_processo(id_tipo_processo)
                acao = 0
        else:
            nodo = cod_nodo
            acao = cod_acao
        
        obj_acao = {
            "acao": acao, # ação 0, protocolar normal com mensagem
            "processo": cod_processo,
            "destino": nodo, # nodo destino da arvore do processo, para onde vai qdo protocolar
            "parecer": mensagem, # mensagem para escrever no parecer ao protocolar
            "parecer_restrito": 0,
            "usuario": id_usuario, # id usuario fluid que esta realizando a operacao por api
            "empresa_origem": id_empresa_origem, # empresa 1
            "empresa_destino": id_empresa_destino, # usar zero para sede, e para agencia passar cod_fluid referente a agencia , fazer depara. 
            "usuario_destino": usuario_destino
            }

        response = requests.post(url, headers=headers, json=obj_acao)    
        cod_res_api = str(response.status_code)
 
    
        if cod_res_api != '204':
            time.sleep(5)
            response = requests.post(url, headers=headers, json=obj_acao)
            cod_res_api = str(response.status_code)
            
        if (cod_res_api == '204'):
            print(f'processo fluid {cod_processo} protocolado com sucesso')
            return cod_res_api
        else:
            raise Exception(f'Erro ao protocolar processo {cod_processo}: {response.text}')


    def tomar_posse(self, cod_processo:str, empresa=1, id_usuario=0):
        time.sleep(1)        
        url = f'{self.url_api}/processos/tomar-posse'
        if id_usuario == 0: id_usuario = self.id_usuario
        
        headers = {"organization": self.organizacao, "Authorization": self.token_fluid }
        param = {"usuario": id_usuario, "empresa": empresa, "processo": cod_processo}
        res = requests.post(url, headers=headers, json=param)

        if res.status_code != 204: raise Exception(f'Erro ao gravar dados no processo {cod_processo}, {res.text}')
        print(f'Ok, tomou posse do processo: {cod_processo}')
        return res.status_code


class Whatsapp:
 
    def __init__(self):
        self.url_api_whats = str(gerador_pwd('url_api_whats', 'sistema'))
        self.token_api_whats = str(gerador_pwd('url_api_whats', 'senha'))
        self.template_informa_novo = str(gerador_pwd('template_informa_novo', 'sistema'))
        self.template_informa_com_img = str(gerador_pwd('template_informa_com_img', 'senha'))
        self.template_informa_com_pdf = str(gerador_pwd('template_informa_com_pdf', 'senha'))
        self.whats_user_origem = str(gerador_pwd('whats_user_origem', 'senha'))
        self.cod_coop = str(gerador_pwd('cod_coop', 'senha'))


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
        self.url_api_sms = str(gerador_pwd('url_api_sms', 'sistema'))
        self.token_api_sms = str(gerador_pwd('url_api_sms', 'senha'))
        self.cod_coop = str(gerador_pwd('cod_coop', 'senha'))
        self.sms_from = str(gerador_pwd('sms_from', 'senha'))

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
    
    
class Emails:
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    
    def __init__(self):
        self.user_mail = gerador_pwd('api_email', 'usuario')
        self.password_mail = gerador_pwd('api_email', 'sistema')
        self.smtpsrv = gerador_pwd('api_email', 'ip_host')


    def enviar_email(self, destinatarios, assunto: str, mensagem='', anexo=None, html_text_img=None, cc=None, cco=None):
        '''
        mail.enviar_email('usuario@dominio.com.br', 'titulo aqui', 'msg aqui') \n\n
        
        lista_dest = ['usuario@dominio.com.br','appuser@dominio.com.br']\n
        mail.enviar_email(lista_dest, 'titulo aqui', 'msg aqui')\n\n
        
        anexos = ['notas.txt', 'README.md']\n
        mail.enviar_email('usuario@dominio.com.br', 'titulo aqui', 'msg aqui', anexos)\n\n
        
        anexos = ['notas.txt', 'README.md', 'imagem.PNG']\n
        html_text_img = '<html><body><h1>msg aqui</h1><img src="cid:imagem_aqui.PNG"></body></html>'\n
        mail.enviar_email('usuario@dominio.com.br', 'titulo aqui', anexos, html_text_img)\n
        '''
        import pathlib
        mail_content = mensagem
        smtpserver = self.smtplib.SMTP(self.smtpsrv,587)
        msg = self.MIMEMultipart('mixed')
        msg = self.MIMEMultipart('alternative')
        if cco: 
            msg['Bcc'] = cco if type(cco) == str else ", ".join(cco)
        if cc: 
            msg['Cc'] = cc if type(cc) == str else ", ".join(cc)
            
        msg['Subject'] = assunto
        msg['From'] = self.user_mail 
        msg['To'] = destinatarios if type(destinatarios) == str else ", ".join(destinatarios)

        
        if html_text_img:
            msg.attach(self.MIMEText(mail_content + html_text_img, 'html', 'utf-8'))
        else:
            msg.attach(self.MIMEText(mail_content,'plain','utf8'))      
        
        if anexo:
            if type(anexo) == str:
                if anexo:
                    attachmentPath = anexo
                    name_file = pathlib.Path(attachmentPath).name
                    try:
                        with open(attachmentPath, "rb") as attachment:
                            p = self.MIMEApplication(attachment.read(),_subtype="png")	
                            p.add_header('Content-Disposition', "attachment; filename= %s" % name_file) 
                            msg.attach(p)
                    except Exception as e:
                        print(str(e))
            elif type(anexo) == list:
                for attachmentPath in anexo:
                    name_file = pathlib.Path(attachmentPath).name
                    try:
                        with open(attachmentPath, "rb") as attachment:
                            p = self.MIMEApplication(attachment.read(),_subtype="png")	
                            p.add_header('Content-Disposition', "attachment; filename= %s" % name_file) 
                            msg.attach(p)
                    except Exception as e:
                        print(str(e))
            
        #Send the Email Message
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(self.user_mail , self.password_mail)

        todos_destinos = []
        if destinatarios and cc and cco:
            if isinstance(destinatarios, list): todos_destinos.extend(destinatarios)
            if isinstance(destinatarios, str): todos_destinos.append(destinatarios)
            if isinstance(cc, list): todos_destinos.extend(cc)
            if isinstance(cc, str): todos_destinos.append(cc)
            if isinstance(cco, list): todos_destinos.extend(cco)
            if isinstance(cco, str): todos_destinos.append(cco) 
            smtpserver.send_message (msg, from_addr=self.user_mail, to_addrs=todos_destinos)
        elif destinatarios and cc:
            if isinstance(destinatarios, list): todos_destinos.extend(destinatarios)
            if isinstance(destinatarios, str): todos_destinos.append(destinatarios)
            if isinstance(cc, list): todos_destinos.extend(cc)
            if isinstance(cc, str): todos_destinos.append(cc)
            smtpserver.send_message (msg, from_addr=self.user_mail, to_addrs=todos_destinos)
        elif destinatarios and cco:
            if isinstance(destinatarios, list): todos_destinos.extend(destinatarios)
            if isinstance(destinatarios, str): todos_destinos.append(destinatarios)
            if isinstance(cco, list): todos_destinos.extend(cco)
            if isinstance(cco, str): todos_destinos.append(cco) 
            smtpserver.send_message (msg, from_addr=self.user_mail, to_addrs=todos_destinos)
        else:
            if isinstance(destinatarios, list): todos_destinos.extend(destinatarios)
            if isinstance(destinatarios, str): todos_destinos.append(destinatarios)
            smtpserver.send_message (msg, from_addr=self.user_mail, to_addrs=todos_destinos)        
        smtpserver.close()
        
                                        
class Acc:
    import pyautogui as p
    import subprocess
    import pyperclip
    
    
    def __init__(self):
        self.usuario_acc = str(gerador_pwd('acc', 'usuario'))
        self.senha_acc = str(gerador_pwd('acc', 'senha'))
        self.janela_sacg = 'janela'
        self.janela_siat = 'janela'
        self.janela_siac = 'janela'

    
    def open_acclient_old(self, siat_siac_sacg, transacional=True):
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
        
        user_acc = self.usuario_acc
        pw_acclient = self.senha_acc
         
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
                posicao = self.p.locateOnScreen(pasta_imagens + 'sacg_branco.png', confidence=0.9, grayscale=True)
            except:
                posicao = self.p.locateOnScreen(pasta_imagens + 'sacg_verde.png', confidence=0.9, grayscale=True)
        elif 'SIAT' in str(siat_siac_sacg).upper():
            try:
                posicao = self.p.locateOnScreen(pasta_imagens + 'siat_amarelo.png', confidence=0.9, grayscale=True)
            except:
                posicao = self.p.locateOnScreen(pasta_imagens + 'siat_branco.png', confidence=0.9, grayscale=True)
        elif 'SIAC' in str(siat_siac_sacg).upper():
            try:
                posicao = self.p.locateOnScreen(pasta_imagens + 'siac_branco.png', confidence=0.9, grayscale=True)
            except:
                posicao = self.p.locateOnScreen(pasta_imagens + 'siac_amarelo.png', confidence=0.9, grayscale=True)
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
        
           
    def open_acclient(self, siat_siac_sacg: str | list, transacional=True):
        ''' acc.open_acclient('siac') \n
         acc.open_acclient(['siat', 'sacg'])'''
        opcoes = []
        if isinstance(siat_siac_sacg, str):
            opcoes.append(siat_siac_sacg)
        else:
            opcoes = siat_siac_sacg
            
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
        
        user_acc = self.usuario_acc
        pw_acclient = self.senha_acc
         
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
        
                   
        
        if transacional:
            self.p.moveTo(janela.left + 48, janela.top + 165)
            time.sleep(1)
            self.p.click()
            # self.p.doubleClick()
        else:
            self.p.moveTo(janela.left + 48, janela.top + 245)
            self.p.click()
            # self.p.doubleClick()
        time.sleep(3)
            
   

        num_menu = 0
        self.janela_sacg = janela
        self.janela_siat = janela
        self.janela_siac = janela
        
        opcoes = [x.upper() for x in opcoes]
        
        for menu in opcoes:
            if menu == 'SACG':
                # Abrir SACG
                try:
                    posicao = self.p.locateOnScreen(pasta_imagens + 'sacg_branco.png', confidence=0.9, grayscale=True)
                except:
                    posicao = self.p.locateOnScreen(pasta_imagens + 'sacg_verde.png', confidence=0.9, grayscale=True)
                self.p.doubleClick(posicao)
                time.sleep(7)
                self.janela_sacg = self.p.getWindowsWithTitle('teoff-exe')[num_menu]
                print('clicou no menu: sacg')
                janela.activate()
            elif menu == 'SIAT':
                # Abrir SIAT
                try:
                    posicao = self.p.locateOnScreen(pasta_imagens + 'siat_amarelo.png', confidence=0.9, grayscale=True)
                except:
                    posicao = self.p.locateOnScreen(pasta_imagens + 'siat_branco.png', confidence=0.9, grayscale=True)
                self.p.doubleClick(posicao)
                time.sleep(7)
                self.janela_siat = self.p.getWindowsWithTitle('teoff-exe')[num_menu] 
                print('clicou no menu: siat')
                janela.activate()
            elif menu == 'SIAC':
                try:
                    posicao = self.p.locateOnScreen(pasta_imagens + 'siac_branco.png', confidence=0.9, grayscale=True)
                except:
                    posicao = self.p.locateOnScreen(pasta_imagens + 'siac_amarelo.png', confidence=0.9, grayscale=True)
                self.p.doubleClick(posicao)
                time.sleep(7)
                self.janela_siac = self.p.getWindowsWithTitle('teoff-exe')[num_menu]
                print('clicou no menu: siac')
                janela.activate()
            time.sleep(1)
        return self.janela_sacg, self.janela_siat, self.janela_siac

             
    def select_menu_letras(self, letras, nome_janela=None):
        '''acc.select_menu_letras(letras) \n
         acc.select_menu_letras(letras, nome_janela='sacg')'''
        self.p.sleep(1)
        nome_janela = str(nome_janela).upper()
        if nome_janela == 'SIAT':
            janela = self.janela_siat
        elif nome_janela == 'SIAC':
            janela = self.janela_siac
        elif nome_janela == 'SACG':
            janela = self.janela_sacg
        else:
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
            
                  
    def get_text(self, ini_linha=22, fim_linha=632, topo1=410, topo2=415, nome_janela=None):
        ''' acc.get_text('Retorna ao Sistema')\n
         acc.get_text('Retorna ao Sistema', nome_janela = 'sacg')'''
        time.sleep(1)
        nome_janela = str(nome_janela).upper()
        if nome_janela == 'SIAT':
            janela = self.janela_siat
        elif nome_janela == 'SIAC':
            janela = self.janela_siac
        elif nome_janela == 'SACG':
            janela = self.janela_sacg
        else:
            janela = self.p.getWindowsWithTitle('teoff-exe')[0]
  
        time.sleep(1)
        janela.activate()
        self.p.moveTo(janela.left + ini_linha, janela.top + topo1)
        self.p.sleep(1)
        self.p.dragTo(janela.left + fim_linha, janela.top + topo2, 1.5, button='left')
        self.p.moveTo(janela.left + ini_linha, janela.top + topo2)
        self.p.rightClick()
        capturado = self.pyperclip.paste()
        print(f'texto capturado:{capturado}')
        return capturado            
            
            
    def exist_text(self, texto_esperado, max_tentativas=7, segundos_entre_tentativas=3, ini_linha=22, fim_linha=632, topo1=412, topo2=412, continua_seerro=False, nome_janela=None):
        ''' acc.exist_text('Retorna ao Sistema')\n
         acc.exist_text('Retorna ao Sistema', nome_janela = 'sacg')'''
        time.sleep(1)
        self.pyperclip.copy('')
        tentativas = 0
        time.sleep(1)
        captura = self.get_text(ini_linha, fim_linha, topo1, topo2, nome_janela = nome_janela)
        resultado = True
        while not texto_esperado in captura and tentativas < max_tentativas:
            print('esperando texto: ', texto_esperado)
            self.p.sleep(segundos_entre_tentativas)
            captura = self.get_text(ini_linha, fim_linha, topo1, topo2, nome_janela = nome_janela)
            tentativas += 1
            if tentativas == max_tentativas:
                resultado = False
        print(resultado)
        if resultado == False and continua_seerro == False:
            raise Exception(f'Execução pausada. O texto: "{texto_esperado}" não foi localizado durante a execução do robô.')
        return resultado
 
         
class Monitorar:
        
    import socket
    import paramiko
    from dateutil.relativedelta import relativedelta
         
    def __init__(self):
        self.dados = Dados()
        self.data_ini = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') + ' 17:30:00'
        self.data_fim = datetime.now().strftime('%Y-%m-%d') + ' 17:30:00'
        self.usuario = str(gerador_pwd('user_monitora_vm', 'senha'))
        self.pwd = str(gerador_pwd('pw_monitora_vm', 'senha'))
        self.linux_host = str(gerador_pwd('vm_linux_host', 'senha'))
        self.linux_ip = str(gerador_pwd('vm_linux_host', 'ip_host'))
        self.linux_user = str(gerador_pwd('vm_linux_user', 'senha'))
        self.linux_pwd = str(gerador_pwd('vm_linux_pw', 'senha'))
        self.conexao = self.dados.criar_engine('cronos')
        
     
            
    def check_vms_running(self, ignorar_vms:list = ['NOTE0012035', 'DESKTOP-J63']):
        hoje_a_noite = datetime.now().strftime('%Y-%m-%d') + ' 18'
        hora_cheia = int(datetime.now().strftime('07'))
        df = self.dados.consultar_banco_dados(self.conexao, f"SELECT * FROM vms_rpa WHERE ativar_monitoramento = 'S' and ativo = 'S' ")
        df = df['vm_host']
        vms = df.to_list()
        dic_vms = {}

        for vm in vms: 
            if vm in ignorar_vms: continue
            
            ### Consulta na fila se teve agendamento de rpa para hoje no intervalo das 18 Horas
            if self.linux_host in vm and 8 >= hora_cheia <= 17:
                try:
                    df = self.dados.consultar_banco_dados(self.conexao, f"SELECT * FROM rpa_fila WHERE data_agendamento like '%{hoje_a_noite}%' ")
                    qtd_agendados_para_hj_noite = len(df)
                    if qtd_agendados_para_hj_noite > 0:
                        print('ok - agendador_python_new.py executou hoje de manhã')
                        status_vm = 'ok'
                        self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET vm_status = '{status_vm}' WHERE vm_host = '{vm}'")
                        self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET agendador_python = 'S' WHERE vm_host = '{vm}'")
                    else:
                        print('Erro, agendador_python_new.py nao foi executado hoje')
                        status_vm = 'erro'
                        self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET vm_status = '{status_vm}' WHERE vm_host = '{vm}'")
                        self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET agendador_python = 'N' WHERE vm_host = '{vm}'")   
                except:
                    pass    
                
            #### Consulta a VM Linux que contem os scripts agendadores de RPA 
            if self.linux_host in vm: 
                try:
                    ip_linux = self.linux_ip
                    ssh = self.paramiko.SSHClient()
                    username= self.linux_user
                    password= self.linux_pwd
                    ssh.set_missing_host_key_policy(self.paramiko.AutoAddPolicy)
                    ssh.connect(hostname=ip_linux, username=username, password=password)
                    stdin, stdout, stderr = ssh.exec_command('ps aux | grep agendador_fluid_new')
                    retorno_ssh = str(stdout.readline())
                    if 'agendador_fluid_new.py' in retorno_ssh:
                        print('ok - agendador_fluid_new, esta em execucao')
                        status_vm = 'ok'
                        self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET vm_status = '{status_vm}' WHERE vm_host = '{vm}'")
                        self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET agendador_fluid = 'S' WHERE vm_host = '{vm}'")
                    else:
                        print('erro na vm do linux')
                        status_vm = 'erro'
                        self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET vm_status = '{status_vm}' WHERE vm_host = '{vm}'")
                        self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET agendador_fluid = 'N' WHERE vm_host = '{vm}'")
                    ssh.close()
                except:
                    print('nao conseguiu conectar na vm linux para consultar os processos python')
                    status_vm = 'erro'
                    self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET vm_status = '{status_vm}' WHERE vm_host = '{vm}'")
                    self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET agendador_fluid = 'N' WHERE vm_host = '{vm}'")
                continue
            
            
            ### Consulta as VMs que possuem os executores de RPAs, consomem a fila do cronos
            try:
                host = self.socket.gethostbyname(vm)
                processos = os.popen(f'wmic /node:{host} /user:{self.usuario} /password:{self.pwd} process get description').read()
            except:
                status_vm = 'erro'
                print('{:<20} {:<8}'.format(vm, status_vm))
                continue
            if 'python.exe' in processos: 
                status_vm = 'ok'
                print('{:<20} {:<8}'.format(vm, status_vm))
            else:
                status_vm = 'erro'
                print('{:<20} {:<8}'.format(vm, status_vm))
            dic_vms[vm] = status_vm
            self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET vm_status = '{status_vm}' WHERE vm_host = '{vm}'")
        print()
        return dic_vms
                
              
                
    def check_status_rpas_na_fila(self, tipo_status='erro', ver_todos_status=False):
        if ver_todos_status:
            df = self.dados.consultar_banco_dados(self.conexao, f"SELECT * FROM rpa_fila")
        else:
            df = self.dados.consultar_banco_dados(self.conexao, f"SELECT * FROM rpa_fila WHERE status_rpa='{tipo_status}'")
        df = df[['cod_rpa', 'executar_na_vm', 'status_rpa']]
        print(df)
        print()
        return df
    
                          
class Escrever_por_extenso:  
            
    def __init__(self):
        self.url_api_escreve_por_extenso = str(gerador_pwd('por_extenso', 'senha'))
   
    
    def numero_por_extenso(self, valor:str):
        '''
        texto = escrever_por_extenso.numero_por_extenso('10000,48')\n
        print -> DEZ MIL REAIS E QUARENTA E OITO CENTAVOS
        '''
    
        if ',' in valor and '.' in valor:
            valor = valor.replace('.','')
            valor = valor.replace(',','.')
        elif ',' in valor:
            valor = valor.replace(',','.')
       
        url = self.url_api_escreve_por_extenso   
        res = requests.post(url, data={"Valor": f'{valor}', "Monetario": "Sim"})
        try:
            resposta = res.json()['Valor'].upper()
        except:
            time.sleep(5)
            res = requests.post(url, data={"Valor": f'{valor}', "Monetario": "Sim"})
            resposta = str(res.json()['Valor'].upper())
        return resposta



    def taxa_por_extenso(self, valor_taxa:str):
        '''
    texto = convert_to_extenso.taxa_por_extenso('1.55')\n
    print -> UM VIRGULA CINQUENTA E CINCO POR CENTO
    
        ''' 
        
        if ',' in valor_taxa and '.' in valor_taxa:
            valor_taxa = valor_taxa.replace('.','')
            valor_taxa = valor_taxa.replace(',','.')
        elif ',' in valor_taxa:
            valor_taxa = valor_taxa.replace(',','.')  
        valor_e = '0'
        valor_d = '0' 

        if '.' in valor_taxa: 
            valor_e, valor_d = valor_taxa.split('.')
        else:
            valor_e = valor_taxa
            valor_d = '0'
            
        url = self.url_api_escreve_por_extenso   
        try:
            res = requests.post(url, data={"Valor": f'{valor_e}', "Monetario": "Não"})
            texto_e =  res.json()['Valor'].upper()
            if 'VALOR NÃO SUPORTADO' in str(texto_e): texto_e = 'ZERO'
            res = requests.post(url, data={"Valor": f'{valor_d}', "Monetario": "Não"})
            texto_d =  res.json()['Valor'].upper()
            if 'VALOR NÃO SUPORTADO' in str(texto_d): texto_d = 'ZERO'
        except:
            time.sleep(5)
            res = requests.post(url, data={"Valor": f'{valor_e}', "Monetario": "Não"})
            texto_e =  res.json()['Valor'].upper()
            if 'VALOR NÃO SUPORTADO' in str(texto_e): texto_e = 'ZERO'
            res = requests.post(url, data={"Valor": f'{valor_d}', "Monetario": "Não"})
            texto_d =  res.json()['Valor'].upper()
            if 'VALOR NÃO SUPORTADO' in str(texto_d): texto_d = 'ZERO'
        taxa_extenso = texto_e + ' virgula ' + texto_d + ' por cento'    
        return taxa_extenso.upper()
        
                     
class Gerador_de_codigo:
    
    def __init__(self):
        pass
    
    
    def comentar_linha(self, path:str, search:str):
        f = open(path, 'r')
        texto= str(f.read())
        texto = texto.replace(search, '#' + search)
        f.close()
        # time.sleep(1)
        f = open(path, 'w')
        f.write(texto)
        # time.sleep(1)
        f.close()

                        
    def template_novo_rpa(self, script_file_path:str):
        '''
        from rpa_coop import gerador_de_codigo\n
        gerador_de_codigo.template_novo_rpa( __file__ )
        '''
              
        txt = '''def main(processo=0):
    qtd_atividades = 1
    msg_log = "em andamento"
    update_status = "andamento"
    try:

        # SEU CODIGO AQUI 

        qtd_atividades = 1
        msg_log = "Concluido com sucesso"
        update_status = "sucesso"
    except Exception as e:
        msg_log = str(e)
        update_status = "erro"
        qtd_atividades = 1
    finally:
        qtd_atividades = str(qtd_atividades)
        return update_status, msg_log, qtd_atividades'''
        
        file = open(script_file_path, 'a')
        file.write(txt)
        file.close()
        self.comentar_linha(script_file_path, 'gerador_de_codigo.')
        
           
    def pandas_add_linhas_to_DataFrame(self, script_file_path:str):
        '''
        from rpa_coop import gerador_de_codigo\n
        gerador_de_codigo.pandas_add_linhas_to_DataFrame( __file__ )
        '''
        
              
        txt = '''import pandas as pd

# Exemplo dados de entrada em formato DataFrame
df = pd.DataFrame([{'cod_area': 1, 'ag': 2, 'cep': 3}, {'cod_area': 4, 'ag': 5, 'cep': 6}, {'cod_area': 7, 'ag': 8, 'cep': 9}])

# Novo DataFrame vazio que receberá os valores filtrados
df2 = pd.DataFrame()

for linha in df.itertuples():
    # FILTRAR AS AGENCIA PARES
    if int(linha.ag) % 2 == 0:
        
        CODIGO = str(linha.cod_area)
        AGENCIA = 'AG-' + str(linha.ag).zfill(2)
               
        df1 = pd.DataFrame(
            [{
            'CODIGO_AREA': CODIGO,
            'AGENCIA ': AGENCIA
            }], 
            index= None)
        df2 = pd.concat([df1, df2])
        
print(df2)'''
        
        file = open(script_file_path, 'a')
        file.write(txt)
        file.close()        
        self.comentar_linha(script_file_path, 'gerador_de_codigo.')
        
           
class Selenium:
    
    def __init__(self):
        pass
    
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.alert import Alert
    
    from selenium.webdriver.chrome.service import Service as ChromeService 
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options as chrome_options
    
    from selenium.webdriver.edge.service import Service as EdgeService
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium.webdriver.edge.options import Options as edge_options
    
    
    def driver_chrome(self):
        driver = self.webdriver.Chrome(service=(self.ChromeService(self.ChromeDriverManager().install())))
        return driver
    
    
    def driver_edge(self):
        driver = self.webdriver.Edge(service=(self.EdgeService(self.EdgeChromiumDriverManager().install())))
        return driver
    
    
    def aguardar_elemento(self, driver, xpath, espera_em_segundos=60):
        '''Espera por um elemento até o tempo máximo definido, interrompe a espera assim que encontrar o elemento'''
        elemento_esperado = self.WebDriverWait(driver, espera_em_segundos).until(self.ec.visibility_of_element_located((self.By.XPATH, xpath)))
        encontrou = str(elemento_esperado.is_displayed())
        return encontrou
        
        
class Dia_util:
    
    ano_atual = int(datetime.now().strftime('%Y'))
    dd = int(datetime.now().strftime('%d'))
    mm = int(datetime.now().strftime('%m'))
    yyyy = int(datetime.now().strftime('%Y'))
      
      
    def feriados_nacionais(self, ano= ano_atual, retorna=True, imprime=False):
        self.ano = int(ano)
        datas_arr = []
        datas_dict = {}
        self.calculo_pascoa()
        
        # Monta a data exata da Páscoa no Ano
        dtPA = date(ano, self.mes, self.dia)
        # Carnaval ocorre 47 dias antes da páscoa
        dtCN = date.fromordinal(dtPA.toordinal() - 47)
        # Corpus Christ ocorre 60 dias depois da páscoa
        dtCC = date.fromordinal(dtPA.toordinal() + 60)
        # Sexta-feira Santa ocorre 2 dias antes da páscoa
        dtSS = date.fromordinal(dtPA.toordinal() - 2)
        
        # Ano Novo
        dt_aux = f'01/01/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Confraternização - Ano Novo'})
        
        # Carnaval
        dt_aux = dtCN.strftime('%d/%m/%Y')
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Carnaval - facultativo'})
        
        # Sexta-feira Santa
        dt_aux = dtSS.strftime('%d/%m/%Y')
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Sexta-feira Santa'})
        
        # Pascoa
        dt_aux = dtPA.strftime('%d/%m/%Y')
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Pascoa'})
        
        # Tiradentes
        dt_aux = f'21/04/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Tiradentes'})
        
        # Dia do Trabalho
        dt_aux = f'01/05/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Dia do Trabalho'})
        
        # Corpus Christ
        dt_aux = dtCC.strftime('%d/%m/%Y')
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Corpus Christ - facultativo'})
        
        # 07 de Setembro - Independencia do Brasil
        dt_aux = f'07/09/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : '07 Setembro - Independencia do Brasil'})
        
        # 12 de Outubro - Nossa Sra Aparecida
        dt_aux = f'12/10/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : '12 de Outubro - Nossa Sra Aparecida'})
        
        # 02 de Novembro - Finados
        dt_aux = f'02/11/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : '02 de Novembro - Finados'})
        
        # 15 de Novembro - Proclamação da República
        dt_aux = f'15/11/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : '15 de Novembro - Proclamação da República'})
        
        # Natal
        dt_aux = f'25/12/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Natal'})
                   
        self.feriados = datas_arr
        
        if imprime:
            # Imprimir data e descrição
            for dt, descr in datas_dict.items():
                print(dt, descr)
                
        if retorna:
            # return datas_dict
            return datas_arr
    
    
    def dias_uteis_mes(self, mes=mm, ano=yyyy, imprime=False):
        mes = int(mes)
        ano = int(ano)
        import calendar
        calc_dias = calendar.monthrange(ano, mes)
        total_dias_mes = calc_dias[1] 
        
        semana = [
            'Segunda-feira',
            'Terça-feira',
            'Quarta-feira',
            'Quinta-Feira',
            'Sexta-feira',
            'Sábado',
            'Domingo'
            ]
        
        self.feriados_nacionais(ano, False)
        feriados = self.feriados
        dias_uteis_br = []
        dias_uteis_us = []
        
        for x in range(1, total_dias_mes+1):
            dia_us = date(ano, mes, x)
            dia_br = str(x).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano).zfill(4)
            indice_semana = dia_us.weekday()
            dia_da_semana = semana[indice_semana]
            if dia_da_semana != 'Sábado' and dia_da_semana != 'Domingo':
                if dia_br not in feriados:
                    if imprime:
                        print(dia_br, dia_da_semana)
                    dias_uteis_br.append(dia_br)
                    dias_uteis_us.append(str(ano).zfill(4) + '/' + str(mes).zfill(2) + '/' + str(x).zfill(2))
        
        # return dias_uteis_us
        return dias_uteis_br

    
    def hoje_eh_dia_util(self, dia=dd, mes=mm, ano=yyyy):
        hoje = str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano).zfill(4)
        dias_uteis_br = self.dias_uteis_mes(mes, ano, False)
        # print()
        # print('hoje: ', hoje)
        if hoje in dias_uteis_br:
            # print('OK - Hoje eh dia útil')
            util_day = True
        else:
            # print('NAO - Hoje não eh dia útil')
            util_day = False
        return util_day
            

    def calculo_pascoa(self):
        p1 = (19 * (self.ano % 19) + 24) % 30
        p2 = (2 * (self.ano % 4) + 4 * (self.ano % 7) + 6 * p1 + 5) % 7
        res = p1 + p2
        if res > 9:
            self.dia = res - 9
            self.mes = 4
        else:
            self.dia = res + 22
            self.mes = 3


    def dia_util_anterior(self, dd_mm_yy=True, yy_mm_dd=False):
        hoje = datetime.now()
        dia_anterior = (hoje - timedelta(days=1)).strftime('%d-%m-%Y')
        eh_util = False
        while not eh_util:
            hoje = hoje - timedelta(days=1)
            dd = hoje.strftime('%d')
            mm = hoje.strftime('%m')
            yy = hoje.strftime('%Y')
            eh_util = self.hoje_eh_dia_util(dd, mm, yy)
            if eh_util:
                dia_br = dd.zfill(2) + '-' + mm.zfill(2) + '-' + yy.zfill(4)
                dia_us = yy.zfill(4) + '-' + mm.zfill(2) + '-' + dd.zfill(2)
                
        if yy_mm_dd:
            dia_anterior = dia_us
        else:
            dia_anterior = dia_br
            
        return dia_anterior
    
    
    def dia_util_posterior(self, dd_mm_yy=True, yy_mm_dd=False):
        hoje = datetime.now()
        dia_util_proximo = (hoje + timedelta(days=1)).strftime('%d-%m-%Y')
        eh_util = False
        while not eh_util:
            hoje = hoje + timedelta(days=1)
            dd = hoje.strftime('%d')
            mm = hoje.strftime('%m')
            yy = hoje.strftime('%Y')
            eh_util = self.hoje_eh_dia_util(dd, mm, yy)
            if eh_util:
                dia_br = dd.zfill(2) + '-' + mm.zfill(2) + '-' + yy.zfill(4)
                dia_us = yy.zfill(4) + '-' + mm.zfill(2) + '-' + dd.zfill(2)
                
        if yy_mm_dd:
            dia_util_proximo = dia_us
        else:
            dia_util_proximo = dia_br
            
        return dia_util_proximo
        
        


    
   
