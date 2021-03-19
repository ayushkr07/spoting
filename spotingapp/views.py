from django.shortcuts import render,redirect
from .models import List
from .forms import ListForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):
    all_items = List.objects.filter(user=request.user)
    return render(request,'spotingapp/index.html',{'all_items': all_items})

@login_required
def delete(request,list_id):
    item=List.objects.get(pk=list_id)
    item.delete()
    messages.success(request,('Item deleted!'))
    return redirect('index')

@login_required
def cross(request,list_id):
    item=List.objects.get(pk=list_id)
    item.completed=True
    item.save()
    return redirect('index')

@login_required
def un_cross(request,list_id):
    item=List.objects.get(pk=list_id)
    item.completed=False
    item.save()
    return redirect('index')

@login_required
def create(request):
    if request.method=='POST':
        form=ListForm(request.POST)
        if form.is_valid:
            list=form.save(commit=False)
            list.user=request.user
            list.save()
            return redirect('index')
    else:
        form=ListForm()
        return render(request,'spotingapp/addList.html',{'form':form})

@login_required
def edit(request,list_id):
    if request.method=='POST':
        item=List.objects.get(pk=list_id)
        form=ListForm(request.POST or None,instance=item)
        if form.is_valid:
            form.save()
            messages.success(request,('Item Edited!'))
            return redirect('index')
    else:
        item=List.objects.get(pk=list_id)
        return render(request,'spotingapp/edit.html',{'item' :item})

