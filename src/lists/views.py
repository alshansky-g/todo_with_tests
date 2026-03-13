from django.forms import ValidationError
from django.http import HttpRequest
from django.shortcuts import redirect, render

from lists.models import Item, List


def home_page(request: HttpRequest):
    return render(request, 'home.html')


def view_list(request: HttpRequest, list_id: int):
    our_list = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(list=our_list, text=request.POST['item_text'])
            item.full_clean()
            item.save()
            return redirect(f'/lists/{our_list.id}')
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list': our_list, 'error': error})


def new_list(request: HttpRequest):
    list_ = List.objects.create()
    item = Item(text=request.POST.get('item_text'), list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(f'/lists/{list_.id}')
