import requests
from bs4 import BeautifulSoup
from clean_consulta import cleanConsulta
from clean_consulta_historica import cleanConsultaHistorica

def consultaRuc(numeroRUC):
    #Primera conexión con SUNAT
    payload={}
    headers = {
        'Host': 'e-consultaruc.sunat.gob.pe',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }

    urlInicial = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"
    sesion = requests.Session()
    response = sesion.request("GET", urlInicial, headers=headers, data=payload, verify=True)

    #Si la primera conexión fue satisfactoria
    if response.ok:
        #Cambio de header con referido de la primera URL
        headers = {
            'Host': 'e-consultaruc.sunat.gob.pe',
            'Origin': 'https://e-consultaruc.sunat.gob.pe',
            'Referer': urlInicial,
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            }
        
        #Obtenemos el número random mediante consulta de DNI
        numeroDNI = "20010271"
        url = f"https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias?accion=consPorTipdoc&razSoc=&nroRuc=&nrodoc={numeroDNI}&contexto=ti-it&modo=1&search1=&rbtnTipo=2&tipdoc=1&search2={numeroDNI}&search3=&codigo="
        response = sesion.request("POST", url, headers=headers, data=payload, verify=True)
        numeroRandom = 0

        if response.ok:
            contenidoHTML = response.text
            soup = BeautifulSoup(contenidoHTML, 'html.parser')
            numeroRandom = soup.find('input', {'name': 'numRnd'})['value']

            #Sólo teniendo el número random, procedemos a consultar el RUC
            url = f"https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias?accion=consPorRuc&nroRuc={numeroRUC}&contexto=ti-it&modo=1&numRnd={numeroRandom}"
            response = sesion.request("POST", url, headers=headers, data=payload, verify=True)
            contenidoHTML = response.text

            rucdata = cleanConsulta(contenidoHTML)

            #Consultar información Histórica
            data = {
                "accion": "getinfHis",
                "contexto": "ti-it",
                "modo": "1",
                "nroRuc": f"{rucdata['ruc']}",
                "desRuc": f"{rucdata['r_social']}"
            }

            response = sesion.request("POST", urlInicial, headers=headers, data=data, verify=True)
            contenidoHTML = response.text

            historicdata = cleanConsultaHistorica(contenidoHTML)
            rucdata['habilitada'][2] = historicdata
            print(rucdata)

            return rucdata
        else:
            print("Hubo un problema al obtener el numeroRandom mediante DNI")
            print(f"Error de página {response.status_code}")
    else:
        print("Hubo un problema al obtener el numeroRandom mediante DNI")
        print(f"Error de página {response.status_code}")