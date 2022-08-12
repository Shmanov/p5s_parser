import requests
from lxml import etree, objectify

url_p5s = "http://stripmag.ru/datafeed/p5s_full_stock.xml"
url_business = "http://alitair.1gb.ru/Intim_Ali_allfids_2.xml"

def get_file(url, file_name):
    print("Загружаем файл" +" "+ url)
    r = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(r.content)

def data_file(file_name):
    xml_data = objectify.parse(file_name)
    return xml_data.getroot()  # Root element

def save_file(name_file, root):
    print("Сохраняем новый файл с обновлёнными данными" + " " + name_file)
    obj_xml = etree.tostring(root, pretty_print = True, xml_declaration = True)
    try:
        with open(name_file, "wb") as f:
            f.write(obj_xml)
    except IOError:
        pass

def pars_p5s(file_name):
    print("Парсим файл поставщика и создаём словарь")
    data = {}
    root = data_file(file_name)
    for product in root.findall('product'):
        id = product.attrib.get('prodID')
        assortiment = product.find('assortiment')
        sklad = assortiment.find('assort').attrib.get('sklad')
        price = product.find('price').attrib
        del price['Discount']
        data[id] = {'sklad': sklad, 'price': price}
    return data

def pars_fid(file_name):
    print("Парсим ФИД" + " " + file_name)
    data = pars_p5s(file_name='p5s_full_stock.xml')
    root = data_file(file_name)
    shop = root.find('shop')
    offers = shop.find('offers')
    for offer in offers.findall('offer'):
        id = offer.attrib.get("id")
        prod = data.get(id)
        if prod != None:
            price = offer.find('price').attrib
            quantity = offer.find('quantity')
            sorted_prod = dict(sorted(prod['price'].items()))

            print("Обновляем товар ID: " + id)
            print("Старые цены " + str(price) + " Старый остаток: " + quantity.text)
            print("Новые  цены " + str(sorted_prod) + " Новый остаток: " + prod['sklad'])

            price.update(sorted_prod)
            quantity._setText(prod['sklad'])

    return root

get_file(url = url_p5s,file_name = 'p5s_full_stock.xml')
get_file(url = url_business, file_name = 'Intim_Ali_allfids_2.xml')
root = pars_fid(file_name='Intim_Ali_allfids_2.xml')
save_file(name_file = 'new_Intim_Ali_allfids_2.xml', root = root)

print ('Выполнено')