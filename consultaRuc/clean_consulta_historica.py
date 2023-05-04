from bs4 import BeautifulSoup

"""
Retorna: tupla
(HABIDO o cualquier otra condición reciente, fecha)
"""

def cleanConsultaHistorica(contenidoHTML):
    
    soup = BeautifulSoup(contenidoHTML, 'html.parser')
    box = soup.find('div', class_="table-responsive")
    txts = box.find_all('tbody')

    box = str(txts[1])

    soup = BeautifulSoup(box, 'html.parser')
    cond_contrib = soup.find('td', attrs={'align': 'left'}).text.strip()
    
    txts = soup.find_all('td', attrs={'align': 'center'})
    date_end = txts[1].get_text().strip()

    historical_data = (cond_contrib, date_end)

    return historical_data