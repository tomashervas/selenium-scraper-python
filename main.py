import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

from extract_data import extract_product

load_dotenv()

sheet_base_url = "https://docs.google.com/spreadsheets/d/"
sheet_id = os.getenv("SHEET_ID")


df = pd.read_csv(sheet_base_url + sheet_id + "/export?format=csv", sep=",")

urls_list = df.values.flatten().tolist()

print(urls_list)

# for url in listado:
#     print(url)

# if __name__ == "__main__":
#     for url in urls:
#         resultado = extract_product(url)
#         print(resultado)