from rpa_coop import acc 

# acc.open_acclient('siat', transacional=True)
# acc.exist_text('Retorna ao Sistema')
# acc.select_menu_letras('cbc')
# acc.exist_text('Informe a conta')
# acc.p.write('123123')
# acc.p.press('enter')

import site 
# r = site.getusersitepackages()
user_site_packages = site.getusersitepackages()
user_site_packages = user_site_packages.replace('Roaming', 'Local\\Programs').replace('site-packages','Lib\\site-packages')

print(user_site_packages)
