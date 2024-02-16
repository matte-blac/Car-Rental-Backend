from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Category, AvailableCar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

def seed_database():
    with app.app_context():
        # Create categories
        categories = [
            {'category_name': 'Sedan'},
            {'category_name': 'SUV'},
            {'category_name': 'Truck'}
        ]

        for category_data in categories:
            category = Category(**category_data)
            db.session.add(category)
        
        db.session.commit()

        # Create available cars
        cars = [
            {'brand': 'Toyota', 'car_name': 'Camry', 'price': 6000.00, 'quantity': 10, 'category_id': 1, 'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhtBPG37ndC9bHiGGRaj_h4JgOEj99wR9jQuzk7moy2A&s', 'number_plate': 'KDK 001A'},
            {'brand': 'Honda', 'car_name': 'CR-V', 'price': 7000.00, 'quantity': 8, 'category_id': 2, 'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQUoD7tuai-N2rHjajm8mA2pTkXviNqdN679AP-_VglGA&s', 'number_plate': 'KDL 002B'},
            {'brand': 'Ford', 'car_name': 'F-150', 'price': 8000.00, 'quantity': 12, 'category_id': 3, 'image_url': 'https://cars.usnews.com/pics/size/390x290/images/Auto/izmo/i159614477/2021_ford_f_150_angularfront.jpg', 'number_plate': 'KDM 003C'},
            {'brand': 'Mercedes-Benz', 'car_name': 'E-Class', 'price': 8500.00, 'quantity': 6, 'category_id': 1, 'image_url': 'https://imgd.aeplcdn.com/370x208/n/cw/ec/47336/e-class-exterior-right-front-three-quarter-27.jpeg?isig=0&q=80', 'number_plate': 'KDN 004D'},
            {'brand': 'Jeep', 'car_name': 'Wrangler', 'price': 9500.00, 'quantity': 5, 'category_id': 2, 'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoMeGP4OwQgkYqZW4hfEdUXt84emXzg2_Fj0QgBe7dLA&s', 'number_plate': 'KDO 005E'},
            {'brand': 'Toyota', 'car_name': 'Tacoma', 'price': 7500.00, 'quantity': 9, 'category_id': 3, 'image_url': 'https://platform.cstatic-images.com/xlarge/in/v2/stock_photos/1da06c3a-d350-48e0-80d5-ce4ed87dc2c8/640e6f66-775c-4779-a565-eb922b215002.png', 'number_plate': 'KDP 006F'},
            {'brand': 'BMW', 'car_name': '3 Series', 'price': 7800.00, 'quantity': 7, 'category_id': 1, 'image_url': 'https://vehicle-images.dealerinspire.com/5b46-18002945/3MW89FF07P8D10033/e562d30825e6d06b741d080156ed1acd.jpg', 'number_plate': 'KDQ 007G'},
            {'brand': 'Audi', 'car_name': 'Q5', 'price': 8200.00, 'quantity': 6, 'category_id': 2, 'image_url': 'https://stimg.cardekho.com/images/carexteriorimages/630x420/Audi/Q5/10556/1689594416925/front-left-side-47.jpg', 'number_plate': 'KDR 008H'},
            {'brand': 'Chevrolet', 'car_name': 'Silverado', 'price': 8800.00, 'quantity': 10, 'category_id': 3, 'image_url': 'https://platform.cstatic-images.com/xlarge/in/v2/stock_photos/406c2669-2ca9-4db7-9821-1a561504e44c/a1c7ae74-6d51-4f87-856e-f1527ccec20e.png', 'number_plate': 'KDS 009I'},
            {'brand': 'Lexus', 'car_name': 'RX', 'price': 8900.00, 'quantity': 8, 'category_id': 2, 'image_url': 'https://cars.usnews.com/pics/size/390x290/images/Auto/izmo/i159614467/2021_lexus_rx_angularfront.jpg', 'number_plate': 'KDT 010J'},
            {'brand': 'Nissan', 'car_name': 'Altima', 'price': 6900.00, 'quantity': 7, 'category_id': 1, 'image_url': 'https://www-europe.nissan-cdn.net/content/dam/Nissan/nissan_middle_east/experience_nissan/latestnews/February2019/Image%201.jpg.ximg.l_12_m.smart.jpg', 'number_plate': 'KDU 011K'},
            {'brand': 'GMC', 'car_name': 'Sierra', 'price': 8200.00, 'quantity': 9, 'category_id': 3, 'image_url': 'https://img.sm360.ca/ir/w1024h768/images/article/steele-auto-group/99186//gmc-sierra-2022-1600-011649699837378.jpg', 'number_plate': 'KDV 012L'},
            {'brand': 'Toyota', 'car_name': 'Corolla', 'price': 5500.00, 'quantity': 6, 'category_id': 1, 'image_url': 'https://global.toyota/pages/news/images/2018/11/29/1400/20181129_03_album_images.jpg', 'number_plate': 'KDW 013M'},
            {'brand': 'Subaru', 'car_name': 'Outback', 'price': 6700.00, 'quantity': 8, 'category_id': 2, 'image_url': 'https://s7d1.scene7.com/is/image/scom/RDB_default_pass_scaled?$900p$', 'number_plate': 'KDX 014N'},
            {'brand': 'Ram', 'car_name': '1500', 'price': 8300.00, 'quantity': 9, 'category_id': 3, 'image_url': 'https://ymimg1.b8cdn.com/uploads/car_car_name/8419/pictures/9007333/2019_RAM_1500.png', 'number_plate': 'KDY 015O'},
            {'brand': 'Volvo', 'car_name': 'S60', 'price': 8000.00, 'quantity': 7, 'category_id': 1, 'image_url': 'https://media.ed.edmunds-media.com/volvo/s60/2024/oem/2024_volvo_s60_sedan_recharge-t8-ultimate_fq_oem_1', 'number_plate': 'KDZ 016P'},
            {'brand': 'Honda', 'car_name': 'Accord', 'price': 6700.00, 'quantity': 6, 'category_id': 1, 'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRf72u85UMP4F4geoRpC4PERe4xz6Sd7KtikYlE8cTzAA&s', 'number_plate': 'KEA 017Q'},
            {'brand': 'Kia', 'car_name': 'Sorento', 'price': 7400.00, 'quantity': 5, 'category_id': 2, 'image_url': 'https://inv.assets.ansira.net/1/8/5/32856549581.jpg', 'number_plate': 'KEB 018R'},
            {'brand': 'Toyota', 'car_name': 'Tundra', 'price': 9900.00, 'quantity': 8, 'category_id': 3, 'image_url': 'https://cars.usnews.com/static/images/Auto/custom/15105/2023_Toyota_Tundra_Angular_Front_1.jpg', 'number_plate': 'KEC 019S'},
            {'brand': 'Audi', 'car_name': 'A4', 'price': 7600.00, 'quantity': 7, 'category_id': 1, 'image_url': 'https://media.ed.edmunds-media.com/audi/a4/2022/oem/2022_audi_a4_sedan_prestige-s-line_fq_oem_8_1280.jpg', 'number_plate': 'KED 020T'},
            {'brand': 'Ford', 'car_name': 'Escape', 'price': 7800.00, 'quantity': 6, 'category_id': 2, 'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_BJYoAXOSx5CPw2kU2G1yPEAbA-QFVVf6v1Z3sQ7_JA&s', 'number_plate': 'KEE 021U'},
            {'brand': 'Jeep', 'car_name': 'Grand Cherokee', 'price': 8300.00, 'quantity': 5, 'category_id': 2, 'image_url': 'https://imgd.aeplcdn.com/1920x1080/n/cw/ec/132711/grand-cherokee-exterior-right-front-three-quarter.jpeg?isig=0&q=80&q=80', 'number_plate': 'KEF 022V'},
            {'brand': 'Ram', 'car_name': '3500', 'price': 9800.00, 'quantity': 4, 'category_id': 3, 'image_url': 'https://cdn.carbuzz.com/gallery-images/1600/568000/200/568290.jpg', 'number_plate': 'KEG 023W'},
            {'brand': 'Volvo', 'car_name': 'XC60', 'price': 8600.00, 'quantity': 3, 'category_id': 2, 'image_url': 'https://stimg.cardekho.com/images/carexteriorimages/630x420/Volvo/XC60/10589/1692870711844/front-left-side-47.jpg?imwidth=420&impolicy=resize', 'number_plate': 'KEH 024X'},
            {'brand': 'GMC', 'car_name': 'Acadia', 'price': 9100.00, 'quantity': 2, 'category_id': 2, 'image_url': 'https://www.motortrend.com/uploads/sites/10/2019/09/2020-gmc-acadia-at4-4wd-suv-angular-front.png', 'number_plate': 'KEI 025Y'}
        ]

        for car_data in cars:
            car = AvailableCar(**car_data)
            db.session.add(car)
        
        db.session.commit()

if __name__ == '__main__':
    seed_database()