
    
    
from rpa_coop import dados, gerador_de_codigo

#gerador_de_codigo.template_novo_rpa(__file__)


def main(processo=0):
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
        return update_status, msg_log, qtd_atividades