from django.http import HttpRequest
from django.shortcuts import redirect, render

from lists.models import Item, List


def home_page(request: HttpRequest):
    return render(request, 'home.html')


def view_list(request: HttpRequest):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request: HttpRequest):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST.get('item_text'), list=list_)
    return redirect('/lists/only-list')