from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from pprint import pprint


# Eğer kullanıcı admin statüsünde ise her türlü işleme izin veriyoruz
# ama admin statüsünde değilse sadece görüntüleyebilmesine izin veriyoruz

class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin



# Eğer yorumun sahibi ile oturumu açan kullanıcı aynı kişi ise ilgili kullanıcının kendi yorumu ile ilgili güncelleme ve silme
# işlemlerine izin veriyoruz ama yorumun sahibi ile oturumu açan kullanıcı aynı kişi değilse
# bu sefer gelen metod örneğin bir get metodu ise sadece yorumu görüntüleyebilmesine izin veriyoruz
class IsYorumSahibiOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.yorum_sahibi


        
        

