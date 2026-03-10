from django.http import HttpRequest
from django.shortcuts import redirect, render

from lists.models import Item


def home_page(request: HttpRequest):
    if request.method == 'POST':
        Item.objects.create(text=request.POST.get('item_text'))
        return redirect('/lists/only-list')

    return render(request, 'home.html')


def view_list(request: HttpRequest):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})