from django.urls import path
from kitaplar.api import views

urlpatterns = [
    path('kitaplar/', views.KitapListCreateAPIView.as_view(), name="kitap-listesi"),
    path('kitaplar/<int:pk>/', views.KitapDetailAPIView.as_view(), name="kitap-detayi"),
    path('kitaplar/<int:kitap_pk>/yorum_yap', views.YorumCreateAPIView.as_view(), name="yorum-yap"),
    path('yorumlar/<int:pk>', views.YorumDetailAPIView.as_view(), name="yorum-detayi"),
    path('yorumlar/', views.YorumListAPIView.as_view(), name="yorumlar"),
] 
