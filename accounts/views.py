import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from accounts.forms import ProfileForm, UserForm
from accounts.models import Profile, Address, Shop
from django.contrib.auth import get_user_model

from orders.models import Order, Payment
from products.models import Category, ShopProduct
from siteview.views import get_all_context

User = get_user_model()

class ProfileView(ListView):
    model = Profile
    template_name = "components/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['category_list'] = Category.objects.all()
        context['addresses'] = Address.objects.filter(user=self.request.user)
        context['payments'] = Payment.objects.filter(user=self.request.user)
        print("context======",context)
        form = ProfileForm()
        context["form"]: form
        return context


@csrf_exempt
def edit_profile(request):
    data = json.loads(request.body)
    user = request.user
    try:
        print("user", user, "first_name", data['f_name'], "last_name", data['l_name'], "phone_number", data['ph_number'],"mobile_number",data['mob_number'])
        profile = Profile.objects.get(user=user)
        print("profile====================================================================",profile)
        profile.first_name=data['f_name']
        profile.last_name=data['l_name']
        profile.phone_number= data['ph_number']
        profile.mobile_number=data['mob_number']
        profile.save()
        response = {"first_name": profile.first_name,
                    "last_name": profile.last_name, "phone_number": profile.phone_number, "mob_number": profile.mobile_number, }
        print(response)
        return HttpResponse(json.dumps(response), status='201')
    except:
        response = ["error"]
        print(response)
        return HttpResponse(json.dumps(response), status='400')


@csrf_exempt
def edit_address(request):
    data = json.loads(request.body)
    user = request.user
    print("user", user, "city", data['city'], "street", data['street'], "allay", data['allay'], "zip_code",
          data['zip_code'])

    try:
        try:
            print("user", user, "city", data['city'], "street", data['street'], "allay", data['allay'],"zip_code",data['zip_code'])
            address = Address.objects.get(user=user, id=data['address_id'])
            print("address===========================================================", address)
            address.city=data['city']
            address.street=data['street']
            address.allay= data['allay']
            address.zip_code=data['zip_code']
            address.save()
            response = {"city": address.city,
                        "street": address.street, "allay": address.allay, "zip_code": address.zip_code, }
            print(response)
            return HttpResponse(json.dumps(response), status='201')
        except:
            print('injaaa')
            address = Address.objects.create(user=user,city=data['city'],street=data['street'],allay=data['allay'],zip_code=data['zip_code'])
            address.save()
            response = {"city": address.city,
                        "street": address.street, "allay": address.allay, "zip_code": address.zip_code, }
            print(response)
            return HttpResponse(json.dumps(response), status='201')
    except:
        # profile = Profile.objects.create(user=user, first_name=data['f_name'], last_name=data['l_name'],
        #                                  phone_number=data['ph_number'], mobile_number=data['mob_number'])
        response = ["error"]
        print(response)
        return HttpResponse(json.dumps(response), status='400')


@login_required
def update_avatar(request):
    form = ProfileForm()
    user=request.user
    profiles = Profile.objects.all()
    categories = Category.objects.all()
    users = User.objects.all()
    profile = Profile.objects.get(user=user)
    context = {
        "form": form,
        "Profiles": profiles,
        "categories": categories,
        "users": users,
    }
    if request.method == 'POST':
        print("----------------------------------POST")
        form = ProfileForm(request.POST, request.FILES)
        print(form)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            avatar = form.cleaned_data.get("avatar")
            # profile = form.save()

            profile = Profile.objects.get(user=user)
            profile.avatar = avatar
            profile.save()
            print("--------------------------------------------profile image save", profile)
            return redirect('profile',pk=profile.id)

        else:
            context['form'] = form
            return redirect('profile',pk=profile.id)
    else:
        print("----------------------------------Get")
        return redirect('profile',pk=profile.id)


class ShopView(ListView):
    model = Shop
    template_name = 'components/shops.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = get_all_context(request=self.request)
        context2.update(context)
        return context2

class ShopDetailView(DetailView):
    model = Shop
    template_name = 'components/shop2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = get_all_context(request=self.request)
        shop = context['shop']
        shop_products = ShopProduct.objects.filter(shop__slug=shop.slug)
        print('*****************************************    ',shop_products)
        context['shop_products'] = shop_products
        context2.update(context)
        return context2


@login_required()  # only logged in users should access this
def edit_user(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserForm(instance=user)
    ProfileInlineFormset = inlineformset_factory(User, Profile,
                                                 fields=('first_name', 'last_name', 'address', 'phone_number', 'mobile_number','avatar',))
    formset = ProfileInlineFormset(instance=user)
    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/accounts/profile/')

        return render(request, "components/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied