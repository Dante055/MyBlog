from urllib import quote_plus

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.urlresolvers import reverse

from .forms import PostForm
from .models import Post


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active() # filter(draft=False).filter(publish__lte=timezone.now())#.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 5) # Show 10 contacts per page
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
        "title": "Underground",
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
    if instance.user == request.user:
        delete = True
    else:
        delete = False
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        'title': 'Detail',
        'delete': delete
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
    # instance = get_object_or_404(Post, slug=slug)
    # instance.delete()
    # messages.success(request, "Successfully deleted")
    # return redirect("posts:list")
    # # return HttpResponse("<h1>Delete</h1>")

    try:
        # obj = Post.objects.get(slug=slug)
        obj = get_object_or_404(Post, slug=slug)
    except:
        raise Http404
    # instance = get_object_or_404(Post, slug=slug)
    if obj.user != request.user:
        # messages.success(request, "You do not have permission to view this.")
        # raise Http404
        reponse = HttpResponse("You do not have permission to do this.")
        reponse.status_code = 403
        return reponse
    # return render(request, "confirm_delete.html", context, status_code=403)

    if request.method == "POST":
        # parent_obj_url = obj.get_absolute_url()
        obj.delete()
        messages.success(request, "Successfully deleted")
        return HttpResponseRedirect(reverse('posts:list'))
    context = {
        "object": obj
    }
    return render(request, "confirm_delete.html", context)
