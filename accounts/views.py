from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, ListView
from accounts.forms import ProfileForm, UserForm
from accounts.models import Profile
from django.contrib.auth import get_user_model

from products.models import Category

User = get_user_model()

class ProfileView(ListView):
    model = Profile
    template_name = "components/profile.html"

    def get_queryset(self):
        qs = super(ProfileView, self).get_queryset()
        # qs= qs.filter(user_id=self.kwargs['pk'])
        qs = qs.filter(user=self.request.user)
        print("qs====", qs)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['category_list'] = Category.objects.all()
        print("context======",context)
        return context


@login_required()  # only logged in users should access this
def edit_user(request, pk):
    # querying the User object with pk from url
    user = User.objects.get(pk=pk)

    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserForm(instance=user)

    # The sorcery begins from here, see explanation below
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