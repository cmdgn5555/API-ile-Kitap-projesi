from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from datetime import datetime
from django.core.mail import send_mail
import time
from datetime import datetime


# Özel anonim throttling sınıfımızı tanımlıyoruz ve varsayılan olarak
# dakikada en fazla 7 istek gönderebilecek şekilde ayarlıyoruz.

class CustomAnonRateThrottle(AnonRateThrottle):
    rate = "7/minute"

    # Kullanıcı dakikada 7 den fazla istek yaptığında kullanıcıya yada kullanıcılara eposta gönderiyoruz
    
    #def throttle_failure(self):
    #    send_mail(
    #        subject="Throttle sınırı aşıldı",
    #        message="Kullanıcı throttle sınırını aştı. Dakikada en çok 7 istek yapılabilir.",
    #        from_email="abcde@gmail.com",
    #        recipient_list=["örnek@gmail.com", "example@gmail.com"]
    #    )
    
    
    # Bizim senaryomuza göre eğer gelen istek localhost yani ana makineden geliyorsa
    # rate parametresini geçersiz kılıyoruz. Yani kullanıcı istediği kadar istek gönderebilir. 
    # Fakat istek ana makineden gelmiyorsa bu sefer rate parametresi aktif hale geliyo ve 
    # kullanıcı eğer dakikada 7 istekten fazla istek yapıyorsa kullanıcıya uyarı mesajı dönüyor.
    
    #def allow_request(self, request, view):
    # Örnek: Belirli bir IP adresi için sınırsız erişim sağlama
        #if self.get_ident(request) == "127.0.0.1":
            #return True
        #return super().allow_request(request, view) 
    

    # Kullanıcının yaptığı her isteği throttle_log.txt adlı dosyaya kaydediyoruz
    # ve kullanıcı eğer dakikada 7 istekten daha fazla istek yaparsa bir dakika süre ile 
    # kullanıcının istek yapabilmesini kısıtlıyoruz

    def throttle_success(self): 
        self.history.insert(0, self.now)
        readable_time = datetime.fromtimestamp(self.now).strftime("%Y-%m-%d %H:%M:%S")
        
        with open("throttle_log.txt", "a") as log_file:
            log_file.write(f"Basarili istek: {readable_time}, Anahtar: {self.key} Gecmis: {self.history}\n")
        
        self.cache.set(self.key, self.history, self.duration)  
        return True









class CustomUserRateThrottle(UserRateThrottle):
    rate = "3/minute" # Anonim yada oturum açmış kullanıcılar için dakikada 3 istek sınırı
    
    def allow_request(self, request, view):
        # Admin kullanıcıları throttling'den muaf tutuyoruz
        # yani admin kullanıcılar istedikleri kadar istek yapabilir
        if request.user.is_staff:
            return True
        return super().allow_request(request, view)
    
    # Anonim yada oturum açmış kullanıcı yada kullanıcılar dakikada 3 ten fazla istek gönderdiğinde
    # ilgili kullanıcı yada kullanıcılara eposta gönderiyoruz

    #def throttle_failure(self):
    #    send_mail(
    #        subject="İstek sınırı aşıldı",
    #        message="Çok fazla istek yaptınız. Daha sonra tekrar deneyiniz.",
    #        from_email="abcde@gmail.com",
    #        recipient_list=["deneme@gmail.com"]
    #    )









class CustomScopedRateThrottle(ScopedRateThrottle):
    
    def allow_request(self, request, view):
        
        # Admin ve oturum açmış kullanıcıları her zaman throttling'den muaf tutuyoruz
        if request.user.is_authenticated:
            izin_verildi = True
        
        else:
        
            # Anonim kullanıcılar için belirli bir zaman diliminde throttling muafiyeti uyguluyoruz
            current_time = datetime.now().time() # Şu anki saati alıyoruz

            # Anonim kullanıcıların throttling'den muaf olma zamanını 12:30 ile 13:30 arası olarak belirliyoruz
            if current_time >= datetime.strptime("12:30", "%H:%M").time() and current_time <= datetime.strptime("13:30", "%H:%M").time():
                izin_verildi = True
            
            else:
                izin_verildi = super().allow_request(request, view)
        
        self.log_usage(request, izin_verildi)

        return izin_verildi
    


    def log_usage(self, request, izin):
        
        user = request.user if request.user.is_authenticated else "Anonim"
        
        if izin:
            print(f"Kullanıcı {user} isteği başarılı")
        else:
            print(f"Kullanıcı {user} hız sınırını aştı")
        
        # Terminale yazdırdığımız çıktıları bir de txt dosyasına kaydediyoruz
        if izin:
            log_message = f"{datetime.now()}: Kullanıcı {user} isteği başarılı\n\n"
        else:
            log_message = f"{datetime.now()}: Kullanıcı {user} hız sınırını aştı\n\n"

        # Log mesajını bir txt dosyasına yazıyoruz
        with open("throttle_log_2.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_message)

         
    
    
    
    def wait(self):
        
        wait_time = super().wait() # Bekleme süresini hesaplıyoruz
        print(f"Kalan bekleme süresi: {wait_time} saniye")
        
        # Kullanıcı istek sınırını aştığında eposta gönderelim
        self.eposta_gönder(wait_time)

        # Bekleme süresi bitene kadar bekleyelim
        time.sleep(wait_time)
        
        # Bekleme süresi bitince kullanıcıya bir eposta gönderiyoruz
        self.eposta_gönder("Bekleme süreniz bitmiştir, artık istek yapabilirsiniz...")
        return wait_time
    
    
    
    def eposta_gönder(self, kalan_süre):
        
        if isinstance(kalan_süre, str):
            mesaj = kalan_süre # Bekleme süresi bittiğinde gelen mesaj
        
        else:
            # İstek sınırı aşıldığında kullanıcıya kalan süreyi bildiren mesaj
            mesaj = f"İstek sınırını aştınız. {int(kalan_süre)} saniye bekledikten sonra tekrar deneyiniz."
        
        send_mail(
            subject="İstek sınırına ulaşıldı",
            message=mesaj,
            from_email="abcde@gmail.com",
            recipient_list=["örnekexample@gmail.com"]
        )
    

    
    # Bu metod istek sayısını ve süreyi döndürür
    def parse_rate(self, rate):
        istek_sayisi, süre = super().parse_rate(rate)
        print(f"İstek sınırı : {istek_sayisi} istek / {süre} saniye")
        return istek_sayisi, süre
    
    
   
    

    


