from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import Post
from .forms import PostForm


def post_list(request):
    queryset = Post.objects.all()
    context = {
        'object_list': queryset,
        'title': "List"
    }
    return render(request, "index.html", context)
    # return HttpResponse("<h1>List</h1>")


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
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
        'title': 'Detail',
        'post_title': instance.title,
        'instance': instance
    }
    return render(request, "post_detail.html", context)
    # return HttpResponse("<h1>Detail</h1>")


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': 'Edit',
        'post_title': instance.title,
        'instance': instance,
        'form':form
    }
    return render(request, 'post_form.html', context)

    # return HttpResponse("<h1>Update</h1>")


def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")
