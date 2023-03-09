# Exemplos de utilizacao da bilioteca rpa_coop

```python
pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org pip rpa-cooperativa
```


## manipulacao da ferramenta de fluxo de trabalho: fluid
```python
########################################################
from rpa_coop import fluid

# Variaveis
id_tipo_processo = 945
valor_campos_comuns = {2055: '782633'}
valor_campos_tabela = [{5221: 'Galileo Galilei', 2012: '111.222.333-55'},{5221: 'Isaac Newton.', 2012: '333.222.453-77'}]

# criar processo novo (rascunho)
cod_processo, nodo_inicial = fluid.criar_processo_rascunho(id_tipo_processo)

# gravar dados em campo comun e campo-tabela
fluid.gravar_dados_campos_comuns(cod_processo, id_tipo_processo, valor_campos_comuns)
fluid.gravar_dados_campos_tabela(cod_processo, id_tipo_processo, 3815, [5221, 2012], valor_campos_tabela )

# anexar arquivos em processo
fluid.anexar_arquivo_fluid(cod_processo, 'C:\\Temp\\teste.xlsx', '417')

# protocolar/enviar
fluid.protocolar_processo_fluid(cod_processo, id_tipo_processo)

# pegar processos aguardando na caixa do usuario
df_processos = fluid.get_processos_fluid([id_tipo_processo])

# pegar dados de processo específico
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
# obs. se transacional = False, clica na opção relatórios no menu inicial
acc.open_acclient('siat', transacional=True)

# verificar se existe texto na tela para decidir a proxima acao
acc.exist_text('Retorna ao Sistema')

# navegar ao menu, sequencia de letras, no caso C.B.C
acc.select_menu_letras('cbc')

# aguarda a mensagem de texto na tela, para realizar a acao
acc.exist_text('Informe a conta')

# acao de digitar o numero da conta na tela
acc.p.write('123123')

# acao de pressionar enter
acc.p.press('enter')
```
