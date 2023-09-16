from dotenv import load_dotenv
import os
import pandas as pd
import asyncio
from prisma import Prisma

from extract_data import extract_product

load_dotenv()

sheet_base_url = "https://docs.google.com/spreadsheets/d/"
sheet_id = os.getenv("SHEET_ID")

try:
    df = pd.read_csv(sheet_base_url + sheet_id + "/export?format=csv", sep=",")
    urls_list = list(df.values.flatten().tolist())

except Exception as e:
    print(f'No se pudo leer la hoja de datos: {str(e)}')

async def main():
    products_list = []

    for url in urls_list:
        product = extract_product(url)
        products_list.append(product)
        print(product)

    db = Prisma()
    await db.connect()

    # user1 = await db.user.create({
    #     "name": "Tomas",
    #     "email": os.getenv("SENDER_EMAIL")
    # })

    # print(f'created post: {user1.model_dump_json(indent=2)}')

    user1 = await db.user.find_unique(where={
        "email": os.getenv("SENDER_EMAIL")
    })
    assert user1 is not None
    print(f'found user: {user1.model_dump_json(indent=2)}')

    for product in products_list:
        prod = await db.product.find_unique(where={
            "shopId": product["product_id"]
        })

        if prod: 
            print(f'ya estaba el producto con shopId {prod.shopId}')

    # productsUser = await db.product.find_many(
    #     where={
    #         "users": {"every":{
    #             "id": user1.id
    #         }}
    #     },
    #     include={
    #         "users": True,
    #         "prices": True
    #     },
        
    # )
    # for product in productsUser:
    #     print(f'product: {product.model_dump_json(indent=2)}')

    # for product in products_list:
    #     prod = await db.product.create({
    #         "name": product["title"],
    #         "imgUrl": product["img"],
    #         "shopId": product["product_id"],
    #         "users": {
    #             "connect": [{
    #                 "id": user1.id
    #             }]
    #         },
    #         "prices":{
    #             "create": [{
    #                 "price": product["price"],
    #             }]
    #         }
    #     })
    #     print(f'product: {prod.model_dump_json(indent=2)}')

    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
