from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


# PageNumberPagination sınıfını miras alarak özel pagination sınıfı yazıyoruz

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'sayfa'
    invalid_page_message = 'Geçersiz bir sayfa numarası girdiniz'
    



# LimitOffsetPagination sınıfını miras alarak özel pagination sınıfı yazıyoruz

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 25
    limit_query_param = "adet"
    offset_query_param = "baslangic_kaydi"




# CursorPagination sınıfını miras alarak özel pagination sınıfı yazıyoruz

class CustomCursorPagination(CursorPagination):
    ordering = "-isim"
    page_size = 20
    cursor_query_param = "imlec"
    invalid_cursor_message = "Geçersiz imleç. Lütfen geçerli bir imleç kullanın.."
    



