from django.urls import path

from .views import ProductDetailView, ProductListView, CatalogPageView, CreateProductView, BuyView, EditView, PurchaseMadeView, CreateCategoryView

app_name = "products"

urlpatterns = [
    path("catalog/", CatalogPageView.as_view(), name="catalog"),
    path("catalog/edit/<slug:slug>/", EditView.as_view(template_name = "edit.html"), name="edit"),
    path("catalog/createproduct/", CreateProductView.as_view(), name="createproduct"),
    path("catalog/createcategory/", CreateCategoryView.as_view(), name="createcategory"),
    path("", ProductListView.as_view(), name="list"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="detail"),
    path("category/<slug:slug>/", ProductListView.as_view(), name="list_by_category"),
    path("<slug:slug>/buy/", BuyView.as_view(template_name = "buy.html"), name="buy"),
    path("<slug:slug>/buy/purchasemade/", PurchaseMadeView.as_view(template_name = "purchasemade.html"), name="purchasemade"),
]