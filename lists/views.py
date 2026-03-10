from django.shortcuts import redirect, render
from django.http import HttpRequest

from lists.models import Item


def home_page(request: HttpRequest):
    if request.method == "POST":
        Item.objects.create(text=request.POST.get('item_text'))
        return redirect('/')

    return render(request, "home.html", {'items': Item.objects.all()})
