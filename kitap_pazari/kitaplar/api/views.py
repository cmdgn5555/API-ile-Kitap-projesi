from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework import generics
from kitaplar.api.serializers import KitapSerializer, YorumSerializer
from kitaplar.models import Kitap, Yorum
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from kitaplar.api.permissions import IsAdminUserOrReadOnly, IsYorumSahibiOrReadOnly
from rest_framework.exceptions import ValidationError
from kitaplar.api.pagination import CustomPageNumberPagination, CustomLimitOffsetPagination, CustomCursorPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from kitaplar.api.throttling import CustomAnonRateThrottle, CustomUserRateThrottle, CustomScopedRateThrottle



# Concrete Views



# Tüm kitapları Listeleyip Kitap Oluşturuyoruz
class KitapListCreateAPIView(generics.ListCreateAPIView): 
    queryset = Kitap.objects.all().order_by('-id')
    serializer_class = KitapSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = CustomPageNumberPagination
    #pagination_class = CustomLimitOffsetPagination
    #pagination_class = CustomCursorPagination
    
    #throttle_classes = [AnonRateThrottle]
    #throttle_classes = [CustomAnonRateThrottle]
    #throttle_classes = [CustomScopedRateThrottle] 
    #throttle_scope = "kitap_listesi"




# Bir kitabı getiriyoruz güncelliyoruz yada siliyoruz
class KitapDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    
    #throttle_classes = [CustomAnonRateThrottle]
    #throttle_classes = [CustomScopedRateThrottle]
    #throttle_scope = "kitap_detayi"



# Bir kitap ile bağlantı kurarak o kitaba yorum yapıyoruz
class YorumCreateAPIView(generics.CreateAPIView):         
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        kitap_pk = self.kwargs.get('kitap_pk')
        kitap = get_object_or_404(Kitap, pk=kitap_pk)
        kullanici = self.request.user
        yorumlar = Yorum.objects.filter(kitap=kitap, yorum_sahibi=kullanici)
        if yorumlar.exists():
            raise ValidationError("Bir kullanıcı bir kitaba sadece bir yorum yapabilir")
        serializer.save(kitap=kitap, yorum_sahibi=kullanici)



# Bir yorumu getiriyoruz güncelliyoruz yada siliyoruz
class YorumDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializer
    permission_classes = [IsYorumSahibiOrReadOnly]
    
    


# Tüm yorumları listeliyoruz
class YorumListAPIView(generics.ListAPIView):
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializer
    
    #throttle_classes = [UserRateThrottle]
    #throttle_classes = [CustomUserRateThrottle]
    



    
    

    








# GenericAPIView ve Mixins Kullanımı

#class KitapListCreateAPIView(ListModelMixin, 
#                             CreateModelMixin, 
#                             GenericAPIView):
#    
#    queryset = Kitap.objects.all()
#    serializer_class = KitapSerializer
#
#    # Listele
#    def get(self, request, *args, **kwargs):
#        return self.list(request, *args, **kwargs) 
#
#
#    # Yarat
#    def post(self, request, *args, **kwargs):
#        return self.create(request, *args, **kwargs)
#
#
#
#class KitapDetailAPIView(RetrieveModelMixin, 
#                         UpdateModelMixin, 
#                         DestroyModelMixin, 
#                         GenericAPIView):
#    
#    queryset = Kitap.objects.all()
#    serializer_class = KitapSerializer
#
#    # Tek bir kaydı getir
#    def get(self, request, *args, **kwargs):
#        return self.retrieve(request, *args, **kwargs)
#    
#    
#    # Tek bir kaydı güncelle
#    def put(self, request, *args, **kwargs):
#        return self.update(request, *args, **kwargs)
#    
#    
#    # Tek bir kaydı sil
#    def delete(self, request, *args, **kwargs):
#        return self.destroy(request, *args, **kwargs)
