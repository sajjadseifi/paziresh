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


class MainViewBattalionGroup(View):
    def get(self, request):
        grohan = battalion_group.objects.filter().all()
        cx = {'grohan': grohan, }
        return render(request, 'battalions/grohan_list.html', cx)
