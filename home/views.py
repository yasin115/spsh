from hesab.models import User
from django.shortcuts import render
from home.models import informationSite
from Product.models import Product
# from blog.models import Blog
from category.models import Languages,Category
# Create your views here.
def home(request):
    siteinformation = informationSite.get_cached()
    product = Product.objects.filter(published=True)
    prodc = Product.objects.filter(published=True).count()
    language = Languages.objects.filter(status=True)
    category = Category.objects.filter(status=True)
    userCount = User.objects.count()
    products = Product.objects.all()[:6]
    # blog = Blog.objects.all()[:3]
    if request.POST:
        
        
        search_words = request.POST['search']
        searchResualt = Product.objects.filter(name__contains=search_words)
        context = {
            "text":search_words,
            "res":searchResualt,
            "siteData":siteinformation,
            "lang":language,
            "category":category,
        }
        return render(request,"main/searchHome.html",context)
    return render(request,"main/index.html",{
        "product":product,
        "siteData":siteinformation,
        "lang":language,
        "category":category,
        "userc":userCount,
        "prodc":prodc,
        "products":products,
        # "blog":blog,
        })
def about(request):
    return ""
def error404(request, exception):
    return render(request,"404.html")
def error500(request, exception):
    return render(request,"500.html")