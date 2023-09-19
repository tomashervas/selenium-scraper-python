import asyncio
import datetime
import os
import pandas as pd
import plotly.express as px
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
    products_list_names = []
    today = datetime.date.today().isoweekday()
    #products_list = []
    products_list = [
        {"product_id": "B00CWB45T2", "price": 45},
        {"product_id": "B07VDLG8LR", "price": 63.5},
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
                      product_name=prod.name,
                      product_img=prod.imgUrl,
                      product_price=product["price"],
                      )
            print(f'El precio del producto {prod.name} ha bajado de {last_price.price} a {product["price"]}')
        else:
            print (f'El precio del producto {prod.name} no ha bajado')

        if today == 2:
            price_list = []
            date_list = []
            for price in prod.prices:
                price_list.append(price.price)
                date_list.append(time.strftime("%d %b", price.created_at.timetuple()))
            price_list.append(product["price"])
            date_list.append(time.strftime("%d %b", datetime.datetime.now().timetuple()))
        
            data = pd.DataFrame({'x': date_list,
                        'y': price_list})
            # print(data)

            fig = px.line(data_frame=data,
                        x = 'x',
                        y = 'y',
                        labels={"x": "Dia", "y": "Precio"},
                        text= 'y',
                        )
            fig.update_traces(textposition='top center', textfont_size=20,
                            textfont_color='grey')

            fig.update_layout(
                font_family="Arial",
                font_color="grey",
                font_size=16,
                plot_bgcolor="rgba(0, 0, 0, 0)",
                paper_bgcolor="rgba(0, 0, 0, 0)",
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                margin=dict(t=20)
            )
            # fig.show()
            if not os.path.exists("images"):
                os.mkdir("images")

            fig.write_image(f"images/prices_{products_list.index(product)}.png")
            products_list_names.append(prod.name)
            

        
    if today == 2:
        send_mail(sender=os.getenv("SENDER_EMAIL"), 
                      password=os.getenv("PASSMAIL"), 
                      receiver=user1.email, 
                      subject="Evolución de los precios de tus productos",
                      product_names=products_list_names,
                      weekly=True
                      )

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