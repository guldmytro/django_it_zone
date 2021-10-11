from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import csv
from .utils import get_csv_header, get_attributes_header, get_product_row, push_products
from catalog.models import Product, Attribute
from .forms import CsvForm


@login_required(login_url='/admin/')
def products_upload(request):
    form = CsvForm()
    return render(request, 'uploads/detail.html', {'form': form})


@login_required(login_url='/admin/')
def products_fetch(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=products.csv'
    writer = csv.writer(response)
    basic_header = get_csv_header()
    attributes_header = get_attributes_header()
    writer.writerow(basic_header + attributes_header)
    products = Product.objects.all()
    attributes = Attribute.objects.all()
    for product in products:
        writer.writerow(get_product_row(product, attributes, request))
    return response


@login_required(login_url='/admin/')
def products_add(request):
    if request.method == 'POST':
        form = CsvForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.save()
            form = CsvForm()
            push_products(csv_file.file.path, request)
            return render(request, 'uploads/detail.html', {'form': form, 'result': 'Отработано'})
    form = CsvForm()
    return render(request, 'uploads/detail.html', {'form': form})

