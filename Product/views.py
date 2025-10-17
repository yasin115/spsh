from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from Product.forms import CommentForms
from django.core.paginator import Paginator
from Product.models import Product,Comment
from category.models import Category,Languages
from home.models import informationSite
def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return str(request.META.get('REMOTE_ADDR'))
def detail(request,string):
    Prod = get_object_or_404(Product,slug=string)
    ip_address = get_client_ip(request)
    
    if str(ip_address) not in str(Prod.viewc.all()):
        Prod.viewc.add(ip_address)
    languagess = Languages.objects.all()
    category = Category.objects.all()
    siteData = informationSite.objects.first()
    comment = Comment.objects.filter(product__slug=string)
    rec = Product.objects.filter(language__category__in=Prod.language.values('category')).exclude(id=Prod.id)
    if request.method == "POST":
        form = CommentForms(request.POST)
        if form.is_valid():
            if Comment.objects.filter(user=request.user).count() < 2:
                ex = Comment()
                ex.text = form.cleaned_data.get('text')
                ex.user = request.user
                ex.product = Product.objects.get(slug=string)
                ex.save()
            
            return redirect("product:detail",Prod.slug)
    else:
        form = CommentForms()

    context ={
        "string":Prod,
        "form":form,
        "category":category,
        "siteData":siteData,
        "lang":languagess,
        "co":comment,
        "rec":rec,
    }
    return render(request,"detail/course-detail.html",context)
def detail2(request,id):
    Prod = get_object_or_404(Product,id=id)
    rec = Product.objects.filter(language=Prod.language.first())
    if request.method == "POST":
        form = CommentForms(request.POST)
        if form.is_valid():
            if Comment.objects.filter(user=request.user).count() < 2:
                ex = Comment()
                ex.text = form.cleaned_data.get('text')
                ex.user = request.user
                ex.product = Product.objects.get(id=id)
                ex.save()
            return redirect('product:detail2',Prod.id)
    else:
        form = CommentForms()

    languagess = Languages.objects.all()
    category = Category.objects.all()
    comment = Comment.objects.filter(product__id=id)
    siteData = informationSite.objects.first()
    context ={
        "string":Prod,
        'form':form,
        "category":category,
        "siteData":siteData,
        "lang":languagess,
        "co":comment,
        "rec":rec,
    }
    return render(request,"detail/course-detail.html",context)

def all(request):
    languagess = Languages.objects.all()
    category = Category.objects.all()
    siteData = informationSite.objects.first()
    categoryname = Product.objects.all().filter(published=True)
    paginator = Paginator(categoryname, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={
        "category":category,
        "page":paginator,
        "category":category,
        "siteData":siteData,
        "lang":languagess,
        "categoryname":page_obj,

    }
    return render(request,"detail/all.html",context)
@login_required
def like(request,id):
    comid = Comment.objects.get(id=id)
    for a in comid.like.all():
        if a == request.user:
            comid.like.remove(request.user)
            break
    else:
        comid.like.add(request.user)
    return redirect('product:detail2',comid.product.id)
@login_required
def dislike(request,id):
    comid = Comment.objects.get(id=id)
    for a in comid.dislike.all():
        if a == request.user:
            comid.dislike.remove(request.user)
            break
    else:
        comid.dislike.add(request.user)
    return redirect('product:detail2',comid.product.id)