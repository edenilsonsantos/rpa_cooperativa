# Exemplos de utilizacao da bilioteca rpa_coop

```python
# linha1: update pip 
# linha2: install lib rpa-cooperativa via pip
python -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --upgrade pip
pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org pip rpa-cooperativa
```

```python
# Melhorias da versao 1.0.31
## - Add libs webdriver as service
## - Add libs dependencia para todos projetos da VM
## - Add acesso gerador de senhas
## - Melhoria metodos da classe fluid, exceptions caso nao retorne 200
```


## manipulacao da ferramenta de fluxo de trabalho: fluid
```python
########################################################
from rpa_coop import fluid

# Variaveis
id_tipo_processo = 945

# criar processo novo (rascunho)
cod_processo = fluid.criar_processo_rascunho(id_tipo_processo) # empresa 1 - sede por padrao
cod_processo = fluid.criar_processo_rascunho(id_tipo_processo, filial_orig, filial_dest) # filiais

# gravar dados em campo comun e campo-tabela
campos_comuns = {2055: '123456'}
campos_tabela = [{5221: 'Galileo Galilei', 2012: '111.222.333-55'},{5221: 'Isaac Newton.', 2012: '333.222.453-77'}]
fluid.gravar_dados_campos_comuns(cod_processo, id_tipo_processo, campos_comuns)
fluid.gravar_dados_campos_tabela(cod_processo, id_tipo_processo, 3815, [5221, 2012], campos_tabela )

# anexar arquivos em processo
cod_tipo_arquivo_fluid = '417' 
fluid.anexar_arquivo_fluid(cod_processo, 'C:\\Temp\\teste.xlsx', cod_tipo_arquivo_fluid)

# protocolar/enviar
fluid.protocolar_processo_fluid(cod_processo, id_tipo_processo) # empresa 1 - padrao, proximo nodo padrao
fluid.protocolar_processo_fluid(cod_processo, id_tipo_processo, filial_orig, filial_dest) # filiais, proximo nodo padrao
fluid.protocolar_processo_fluid(cod_processo, id_tipo_processo, filial_orig, filial_dest, nome_do_nodo='Devolver a confeccao') 
fluid.protocolar_processo_fluid(cod_processo, id_tipo_processo, nome_do_nodo='Devolver a confeccao') # nodo específico pelo nome

# pegar processos aguardando na caixa do usuario
df_processos = fluid.get_processos_fluid([id_tipo_processo]) # por padrao user do rpa no fluid, passar lista id_tipo_processo

# pegar dados de processo especifico
df_dados_processo = fluid.get_dados_processo(cod_processo)

print(df_processos)
print()
print(df_dados_processo)
```

# manipulacao de banco de dados
```python
########################################################

from rpa_coop import dados

# conexao
conexao = dados.criar_engine('nome_db')

# select
df = dados.select_banco_dados(conexao, "SELECT * FROM rpas WHERE id = 9161")
print(df)

# update
dados.update_banco_dados(conexao, "UPDATE rpas SET nome = 'test' WHERE id = 9161")

# insert
sql = "INSERT INTO rpa_fila(cod_rpa, status_rpa, vm) VALUES (6001, 'novo', 'VM01')"
dados.insert_banco_dados(conexao, sql)
```

# sistema legado acclient
```python
########################################################

from rpa_coop import acc 

# abrir aplicativo acc 
# obs. se transacional = False, clica na opção relatorios no menu inicial
acc.open_acclient('siat', transacional=True)

# verificar se existe texto na tela para decidir a proxima acao
acc.exist_text('Retorna ao Sistema')
acc.exist_text('Retorna ao Sistema', topo1=100, topo2=200, continua_seerro=True)

# navegar ao menu, sequencia de letras, no caso C.B.C
acc.select_menu_letras('cbc')

# aguarda a mensagem de texto na tela, para realizar a acao
acc.exist_text('Informe a conta')

# acao de digitar o numero da conta na tela
acc.p.write('123123')

# acao de pressionar enter
acc.p.press('enter')
```

# gerador de senhas de sistemas com rpa
```python
########################################################
# OBS. 
# funciona somente em maquinas no dominio da empresa, 
# e maquinas que possuam as variaveis de ambientes para acesso ao cofre de senhas

from rpa_coop import gerador_pwd

usuario = gerador_pwd('denodo', 'usuario')
print(usuario)

senha = gerador_pwd('denodo', 'senha')
print(senha)
```

