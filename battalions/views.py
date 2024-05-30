from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import battalion, battalion_group
from django.views import View
from django.urls import reverse_lazy
from .forms import *


# Create your views here.


class MainViewBattalion(LoginRequiredMixin, View):
    def get(self, request):
        gordan = battalion.objects.filter().all()
        cx = {'gordan': gordan, }
        return render(request, 'battalions/gordan_list.html', cx)


class BattalionCreate(LoginRequiredMixin, View):
    template = 'battalions/gordan_form.html'
    success_url = reverse_lazy('all-Battalion')

    def get(self, request):
        b_form = BattalionForm()
        cx = {'form': b_form}
        return render(request, self.template, cx)

    def post(self, request):
        b_form = BattalionForm(request.POST, request.FILES or None)
        if not b_form.is_valid():
            cx = {'form': b_form}
            return render(request, self.template, cx)
        my_battalion = battalion()
        my_battalion.name = b_form.cleaned_data['name']
        my_battalion.order = b_form.cleaned_data['order']
        my_battalion.is_active = b_form.cleaned_data['is_active']

        my_battalion.save()
        return redirect(self.success_url)


class BattalionUpdate(LoginRequiredMixin, View):
    template = 'battalions/gordan_form.html'
    success_url = reverse_lazy('all-Battalion')

    def get(self, request, pk):
        my_battalion = battalion.objects.filter(pk=pk).first()
        b_form = BattalionForm()
        b_form.initial['name'] = my_battalion.name
        b_form.initial['order'] = my_battalion.order
        b_form.initial['is_active'] = my_battalion.is_active
        cx = {'form': b_form}
        return render(request, self.template, cx)

    def post(self, request, pk):
        my_battalion = battalion.objects.filter(pk=pk).first()
        b_form = BattalionForm(request.POST, request.FILES or None)
        if not b_form.is_valid():
            cx = {'form': b_form}
            return render(request, self.template, cx)
        my_battalion.name = b_form.cleaned_data['name']
        my_battalion.order = b_form.cleaned_data['order']
        my_battalion.is_active = b_form.cleaned_data['is_active']
        my_battalion.save()
        return redirect(self.success_url)


class MainViewBattalionGroup(LoginRequiredMixin, View):
    def get(self, request):
        grohan = battalion_group.objects.filter().all()
        cx = {'grohan': grohan, }
        return render(request, 'battalions/grohan_list.html', cx)


class CreateBattalionGroup(View):
    template = 'battalions/grohan_form.html'
    success_url = reverse_lazy('MainViewBattalionGroup')

    def get(self, request):
        bg_f = BattalionGroupForm()
        bt_list = []
        my_bt = battalion.objects.filter().all()
        for item in my_bt:
            bt_list.append((item.id, item.name))
        bg_f.fields['gordan'].choices = bt_list
        cx = {'form': bg_f}
        return render(request, self.template, cx)

    def post(self, request):
        bg_f = BattalionGroupForm(request.POST, request.FILES or None)
        bt_list = []
        my_bt = battalion.objects.filter().all()
        for item in my_bt:
            bt_list.append((item.id, item.name))
        bg_f.fields['gordan'].choices = bt_list
        if not bg_f.is_valid():
            cx = {'form': bg_f}
            return render(request, self.template, cx)
        bg = battalion_group()
        bg.name = bg_f.cleaned_data['name']
        gordan_id = bg_f.cleaned_data['gordan']
        gordan = battalion.objects.filter(pk=gordan_id).first()
        bg.gordan = gordan
        bg.zirediplom = bg_f.cleaned_data['zirediplom']
        bg.diplom = bg_f.cleaned_data['diplom']
        bg.ofghdiplom = bg_f.cleaned_data['ofghdiplom']
        bg.lisans = bg_f.cleaned_data['lisans']
        bg.ofghlisans = bg_f.cleaned_data['ofghlisans']
        bg.doctra = bg_f.cleaned_data['doctra']
        bg.shie = bg_f.cleaned_data['shie']
        bg.ahle_tasnon = bg_f.cleaned_data['ahle_tasnon']
        bg.zarfiat = bg_f.cleaned_data['zarfiat']
        bg.salemm = bg_f.cleaned_data['salemm']
        bg.takmilzarmit = bg_f.cleaned_data['takmilzarmit']
        bg.moafazrazm = bg_f.cleaned_data['moafazrazm']
        bg.moafazrazm_gorehbe = bg_f.cleaned_data['moafazrazm_gorehbe']
        bg.gorehbe = bg_f.cleaned_data['gorehbe']
        bg.order = bg_f.cleaned_data['order']
        bg.save()
        return redirect(self.success_url)


