from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .forms import PostForm


def post_list(request):
    queryset = Post.objects.all()
    context = {
        'object_list': queryset,
        'title': "List"
    }
    return render(request, "post_list.html", context)
    # return HttpResponse("<h1>List</h1>")


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form,
        'title': 'Form'
    }
    return render(request, 'post_form.html', context)
    # return HttpResponse("<h1>Create</h1>")


def post_detail(request, id=None):
    # instance = Post.objects.get(id=4)
    instance = get_object_or_404(Post, id=id)
    context = {
        'post_title': instance.title,
        'instance': instance,
        'title': 'Detail'
    }
    return render(request, "post_detail.html", context)
    # return HttpResponse("<h1>Detail</h1>")


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Edited  ")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'post_title': instance.title,
        'instance': instance,
        'form':form,
        'title':'Edit'
    }
    return render(request, 'post_form.html', context)

    # return HttpResponse("<h1>Update</h1>")


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")
    # return HttpResponse("<h1>Delete</h1>")
