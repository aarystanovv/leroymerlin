from django.db.models import Count

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.views import View
from .models import Product, Customer, ItemTable
from .forms import CustomerProfileForm, CustomerRegistrationForm, ProductForm, CustomerUpdate, ItemForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from app.forms import contactformemail
from django.core.mail import send_mail


def home(request):
    return render(request, "app/home.html")


def about(request):
    return render(request, "app/about.html")


def contact(request):
    return render(request, "app/contact.html")


class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())


class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html", locals())


class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/customerregistration.html', locals())

    def signup(self, request):
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            email = request.POST["email"]

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            login(request, user)
            subject = 'Welcome to Leroy Merlen'
            message = f'Hi {user.username}, thank you for registering in site.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return redirect("app/home.html")
        return render(request, "app/customerregistration.html", locals())


def delete_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Product, id=id)
    product = Product.objects.get(id=id)

    if request.method == "POST":
        obj.delete()

        return HttpResponseRedirect("/")

    return render(request, "app/delete_view.html", locals())


def contactsendmail(request):
    if request.method == "GET":
        form = contactformemail()
    else:
        form = contactformemail(request.POST)
        if form.is_valid():
            frommail = form.cleaned_data['fromemail']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject, message, frommail, ['ttt.arystan@gmail.com', frommail])
    return render(request, 'app/Contactpage.html', {'form': form})


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state,
                           zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        return render(request, 'app/profile.html', locals())


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())


class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")


class ProductView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'app/create_view.html', locals())

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            selling_price = form.cleaned_data['selling_price']
            discounted_price = form.cleaned_data['discounted_price']
            description = form.cleaned_data['description']
            composition = form.cleaned_data['composition']
            prodapp = form.cleaned_data['prodapp']
            category = form.cleaned_data['category']
            product_image = form.cleaned_data['product_image']

            reg = Product(title=title, selling_price=selling_price, discounted_price=discounted_price,
                          description=description, composition=composition, prodapp=prodapp,
                          category=category, product_image=product_image)
            reg.save()
            messages.success(request, "Congratulations! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        return redirect("address")


# def upload_image(request):  # new
#     context = {}
#     form = ProductForm(request.POST or None)
#
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#
#         context['form'] = form
#     return render(request, 'app/create_view.html', context)


class updateProduct(View):
    def get(self, request, pk):
        add = Product.objects.get(pk=pk)
        form = ProductForm(instance=add)
        return render(request, 'app/update_view.html', locals())

    def post(self, request, pk):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            add = Product.objects.get(pk=pk)
            add.title = form.cleaned_data['title']
            add.selling_price = form.cleaned_data['selling_price']
            add.discounted_price = form.cleaned_data['discounted_price']
            add.description = form.cleaned_data['description']
            add.composition = form.cleaned_data['composition']
            add.prodapp = form.cleaned_data['prodapp']
            add.category = form.cleaned_data['category']
            add.product_image = form.cleaned_data['product_image']
            add.save()
            messages.success(request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")


class edit_profile(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerUpdate(instance=add)
        return render(request, 'app/edit_user.html', locals())

    def post(self, request, pk):
        form = CustomerUpdate(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.user = form.cleaned_data['user']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")

def AdminUser(request):
    return render(request, 'app/AdminUser.html')


def allForClients(request):
    context = {
        "allForClientsItems": ItemTable.objects.all()
    }
    return render(request, 'app/allForClients.html', context)


def all(request):
    context = {
        "allForClientsItems": ItemTable.objects.all()
    }
    return render(request, 'app/all.html', context)

def allUsers(request):
    context = {
        "allForUsers": User.objects.all()
    }
    return render(request, 'app/allUsers.html', context)


def insert(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/all")
    else:
        form = ItemForm()
    return render(request, 'app/media.html', {'form': form})


def insertUsers(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/allUsers")
    else:
        form = CustomerRegistrationForm()
    return render(request, 'app/insertUserMedia.html', {'form': form})


def allEdit(request):
    context = {
        "allForClientsItems": ItemTable.objects.all()
    }
    return render(request, 'app/allEdit.html', context)




def updateItems(request, pk):
    if pk is not None:
        items = get_object_or_404(ItemTable, pk=pk)
    else:
        items = None

    if request.method == "POST":
        form = ItemForm(request.POST, instance=items)
        if form.is_valid():
            updated_items = form.save()
            return render(request, "app/AdminUser.html")
    else:
        form = ItemForm(instance=items)

    return render(request, "app/Update.html",
                  {"form": form, "instance": items, "model_type": "Item"})

def deleteItems(request, pk=None):
    context = {}
    if pk is not None:
        items = get_object_or_404(ItemTable, pk=pk)
    else:
        items = None

    if  request.method == "POST":
        items.delete()
        return HttpResponseRedirect('/allForClients')

    return render(request,'app/delete.html', context)


def profile(request):
    return render(request, 'app/profile1.html')

def edit(request, pk):
    context = {}
    obj = get_object_or_404(User, pk=pk)
    form = CustomerRegistrationForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return render(request, 'app/home.html')
    context["form"] = form

    return render(request, "app/edit.html", context)



def UU(request):
    context = {
        "allForUsers": User.objects.all()
    }
    return render(request, 'app/UU.html', context)


def updateOnlyUser(request, pk=None):
    context = {}
    if pk is not None:
        user = get_object_or_404(User, pk=pk)
    else:
        user = None

    if  request.method == "POST":
        user.delete()
        return HttpResponseRedirect('/allUsers')

    return render(request,'app/delete.html', context)


def detail(request, id):
    context = {}
    context["data"] = ItemTable.objects.get(id=id)
    data = ItemTable.objects.get(id=id)

    if request.user.is_authenticated:
        max_viewed_item_length = 10
        viewed_items = request.session.get('viewed_items', [])
        viewed_item = data.id, data.name
        if viewed_item in viewed_items:
            viewed_items.pop(viewed_items.index(viewed_item))
        viewed_items.insert(0, viewed_item)
        viewed_items = viewed_items[:max_viewed_item_length]
        request.session['viewed_items'] = viewed_items

    return render(request, "app/detail.html", context)


def search_books(request):
    name = request.GET.get('name', "")
    data = ItemTable.objects.all().filter(name__contains=name).values()
    template = loader.get_template('app/search.html')

    context = {
        'data' : data,
        'name' : name
    }
    return render(request, "app/search.html", context)


def item_list(request):
    sort_option = request.GET.get('sort', 'asc')
    query = request.GET.get('q')

    if query and sort_option == 'asc':
        items = ItemTable.objects.filter(name__icontains=query)
        items = items.order_by('price')

    elif query and sort_option == 'desc':
        items = ItemTable.objects.filter(name__icontains=query)
        items = items.order_by('-price')
    else:
        items = ItemTable.objects.all()

    if sort_option == 'asc':
        items = items.order_by('price')
    elif sort_option == 'desc':
        items = items.order_by('-price')


    return render(request, 'app/allForClients.html', {'items': items, 'sort_option': sort_option, 'query': query})