class BattalionGroupUpdate(View):
    template = 'battalions/grohan_form.html'
    success_url = reverse_lazy('MainViewBattalionGroup')

    def get(self, request, pk):
        bg_f = BattalionGroupForm()
        bg = battalion_group.objects.filter(pk=pk).first()
        bt_list = []
        my_bt = battalion.objects.filter().all()
        for item in my_bt:
            bt_list.append((item.id, item.name))
        bg_f.initial['name'] = bg.name
        bg_f.fields['gordan'].choices = bt_list
        bg_f.fields['gordan'].initial = bg.gordan.id
        bg_f.initial['zirediplom'] = bg.zirediplom
        bg_f.initial['diplom'] = bg.diplom
        bg_f.initial['ofghdiplom'] = bg.ofghdiplom
        bg_f.initial['lisans'] = bg.lisans
        bg_f.initial['doctra'] = bg.doctra
        bg_f.initial['shie'] = bg.shie
        bg_f.initial['ahle_tasnon'] = bg.ahle_tasnon
        bg_f.initial['zarfiat'] = bg.zarfiat
        bg_f.initial['takmilzarmit'] = bg.takmilzarmit
        bg_f.initial['order'] = bg.order
        bg_f.initial['salemm'] = bg.salemm
        bg_f.initial['moafazrazm'] = bg.moafazrazm
        bg_f.initial['moafazrazm_gorehbe'] = bg.moafazrazm_gorehbe
        bg_f.initial['gorehbe'].gorehbe = bg.gorehbe
        cx = {'form': bg_f}
        return render(request, self.template, cx)

    def post(self, request, pk):
        bg_f = BattalionGroupForm(request.POST, request.FILES or None)
        bg = battalion_group.objects.filter(pk=pk).first()
        bt_list = []
        my_bt = battalion.objects.filter().all()
        for item in my_bt:
            bt_list.append((item.id, item.name))
        bg_f.fields['gordan'].choices = bt_list
        bg_f.fields['gordan'].initial = bg.gordan.id
        if not bg_f.is_valid():
            cx = {'form': bg_f}
            return render(request, self.template, cx)
        bg.name = bg_f.cleaned_data['name']
        gordan_id = bg_f.cleaned_data['gordan']
        gordan = battalion.objects.filter(pk=gordan_id).first()
        bg.gordan = gordan
        bg.zirediplom = bg_f.cleaned_data['zirediplom']
        bg.diplom = bg_f.cleaned_data['diplom']
        bg.ofghdiplom = bg_f.cleaned_data['ofghdiplom']
        bg.lisans = bg_f.cleaned_data['lisans']
        bg.ofghlisans = bg_f.cleaned_data['ofghlisans']
        bg.doctra = bg_f.cleaned_data['doctra']
        bg.shie = bg_f.cleaned_data['shie']
        bg.ahle_tasnon = bg_f.cleaned_data['ahle_tasnon']
        bg.zarfiat = bg_f.cleaned_data['zarfiat']
        bg.takmilzarmit = bg_f.cleaned_data['takmilzarmit']
        bg.order = bg_f.cleaned_data['order']
        bg.salemm = bg_f.cleaned_data['salemm']
        bg.moafazrazm = bg_f.cleaned_data['moafazrazm']
        bg.moafazrazm_gorehbe = bg_f.cleaned_data['moafazrazm_gorehbe']
        bg.gorehbe = bg_f.cleaned_data['gorehbe']
        bg.save()
        return redirect(self.success_url)
