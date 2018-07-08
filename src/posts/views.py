from urllib import quote_plus

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm
from .models import Post




def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active() # filter(draft=False).filter(publish__lte=timezone.now())#.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 10) # Show 10 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var,
        'today':today
    }

    return render(request, "post_list.html", context)
    # return HttpResponse("<h1>List</h1>")


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
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


def post_detail(request, slug=None):
    # instance = Post.objects.get(id=4)
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        'title': 'Detail'
    }
    return render(request, "post_detail.html", context)
    # return HttpResponse("<h1>Detail</h1>")


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
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


def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")
    # return HttpResponse("<h1>Delete</h1>")
