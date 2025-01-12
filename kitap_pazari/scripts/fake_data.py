import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitap_pazari.settings')

import django
django.setup()



# Python faker kütüphanesini kullanarak sahte verilerle kullanıcı kaydı oluşturuyoruz

from django.contrib.auth.models import User
from faker import Faker
import requests
from pprint import pprint
from kitaplar.api.serializers import KitapSerializer
from kitaplar.models import Kitap, Yorum

def set_user():
    fake = Faker(['en_US'])

    isim = fake.first_name()
    soyisim = fake.last_name()
    kullanici_adi = f"{isim.lower()}_{soyisim.lower()}"
    eposta = f"{kullanici_adi}@{fake.domain_name()}"
    print(isim, soyisim, kullanici_adi, eposta)

    # Kullanıcı adı veritabanında varsa sonuna rastgele sayı getirerek eşsiz yani veritabanında olmayan
    # bir kullanıcı elde edene kadar döngü kuruyoruz
    user_check = User.objects.filter(username=kullanici_adi)

    while user_check.exists():
        kullanici_adi = kullanici_adi + str(random.randint(1,100))
        user_check = User.objects.filter(username=kullanici_adi)

    # Eşsiz yani veritabanında olmayan bir kullanıcı adı bulunduğunda döngüyü kırıyoruz
    # ve kullanıcıyı oluşturuyoruz
    user = User(
        username=kullanici_adi,
        first_name=isim,
        last_name=soyisim,
        email=eposta,
        is_staff=fake.boolean(chance_of_getting_true=50),
        is_superuser = fake.boolean(chance_of_getting_true=10)
    )

    user.set_password("sifre12345")
    user.save()
    print("kullanıcı kaydedildi", kullanici_adi)




# Python faker kütüphanesini kullanarak sahte veriler üretip, requests kütüphanesini de kullanarak 
# api servisinden veriler çekip kitap kayıtları oluşturuyoruz

def kitap_ekle(konu):
    fake = Faker(["tr_TR"])
    url = 'https://openlibrary.org/search.json?'
    payload = {'q': konu}
    response = requests.get(url, params=payload)
    
    if response.status_code != 200:
        print('Hatalı istek yaptınız', response.status_code)
        return
    
    jsn = response.json()
    kitaplar = jsn.get('docs') 

    for kitap in kitaplar:
        
        veri = dict(
                isim = kitap.get('title'),
                yazar = kitap.get('author_name')[0],
                aciklama = fake.paragraph(),
                yayin_tarihi = fake.date_time_between(start_date='-20y', end_date="now", tzinfo=None)
        )
        
        serializer = KitapSerializer(data=veri) 
        
        if serializer.is_valid():
            serializer.save()
            print("kitap kaydedildi:", kitap.get("title")) 
        else:
            continue
    

    


      

    




