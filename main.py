import asyncio
import os
import pandas as pd
import random
import time

from dotenv import load_dotenv
from prisma import Prisma

from extract_data import extract_product
from send_mail import send_mail

load_dotenv()

sheet_base_url = "https://docs.google.com/spreadsheets/d/"
sheet_id = os.getenv("SHEET_ID")

try:
    df = pd.read_csv(sheet_base_url + sheet_id + "/export?format=csv", sep=",")
    urls_list = list(df.values.flatten().tolist())
    random.shuffle(urls_list)

except Exception as e:
    print(f'No se pudo leer la hoja de datos: {str(e)}')

async def main():
    #products_list = []
    products_list = [
        {"product_id": "B00CWB45T2", "price": 45},
        {"product_id": "B07VDLG8LR", "price": 63.15},
        {"product_id": "B0713WPGLL", "price": 102.0},
    ]
    products_list_db = []


    # for url in urls_list:
    #     product = extract_product(url)
    #     products_list.append(product)
    #     print(product)

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
    print(f'found user: {user1.name}')

    for product in products_list:
        prod = await db.product.find_unique(where={
            "shopId": product["product_id"]
        },include={"prices": True} )

        # if prod: 
        #     print(f'ya estaba el producto con shopId {prod.shopId}')
        #     new_price = await db.priceproduct.create(
        #         data={
        #             "price": product["price"],
        #             "product": {
        #                 "connect": {
        #                     "id": prod.id
        #                 }
        #             }
        #         })
        #     print(f'created price: {new_price.price}, date: {time.strftime("%d-%m-%Y %H:%M", new_price.created_at.timetuple())}')
        
        # else:
        #     new_product = await db.product.create({
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
        #     print(f'created product: {new_product.model_dump_json(indent=2)}')
        last_price = prod.prices[-1]
        print(f'last price of {prod.name}: {last_price.price} date: {time.strftime("%d-%m-%Y %H:%M", last_price.created_at.timetuple())}')
        if product["price"] < last_price.price:
            send_mail(sender=os.getenv("SENDER_EMAIL"), 
                      password=os.getenv("PASSMAIL"), 
                      receiver=user1.email, 
                      subject=f'Precio de {prod.name} bajado', 
                      body=f"""
                        <html>
                            <body style="margin:0;padding:0;">
                                <p style="font-size: large;">El precio del producto</p>
                                <h1 style="font-weight: bold;">{prod.name}</h1>
                                <img src="{prod.imgUrl}" alt="" style="width: 40%; margin: 16px 30%;">
                                <p style="font-size: large;">ha bajado a: </p>
                                <h1 style="color: crimson; text-align: center;">{product["price"]}€</h1>
                                <br>
                                <p style="font-size: large; text-align: right; margin-top: 16px;"><a href="" style="text-decoration: none; margin-top: 16px; padding: 8px 16px; background-color: lightslategray; border-radius: 8px;">Ir a la tienda -> </a></p>
                            </body>
                        </html>
                      """
                      )
            print(f'El precio del producto {prod.name} ha bajado de {last_price.price} a {product["price"]}')
        else:
            print (f'El precio del producto {prod.name} no ha bajado')

    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())








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