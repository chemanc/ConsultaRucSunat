from bs4 import BeautifulSoup

"""
Datos para diccionario (return) -> en Caso de RUC 10
'ruc': ruc,
'r_social': r_social,
't_contribuyente': t_contribuyente,
'documento': documento,
'date_inscripcion': date_inscripcion,
'date_inicio_actividades': date_inicio_actividades,
'habilitada': habilitada,
'domicilio_fiscal': domicilio_fiscal,
'emision_comprobante': emision_comprobante,
'comercio_exterior': comercio_exterior,
'sis_contable': sis_contable,

Datos para data (return) -> en Caso de RUC 20
'ruc': ruc,
'r_social': r_social,
't_contribuyente': t_contribuyente,
'nombre_comercial': nombre_comercial,
'date_inscripcion': date_inscripcion,
'date_inicio_actividades': date_inicio_actividades,
'habilitada': habilitada,
'domicilio_fiscal': domicilio_fiscal,
'emision_comprobante': emision_comprobante,
'comercio_exterior': comercio_exterior,
'sis_contable': sis_contable,
"""

def cleanConsulta(contenidoHTML):
    
    soup = BeautifulSoup(contenidoHTML, 'html.parser')
    box = soup.find('div', class_="list-group")

    data = {}
    #data = ()

    ruc, r_social = box.find('div', class_='col-sm-7').find('h4', class_='list-group-item-heading').text.split(' - ')

    txts = box.find_all('p', class_='list-group-item-text')

    campos = []
    for txt in txts:
        campos.append(txt.get_text())

    if 'IMPORTANTE' in campos[0]:
        campos.pop(0)

    t_contribuyente = campos[0]

    if ruc[:2] == '10':
        dni, nombre = campos[1].split('-')
        dni = dni.split('DNI')
        dni = [parte.strip() for parte in dni]
        documento = [dni[1], nombre]
        documento = [parte.strip() for parte in documento]
        date_inscripcion = campos[3]
        date_inicio_actividades = campos[4]
        habilitada = ['', '', '']
        habilitada[0] = campos[5].replace('\r', '').replace('\n', '').replace('\t', '').replace('  ', '').strip()
        habilitada[1] = campos[6].strip()
        domicilio_fiscal = ['', '', '', '', '']
        if len(campos[7].strip()) > 5 and ' (' in campos[7].strip():
            df_0 = campos[7].replace('  ', ' ').replace('    ', '').replace('  ', ' ').strip()
            df_1 = df_0.split(' (')
            df_2 = df_1[1].split(') ')
            df_3 = df_2[1].split('-')
            df_3 = [parte.strip() for parte in df_3]
            domicilio_fiscal = [df_1[0], df_2[0], df_3[0], df_3[1], df_3[2]]
        elif len(campos[7].strip()) > 5:
            df_0 = campos[7].replace('  ', ' ').replace('    ', '').replace('  ', ' ').strip()
            df_1 = df_0.split('-')
            df_1 = [parte.strip() for parte in df_1]
            df_2 = df_1[0].rsplit(' ', maxsplit=1)
        else:
            df_0 = campos[7].strip()
            domicilio_fiscal = [df_0, '', '', '', '']
        emision_comprobante = campos[8]
        comercio_exterior = campos[9]
        sis_contable = campos[10]

        #data = (ruc, r_social, t_contribuyente, documento, date_inscripcion, date_inicio_actividades, habilitada, domicilio_fiscal, emision_comprobante, comercio_exterior, sis_contable)
        data = {
            'ruc': ruc,
            'r_social': r_social,
            't_contribuyente': t_contribuyente,
            'documento': documento,
            'date_inscripcion': date_inscripcion,
            'date_inicio_actividades': date_inicio_actividades,
            'habilitada': habilitada,
            'domicilio_fiscal': domicilio_fiscal,
            'emision_comprobante': emision_comprobante,
            'comercio_exterior': comercio_exterior,
            'sis_contable': sis_contable,
        }

    else:
        nombre_comercial = campos[1].strip()
        date_inscripcion = campos[2]
        date_inicio_actividades = campos[3]
        habilitada = ['', '', '']
        habilitada[0] = campos[4].replace('\r', '').replace('\n', '').replace('\t', '').replace('  ', '').strip()
        habilitada[1] = campos[5].strip()
        domicilio_fiscal = ['', '', '', '', '']
        if len(campos[6].strip()) > 5 and ' (' in campos[6].strip():
            df_0 = campos[6].replace('  ', ' ').replace('    ', '').replace('  ', ' ').strip()
            df_1 = df_0.split(' (')
            df_2 = df_1[1].split(') ')
            df_3 = df_2[1].split('-')
            df_3 = [parte.strip() for parte in df_3]
            domicilio_fiscal = [df_1[0], df_2[0], df_3[0], df_3[1], df_3[2]]
        elif len(campos[6].strip()) > 5:
            df_0 = campos[6].replace('  ', ' ').replace('    ', '').replace('  ', ' ').strip()
            df_1 = df_0.split('-')
            df_1 = [parte.strip() for parte in df_1]
            df_2 = df_1[0].rsplit(' ', maxsplit=1)
        else:
            df_0 = campos[6].strip()
            domicilio_fiscal = [df_0, '', '', '', '']
        emision_comprobante = campos[7]
        comercio_exterior = campos[8]
        sis_contable = campos[9]

        data = {
            'ruc': ruc,
            'r_social': r_social,
            't_contribuyente': t_contribuyente,
            'nombre_comercial': nombre_comercial,
            'date_inscripcion': date_inscripcion,
            'date_inicio_actividades': date_inicio_actividades,
            'habilitada': habilitada,
            'domicilio_fiscal': domicilio_fiscal,
            'emision_comprobante': emision_comprobante,
            'comercio_exterior': comercio_exterior,
            'sis_contable': sis_contable,
        }

    return data