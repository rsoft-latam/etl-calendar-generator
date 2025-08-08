import pandas as pd
import boto3
from io import BytesIO
import re

MONTH_MAP = {
    "enero": "January", "febrero": "February", "marzo": "March",
    "abril": "April", "mayo": "May", "junio": "June",
    "julio": "July", "agosto": "August", "septiembre": "September",
    "octubre": "October", "noviembre": "November", "diciembre": "December"
}

def translate_date(date_str):
    # miércoles, 01 de enero de 2025
    date_str = re.sub(r'^\w+,\s*', '', date_str.lower().strip())

    # 01 de enero de 2025
    for es, en in MONTH_MAP.items():
        date_str = re.sub(rf'de {es} de', f'of {en}', date_str)

    # 01 of January 2025
    return re.sub(r'\s+', ' ', date_str)

def read_excel_rows_from_s3(bucket_name, object_key):
    s3 = boto3.client('s3')
    reponse = s3.get_object(Bucket=bucket_name, Key=object_key)
    file_stream = BytesIO(reponse['Body'].read())
    df = pd.read_excel(file_stream, header=2)
    df.columns = df.columns.str.strip()
    fecha_col = next((col for col in df.columns if col.lower() == 'fecha'), None)
    translated_dates = df[fecha_col].astype(str).apply(translate_date)

    df['Fecha'] = pd.to_datetime(translated_dates, errors='coerce', dayfirst=True)
    df = df.dropna(subset=['Fecha'])

    return df

