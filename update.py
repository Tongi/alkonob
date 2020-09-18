import sys
import json
import re
import time
import datetime
import urllib.request
from discord_webhook import DiscordWebhook, DiscordEmbed
from multiprocessing import Process

dict_EU = {}
dict1_EU = {}

testing_EU = False

test_EU = ""
test_outofstock_EU = ""
test_restock_EU = ""
outofstock_stockid_EU = ""
restock_stockid_EU = ""

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

# runInParallel(func1, func2)

def Supreme_EU():

    with urllib.request.urlopen("http://www.supremenewyork.com/mobile_stock.json") as url_EU:

        supremeLink_EU = json.loads(url_EU.read().decode("utf-8"))

        Currency_EU = "€"

        for products_and_categories_EU in supremeLink_EU['products_and_categories'].items():

            products_and_categoriesName_EU = products_and_categories_EU[0]

            for supreme_EU in products_and_categories_EU[1]:

                ProductName_EU = supreme_EU["name"];

                ProductCategory_EU = supreme_EU["category_name"]
                ProductCategory1_EU = supreme_EU["category_name"].lower()

                if (ProductCategory1_EU == "tops/sweaters"):

                    ProductCategory1_EU = "tops-sweaters"

                ProductID_EU = supreme_EU["id"]

                ProductPriceEuro_EU = supreme_EU["price_euro"];
                ProductPrice_EU = supreme_EU["price"];

                if (str(ProductPriceEuro_EU)[-2:] != "00" and str(ProductPrice_EU)[-2:] != "00"):

                    ProductPriceFix_EU = " (£" + "{:_.2f}".format(float(str(ProductPrice_EU[:-2] + '.' + ProductPrice_EU[-2:]))).replace('.', ',').replace('_', '.') + ")";
                    ProductPriceEuroFix_EU = "{:_.2f}".format(float(str(ProductPriceEuro_EU[:-2] + '.' + ProductPriceEuro_EU[-2:]))).replace('.', ',').replace('_', '.');

                elif (str(ProductPriceEuro_EU)[-2:] != "00" and str(ProductPrice_EU)[-2:] == "00"):

                    ProductPriceFix_EU = " (£" + "{:_.0f}".format(int(str(ProductPrice_EU)[:-2])).replace('.', ',').replace('_', '.') + ")";
                    ProductPriceEuroFix_EU = "{:_.2f}".format(float(str(ProductPriceEuro_EU[:-2] + '.' + ProductPriceEuro_EU[-2:]))).replace('.', ',').replace('_', '.');

                elif (str(ProductPrice_EU)[-2:] != "00" and str(ProductPriceEuro_EU)[-2:] == "00"):

                    ProductPriceFix_EU = " (£" + "{:_.2f}".format(float(str(ProductPrice_EU[:-2] + '.' + ProductPrice_EU[-2:]))).replace('.', ',').replace('_', '.') + ")";
                    ProductPriceEuroFix_EU = "{:_.0f}".format(int(str(ProductPriceEuro_EU)[:-2])).replace('.', ',').replace('_', '.');

                else:

                    ProductPriceFix_EU = " (£" + "{:_.0f}".format(int(str(ProductPrice_EU)[:-2])).replace('.', ',').replace('_', '.') + ")";
                    ProductPriceEuroFix_EU = "{:_.0f}".format(int(str(ProductPriceEuro_EU)[:-2])).replace('.', ',').replace('_', '.');

                with urllib.request.urlopen("https://www.supremenewyork.com/shop/" + str(ProductID_EU) + ".json") as IDurl_EU:

                    supremeIDLink_EU = json.loads(IDurl_EU.read().decode("utf-8"))

                    ProductStyles_EU = supremeIDLink_EU["styles"]
                    ProductDescription_EU = supremeIDLink_EU["description"]

                    for tongibiggestnoob_EU in ProductStyles_EU:

                        color_EU = tongibiggestnoob_EU["name"];
                        style_Id_EU = tongibiggestnoob_EU["id"];
                        style_Currency_EU = tongibiggestnoob_EU["currency"];
                        image_EU = tongibiggestnoob_EU["bigger_zoomed_url"];

                        for ProductSizes_EU in tongibiggestnoob_EU["sizes"]:

                            ProductSize_EU = ProductSizes_EU["name"];
                            ProductStockID_EU = ProductSizes_EU["id"];
                            ProductStockLevel_EU = ProductSizes_EU["stock_level"];

                            color_EU = (re.compile(ProductSize_EU, re.IGNORECASE).sub("", color_EU)).strip()

                            if color_EU.endswith("-"):

                                color_EU = color_EU[:-1]

                            if ProductStockID_EU not in dict1_EU:

                                dict1_EU[ProductStockID_EU] = {"ProductStockID_EU" : ProductStockID_EU, "ProductStockLevel_EU" : ProductStockLevel_EU}

                            if ProductStockID_EU not in dict_EU:

                                dict_EU[ProductStockID_EU] = {"ProductStockID_EU" : ProductStockID_EU, "ProductStockLevel_EU" : ProductStockLevel_EU}

                                if (testing_EU == True):

                                    global test_EU 

                                    if (style_Id_EU == test_EU):

                                        continue

                                    test_EU = style_Id_EU;

                                    time.sleep(2.0)

                                    webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/750480042924048384/XrY6OQwp8hO6ddp5CPji8RecTbSYJYsfQfzxMqZxX8SkOpDB3-jQGj7OQLTiNlVQC2Sn")

                                    embed_EU = DiscordEmbed(
                                        title=ProductName_EU, 
                                        description="**Price:** " + str(Currency_EU) + str(ProductPriceEuroFix_EU) + str(ProductPriceFix_EU) + " | " + "[**Mobile**](https://www.supremenewyork.com/mobile#products/" + str(ProductID_EU) + "/" + str(style_Id_EU) + ")" + " | [Setup](https://atc.bz/config)" + "\n**Category:** " + str(ProductCategory_EU) + "\n**Color:** " + str(color_EU), 
                                        url="https://www.supremenewyork.com/shop/" + str(ProductCategory1_EU) + "/" + str(ProductID_EU) + "/" + str(style_Id_EU),
                                        color=0xc27c0e,
                                        timestamp=(datetime.datetime.now().isoformat())
                                    )

                                    for tongibiggestnoob1_EU in tongibiggestnoob_EU["sizes"]:

                                        size1_EU = tongibiggestnoob1_EU["name"]

                                        if tongibiggestnoob1_EU["stock_level"] == 0:

                                            embed_EU.add_embed_field(name=size1_EU, value="[**[ATC]**](https://www.supremenewyork.com/) | [BOT 1](https://www.supremenewyork.com/) - [BOT 2](https://www.supremenewyork.com/)", inline=True)
                                            embed_EU.add_embed_field(name="​", value="​", inline=True)
                                            embed_EU.add_embed_field(name=" ‍  ‍  ‍  ‍  ‍  ‍  ‍ ‍ ‍ ‍```OUT-OF-STOCK```", value="​", inline=True)

                                        elif tongibiggestnoob1_EU["stock_level"] == 1:

                                            embed_EU.add_embed_field(name=size1_EU, value="[**[ATC]**](https://www.supremenewyork.com/) | [BOT 1](https://www.supremenewyork.com/) - [BOT 2](https://www.supremenewyork.com/)", inline=False)

                                        else:

                                            embed_EU.add_embed_field(name=size1_EU, value="[**[ATC]**](https://www.supremenewyork.com/) | [BOT 1](https://www.supremenewyork.com/) - [BOT 2](https://www.supremenewyork.com/)", inline=False)

                                    embed_EU.set_footer(text="Powered by Woke", icon_url="https://cdn.discordapp.com/attachments/697494373037768745/750497955353723010/woke_Aio_logo_MAIN_transparent.png")
                                    embed_EU.set_image(url="https:" + image_EU)

                                    webhook.add_embed(embed_EU)

                                    response = webhook.execute()

                            elif (dict_EU[ProductStockID_EU]["ProductStockID_EU"] == dict1_EU[ProductStockID_EU]["ProductStockID_EU"]) and (dict_EU[ProductStockID_EU]["ProductStockLevel_EU"] == dict1_EU[ProductStockID_EU]["ProductStockLevel_EU"]): # fandt ikke noget nyt

                                continue

                            elif dict_EU[ProductStockID_EU]["ProductStockID_EU"] == dict1_EU[ProductStockID_EU]["ProductStockID_EU"] and dict_EU[ProductStockID_EU]["ProductStockLevel_EU"] == 1 and dict1_EU[ProductStockID_EU]["ProductStockLevel_EU"] == 0: # lige gået "out of stock"

                                global test_outofstock_EU 
                                global outofstock_stockid_EU
                                
                                if (style_Id_EU == test_outofstock_EU):

                                        continue

                                test_outofstock_EU = style_Id_EU

                                webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/750479942004768850/3OICpjDl8JBgJzVujg2Omn7lq-VAHQky8y-CGRJXCH5HPqTSfHNtoP3lkE5ufR2fA8ir")

                                embed_EU = DiscordEmbed(
                                    title=ProductName_EU, 
                                    description="**Price:** " + str(Currency_EU) + str(ProductPriceEuroFix_EU) + str(ProductPriceFix_EU) + " | " + "[**Mobile**](https://www.supremenewyork.com/mobile#products/" + str(ProductID_EU) + "/" + str(style_Id_EU) + ")" + " | [Setup](https://atc.bz/config)" + "\n**Category:** " + str(ProductCategory_EU) + "\n**Color:** " + str(color_EU), 
                                    url="https://www.supremenewyork.com/shop/" + str(ProductCategory1_EU) + "/" + str(ProductID_EU) + "/" + str(style_Id_EU),
                                    color=0xc27c0e,
                                    timestamp=(datetime.datetime.now().isoformat())
                                )

                                for tongibiggestnoob1_EU in tongibiggestnoob_EU["sizes"]:

                                    ProductSize1_EU = tongibiggestnoob1_EU["name"];
                                    ProductStockID1_EU = tongibiggestnoob1_EU["id"];
                                    ProductStockLevel1_EU = tongibiggestnoob1_EU["stock_level"];

                                    if dict_EU[ProductStockID1_EU]["ProductStockLevel_EU"] == 1 and dict_EU[ProductStockID_EU]["ProductStockID_EU"] == ProductStockID1_EU and ProductStockLevel1_EU == 0:

                                        dict_EU[ProductStockID_EU]["ProductStockLevel_EU"] = 0

                                        print(dict_EU[ProductStockID_EU])

                                        outofstock_stockid_EU = ProductStockID1_EU

                                    if outofstock_stockid_EU == ProductStockID1_EU: 

                                        embed_EU.add_embed_field(name=ProductSize1_EU, value="[**[ATC]**](https://www.supremenewyork.com/) | [BOT 1](https://www.supremenewyork.com/) - [BOT 2](https://www.supremenewyork.com/)", inline=True);
                                        embed_EU.add_embed_field(name=" ‍", value=" ‍", inline=True);
                                        embed_EU.add_embed_field(name=" ‍ ‍ ‍ ‍ ‍ ‍ ‍```NOW OUT-OF-STOCK```", value=" ‍", inline=True);

                                    elif ProductStockLevel1_EU == 0:

                                        embed_EU.add_embed_field(name=ProductSize1_EU, value="[**[ATC]**](https://www.supremenewyork.com/) | [BOT 1](https://www.supremenewyork.com/) - [BOT 2](https://www.supremenewyork.com/)", inline=True)
                                        embed_EU.add_embed_field(name="​", value="​", inline=True)
                                        embed_EU.add_embed_field(name=" ‍  ‍  ‍  ‍  ‍  ‍  ‍ ‍ ‍ ‍```OUT-OF-STOCK```", value="​", inline=True)

                                    elif ProductStockLevel1_EU == 1:

                                        embed_EU.add_embed_field(name=ProductSize1_EU, value="[**[ATC]**](https://www.supremenewyork.com/) | [BOT 1](https://www.supremenewyork.com/) - [BOT 2](https://www.supremenewyork.com/)", inline=False)

                                    else:

                                        embed_EU.add_embed_field(name=ProductSize1_EU, value="[**[ATC]**](https://www.supremenewyork.com/) | [BOT 1](https://www.supremenewyork.com/) - [BOT 2](https://www.supremenewyork.com/)", inline=False)

                                embed_EU.set_footer(text="Powered by Woke", icon_url="https://cdn.discordapp.com/attachments/697494373037768745/750497955353723010/woke_Aio_logo_MAIN_transparent.png")
                                embed_EU.set_image(url="https:" + image_EU)

                                webhook.add_embed(embed_EU)

                                response = webhook.execute()

                            elif dict_EU[ProductStockID_EU]["ProductStockID_EU"] == dict1_EU[ProductStockID_EU]["ProductStockID_EU"] and dict_EU[ProductStockID_EU]["ProductStockLevel_EU"] == 0 and dict1_EU[ProductStockID_EU]["ProductStockLevel_EU"] == 1: # restock

                                global test_restock_EU
                                global restock_stockid_EU

                                if (style_Id_EU == test_restock_EU):

                                        continue

                                test_restock_EU = style_Id_EU

                                webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/750479838539808808/bxt_HojreEtys9f1O060M45SQyIlxXW92WJIYN_9dIcTxcA52CCLVw3wG3krvlRZ8f59")

                                embed_EU = DiscordEmbed(
                                    title=ProductName_EU, 
                                    description="**Price:** " + str(Currency_EU) + str(ProductPriceEuroFix_EU) + str(ProductPriceFix_EU) + " | " + "[**Mobile**](https://www.supremenewyork.com/mobile#products/" + str(ProductID_EU) + "/" + str(style_Id_EU) + ")" + " | [Setup](https://atc.bz/config)" + "\n**Category:** " + str(ProductCategory_EU) + "\n**Color:** " + str(color_EU), 
                                    url="https://www.supremenewyork.com/shop/" + str(ProductCategory1_EU) + "/" + str(ProductID_EU) + "/" + str(style_Id_EU),
                                    color=0xc27c0e,
                                    timestamp=(datetime.datetime.now().isoformat())
                                )

                                for tongibiggestnoob1_EU in tongibiggestnoob_EU["sizes"]:

                                    ProductSize1_EU = tongibiggestnoob1_EU["name"];
                                    ProductStockID1_EU = tongibiggestnoob1_EU["id"];
                                    ProductStockLevel1_EU = tongibiggestnoob1_EU["stock_level"];

                                    if dict_EU[ProductStockID1_EU]["ProductStockLevel_EU"] == 0 and dict_EU[ProductStockID_EU]["ProductStockID_EU"] == ProductStockID1_EU and ProductStockLevel1_EU == 1:

                                        dict_EU[ProductStockID_EU]["ProductStockLevel_EU"] = 1

                                        print(dict_EU[ProductStockID_EU])

                                        restock_stockid_EU = ProductStockID1_EU

                                    if restock_stockid_EU == ProductStockID1_EU: 

                                        embed_EU.add_embed_field(name=ProductSize1_EU, value="[**[ATC]**](https://www.supremenewyork.com/) | [BOT 1](https://www.supremenewyork.com/) - [BOT 2](https://www.supremenewyork.com/)", inline=True);
                                        embed_EU.add_embed_field(name=" ‍", value=" ‍", inline=True);
                                        embed_EU.add_embed_field(name=" ‍  ‍  ‍  ‍  ‍  ‍  ‍ ‍ ‍ ‍```NOW IN-STOCK```", value=" ‍", inline=True);

                                    elif ProductStockLevel1_EU == 0:

                                        embed_EU.add_embed_field(name=ProductSize1_EU, value="[**[ATC]**](https://www.supremenewyork.com/) | [BOT 1](https://www.supremenewyork.com/) - [BOT 2](https://www.supremenewyork.com/)", inline=True)
                                        embed_EU.add_embed_field(name="​", value="​", inline=True)
                                        embed_EU.add_embed_field(name=" ‍  ‍  ‍  ‍  ‍  ‍  ‍ ‍ ‍ ‍```OUT-OF-STOCK```", value="​", inline=True)

                                    elif ProductStockLevel1_EU == 1:

                                        embed_EU.add_embed_field(name=ProductSize1_EU, value="[**[ATC]**](https://www.supremenewyork.com/) | [BOT 1](https://www.supremenewyork.com/) - [BOT 2](https://www.supremenewyork.com/)", inline=False)

                                    else:

                                        embed_EU.add_embed_field(name=ProductSize1_EU, value="[**[ATC]**](https://www.supremenewyork.com/) | [BOT 1](https://www.supremenewyork.com/) - [BOT 2](https://www.supremenewyork.com/)", inline=False)

                                embed_EU.set_footer(text="Powered by Woke", icon_url="https://cdn.discordapp.com/attachments/697494373037768745/750497955353723010/woke_Aio_logo_MAIN_transparent.png")
                                embed_EU.set_image(url="https:" + image_EU)

                                webhook.add_embed(embed_EU)

                                response = webhook.execute()

                            else:

                                print("Tonginoob")

        dict1_EU.clear()

        time.sleep(5.0)

        Supreme_EU()


Supreme_EU()