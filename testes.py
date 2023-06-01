
########################################

from rpa_coop import acc

# usando multi janelas do sistema acc, alternando entre elas
acc.open_acclient(['siat', 'sacg'])

acc.exist_text('Retorna ao Sistema', nome_janela = 'siat')
acc.select_menu_letras('cbaa', nome_janela = 'siat')

acc.exist_text('Retorna ao Sistema', nome_janela = 'sacg')
acc.select_menu_letras('cga', nome_janela = 'sacg')
