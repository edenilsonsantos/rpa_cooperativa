# Exemplos de utilizacao da bilioteca rpa_coop


## manipulacao da ferramenta de fluxo de trabalho: fluid
```python
########################################################
from rpa_coop import fluid

# Variaveis
id_tipo_processo = 945
valor_campos_comuns = {2055: '782633'}
valor_campos_tabela = [{5221: 'Galileo Galilei', 2012: '111.222.333-55'},{5221: 'Isaac Newton.', 2012: '333.222.453-77'}]

cod_processo, nodo_inicial = fluid.criar_processo_rascunho(id_tipo_processo)
fluid.gravar_dados_campos_comuns(cod_processo, id_tipo_processo, valor_campos_comuns)
fluid.gravar_dados_campos_tabela(cod_processo, id_tipo_processo, 3815, [5221, 2012], valor_campos_tabela )
fluid.anexar_arquivo_fluid(cod_processo, 'C:\\Temp\\teste.xlsx', '417')
fluid.protocolar_processo_fluid(cod_processo, id_tipo_processo)
df_processos = fluid.get_processos_fluid([id_tipo_processo])
df_dados_processo = fluid.get_dados_processo(cod_processo)

print(df_processos)
print()
print(df_dados_processo)
```

# manipulacao de banco de dados
```python
########################################################

from rpa_coop import dados

conexao = dados.criar_engine('nome_db')
df = dados.select_banco_dados(conexao, "SELECT * FROM rpa_hist WHERE id_fila = 9161")
print(df)
dados.update_banco_dados(conexao, "UPDATE rpa_hist SET log = 'teste_01' WHERE id_fila = 9161")
sql = "INSERT INTO rpa_fila(cod_rpa, status_rpa, vm) VALUES (6001, 'novo', 'VM01') "
dados.insert_banco_dados(conexao, sql)
```