

from rpa_coop import fluid


# id_tipo_processo = 945
# valor_campos_comuns = {2055: '782633'}
# valor_campos_tabela = [{5221: 'Galileo Galilei', 2012: '111.222.333-55'},{5221: 'Isaac Newton.', 2012: '333.222.453-77'}]

# cod_processo, nodo_inicial = fluid.criar_processo_rascunho(id_tipo_processo)
# fluid.gravar_dados_campos_comuns(cod_processo, id_tipo_processo, valor_campos_comuns)
# fluid.gravar_dados_campos_tabela(cod_processo, id_tipo_processo, 3815, [5221, 2012], valor_campos_tabela )
# fluid.anexar_arquivo_fluid(cod_processo, 'C:\\Temp\\teste.xlsx', '417')
# fluid.protocolar_processo_fluid(cod_processo, id_tipo_processo)
# df_processos = fluid.get_processos_fluid([id_tipo_processo])
# df_dados_processo = fluid.get_dados_processo(cod_processo)

# print(df_processos)
# print()
# print(df_dados_processo)



########################################################
from rpa_coop import dados

conexao = dados.criar_engine('cronos')
df = dados.select_banco_dados(conexao, "SELECT * FROM rpa_historico WHERE id_historico_rpas = 9161")
print(df)
dados.update_banco_dados(conexao, "UPDATE rpa_historico SET msg_log = 'teste_01' WHERE id_historico_rpas = 9161")
sql = "INSERT INTO rpa_fila(num_processo_fluid, cod_rpa, nome_rpa, cod_prioridade, data_agendamento, status_rpa, executar_na_vm) VALUES (NULL, 6001, 'teste_query', '5', '2023-03-08 17:00:00', 'novo', 'VM01') "
dados.insert_banco_dados(conexao, sql)