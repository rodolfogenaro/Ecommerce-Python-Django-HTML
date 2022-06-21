from django.urls import path

from .views import AdminPageView
#from ..products.views import ProductDetailView, ProductListView

app_name = "users"

urlpatterns = [
    #path("admin/", AdminPageView.as_view(), name="admin"),
]