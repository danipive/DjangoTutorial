from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django import forms
from django.shortcuts import render, redirect
from .models import Product 

# Create your views here.
def homePageView(request):
    return HttpResponse("testing")

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        "title": "About us - Online Store",
        "subtitle": "About us",
        "author": "Developed by: Daniel Pineda",
        })

        return context
    
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        "telefono":"3136895005",
        "correo":"ejemplo@eafit.edu.co",
        "dirección":" Carrera 49, Cl. 7 Sur #50, Medellín, Antioquia"        
        })

        return context
    


class ProductIndexView(View):
    template_name = 'products/index.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()
        return render(request, self.template_name, viewData)
    
class ProductShowView(View):
    template_name = 'products/show.html'
    def get(self, request, id):
        viewData = {}
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except:
            return HttpResponseRedirect(reverse('home'))
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product
        
        return render(request, self.template_name, viewData)
        
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Products - Online Store'
        context['subtittle'] = 'List of products'
        return context
    

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price']

    def clean_price(self):
        price = self.cleaned_data['price']
        if (price <= 0):
            raise forms.ValidationError("Price must be greater than zero")
        return price
    

class ProductCreateView(View):
    template_name = 'products/create.html'
    created_product = 'products/create_product.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    def post(self, request):
        form = ProductForm(request.POST)
        viewData = {}
        viewData["form"] = form.data
        print(form.data)
        if form.is_valid():
            form.save()
            return render(request,self.created_product,viewData)
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)