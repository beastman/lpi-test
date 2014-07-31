from django.shortcuts import render
from shop.models import Product
from shop.forms import ProductFilterForm


# Create your views here.
def home(request):
    if request.method == 'POST':
        filter_form = ProductFilterForm(request.POST)
        products = Product.objects.all()
        if filter_form.is_valid():
            products = products.filter(trademark__in=filter_form.cleaned_data['trademarks'])
            products = products.filter(category__in=filter_form.cleaned_data['categories'])
            products = products.filter(price__gte=filter_form.cleaned_data['price_min'],
                                       price__lte=filter_form.cleaned_data['price_max'])
            products = products.filter(in_stock_count__gte=filter_form.cleaned_data['min_stock'])
    else:
        filter_form = ProductFilterForm()
        products = Product.objects.all()
    context = {
        'products': products,
        'filter_form': filter_form,
    }
    return render(request, 'home.html', context)