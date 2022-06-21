from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from .models import Category, Product, Order
from .forms import ProductsForm, OrdersForm, CategoriesForm


class CatalogPageView(TemplateView):
    template_name = "catalog.html"
    
    
    def get(self, request):
        product_list = Product.objects.all()
        args = {'product_list': product_list}
        return render(request, self.template_name, args)
    
    
    def post(self, request):
        form = ProductsForm(request.POST)
        #print(form.is_valid())
        #print ("Erro: ", form.errors, "\n\n")
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            pname = form.cleaned_data['product.name']
            form = ProductsForm()
            return redirect('products:catalog')
        
        product = Product.objects.get(name=pname)
        args = {'form': form, 'pname': pname}
        return render(request, self.template_name, args)
    
class EditView(DetailView):
    specific_product = None
    
    def get_queryset(self):
        queryset = Product.objects.all()

        product_slug = self.kwargs.get("slug")
        if product_slug:
            self.specific_product = get_object_or_404(Product, slug=product_slug)
            #print ("Produto: ", self.product, "\n\n")
            queryset = queryset.filter(slug=product_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["specific_product"] = self.specific_product
        context["category_list"] = Category.objects.all()
        return context
    
    def post(self, request, **kwargs):
        # def get_queryset(self):
        queryset = Product.objects.all()

        product_slug = self.kwargs.get("slug")
        if product_slug:
            self.specific_product = get_object_or_404(Product, slug=product_slug)
            #print ("Produto: ", self.product, "\n\n")
            queryset = queryset.filter(slug=product_slug)
        
        # def post() "comum"
        form = ProductsForm(request.POST, request.FILES)
        #print(form.is_valid())
        #print ("Erro: ", form.errors, "\n\n")
        if form.is_valid():
            aux_product = form.save(commit=False)
            self.specific_product.category = aux_product.category
            self.specific_product.name = aux_product.name
            if aux_product.image: #imagem nao mantem sozinha apos editar
                self.specific_product.image = aux_product.image
            self.specific_product.description = aux_product.description
            if aux_product.price: #preco nao mantem sozinha apos editar
                self.specific_product.price = aux_product.price
            self.specific_product.is_available = aux_product.is_available
            self.specific_product.save()
            text = form.cleaned_data['name']
            form = ProductsForm()
            return redirect('products:catalog')
        
        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)
    
class CreateProductView(TemplateView):
    template_name = "createproduct.html"
    
    def get(self, request):
        category_list = Category.objects.all()
        args = {'category_list': category_list}
        return render(request, self.template_name, args)
    
    def post(self, request):
        form = ProductsForm(request.POST, request.FILES)
        #print(form.is_valid())
        #print ("Erro: ", form.errors, "\n\n")
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            text = form.cleaned_data['name']
            form = ProductsForm()
            return redirect('products:catalog')
        
        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)
    
class CreateCategoryView(TemplateView):
    template_name = "createcategory.html"
    
    def get(self, request):
        category_list = Category.objects.all()
        args = {'category_list': category_list}
        return render(request, self.template_name, args)
    
    def post(self, request):
        form = CategoriesForm(request.POST)
        #print(form.is_valid())
        #print ("Erro: ", form.errors, "\n\n")
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            text = form.cleaned_data['name']
            form = CategoriesForm()
            return redirect('products:catalog')
        
        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)

class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    
class BuyView(DetailView):
    specific_product = None
    
    def get_queryset(self):
        queryset = Product.objects.all()

        product_slug = self.kwargs.get("slug")
        if product_slug:
            self.specific_product = get_object_or_404(Product, slug=product_slug)
            #print ("Produto: ", self.product, "\n\n")
            queryset = queryset.filter(slug=product_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["specific_product"] = self.specific_product
        return context
    
    def post(self, request, **kwargs):
        # def get_queryset(self):
        queryset = Product.objects.all()

        product_slug = self.kwargs.get("slug")
        if product_slug:
            self.specific_product = get_object_or_404(Product, slug=product_slug)
            #print ("Produto: ", self.product, "\n\n")
            queryset = queryset.filter(slug=product_slug)
        
        # def post() "comum"
        form = OrdersForm(request.POST)
        print(form.is_valid())
        print ("Erro: ", form.errors, "\n\n")
        if form.is_valid():
            order = form.save(commit=False)
            order.price = order.quantity*self.specific_product.price
            self.specific_product.is_available = self.specific_product.is_available - order.quantity
            self.specific_product.save()
            order.save()
            quantity = form.cleaned_data['quantity']
            form = OrdersForm()
            return redirect(self.specific_product.get_purchasemade_url())
        
        args = {'form': form, 'quantity': quantity}
        return render(request, self.template_name, args)

class PurchaseMadeView(DetailView):
    specific_order = None
    
    def get_queryset(self):
        queryset = Product.objects.all()

        product_slug = self.kwargs.get("slug")
        if product_slug:
            product_order = get_object_or_404(Product, slug=product_slug)
            #print (Order.objects.values_list('id', flat=True), "\n\n")
            max_id_order = Order.objects.values_list('id', flat=True).last()
            self.specific_order = Order.objects.get(id=max_id_order)
            queryset = queryset.filter(slug=product_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["specific_order"] = self.specific_order
        return context

class ProductListView(ListView):
    category = None
    paginate_by = 5

    def get_queryset(self):
        queryset = Product.objects.exclude(is_available=0)

        category_slug = self.kwargs.get("slug")
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["categories"] = Category.objects.all()
        return context