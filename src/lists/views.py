from django.http import HttpRequest
from django.shortcuts import redirect, render

from lists.forms import ExistingListItemForm, ItemForm
from lists.models import List


def home_page(request: HttpRequest):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request: HttpRequest, list_id: int):
    our_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=our_list)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=our_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(our_list)
    return render(request, 'list.html', {'list': our_list, 'form': form})


def new_list(request: HttpRequest):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        return render(request, 'home.html', {'form': form})


def my_lists(request: HttpRequest, email: str):
    return render(request, 'my_lists.html')