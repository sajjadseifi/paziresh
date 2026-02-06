from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import battalion, battalion_group,battalion_group_batch
from django.views import View
from django.urls import reverse_lazy
from .forms import *
from soldiers.models import Soldier
from django.contrib import messages
from ensani_soldires_management.utils import battalion_and_groups_allowed

class MainViewBattalion(LoginRequiredMixin, View):
    def get(self, request):
        gordan , _ = battalion_and_groups_allowed(request.user)
        gordan = gordan.order_by('-is_active','order')
        
        cx = { 'gordan': gordan }
        return render(request, 'battalions/gordan_list.html', cx)

class BattalionCreate(LoginRequiredMixin, View):
    template = 'battalions/gordan_form.html'
    success_url = reverse_lazy('all-Battalion')

    def get(self, request):
        b_form = BattalionForm()
        cx = {'form': b_form,'new':True }
        return render(request, self.template, cx)

    def post(self, request):
        form = BattalionForm(request.POST, request.FILES or None)
        if not form.is_valid():
            cx = {'form': form ,'new':True}
            return render(request, self.template, cx)
        b = battalion()
        b.name = form.cleaned_data['name']
        b.order = form.cleaned_data['order']
        b.is_active = form.cleaned_data['is_active']
        b.gcode = form.cleaned_data['gcode']
        b.commander = form.cleaned_data['commander']
        
        b.save()
        
        return redirect(self.success_url)


class BattalionUpdate(LoginRequiredMixin, View):
    template = 'battalions/gordan_form.html'
    success_url = reverse_lazy('all-Battalion')

    def get(self, request, pk):
        b = battalion.objects.filter(pk=pk).first()
        grohans = b.grohans if battalion else []

        form = BattalionForm()
        form.initial['name'] = b.name
        form.initial['order'] = b.order
        form.initial['is_active'] = b.is_active
        form.initial['gcode'] = b.gcode
        form.initial['commander'] = b.commander
        
        cx = {'form': form, 'grohans': grohans,'battalion':b }
        return render(request, self.template, cx)

    def post(self, request, pk):
        b = battalion.objects.filter(pk=pk).first()
        grohans = b.grohans if b else []

        form = BattalionForm(request.POST, request.FILES or None)

        if not form.is_valid():
            cx = { 'form': form, 'grohans': grohans,'battalion':b }
            return render(request, self.template, cx)

        b.name = form.cleaned_data['name']
        b.order = form.cleaned_data['order']
        b.is_active = form.cleaned_data['is_active']
        b.gcode = form.cleaned_data['gcode']
        b.commander = form.cleaned_data['commander']
    
        b.save()
        return redirect(self.success_url)


class MainViewBattalionGroup(LoginRequiredMixin, View):
    def get(self, request):
        _ , grohan = battalion_and_groups_allowed(request.user)
        grohan = grohan.order_by('gordan','name')
        cx = { 'grohan': grohan }
        return render(request, 'battalions/grohan_list.html', cx)

    def post(self, request):
        action = request.GET.get('action','')
        
        if action == 'cleanup' and request.method == 'POST':
            data = battalion_group.clean_data()
            battalion_group.objects.update(**data)

        return redirect(request.path)

class CreateBattalionGroup(View):
    template = 'battalions/grohan_form.html'
    success_url = reverse_lazy('MainViewBattalionGroup')

    def get(self, request):
        b = request.GET.get('battalion','')
        bg_f = BattalionGroupForm()
        bg_f.fields['status_types'].choices = Soldier.status_types_options()

        bt_list = []
        for item in battalion.objects.filter():
            bt_list.append((item.id, item.name))

        bg_f.fields['gordan'].choices = bt_list
        bg_f.initial['gordan'] = b
        
        cx = {'form': bg_f,'grohans':[],'new':True}
        return render(request, self.template, cx)

    def post(self, request):
        bg_f = BattalionGroupForm(request.POST, request.FILES or None)
        bt_list = []
        my_bt = battalion.objects.filter().all()
        for item in my_bt:
            bt_list.append((item.id, item.name))
        bg_f.fields['gordan'].choices = bt_list
        if not bg_f.is_valid():
            cx = {'form': bg_f,'grohans':[],'new':True}
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
        bg.is_active = bg_f.cleaned_data['is_active']
        bg.commander = bg_f.cleaned_data['commander']

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
        bg_f.fields['status_types'].choices = Soldier.status_types_options()
        bg_f.fields['status_types'].initial = bg.status_types_active
        
        bg_f.fields['gordan'].choices = bt_list
        bg_f.fields['gordan'].initial = bg.gordan.id
        bg_f.initial['zirediplom'] = bg.zirediplom
        bg_f.initial['diplom'] = bg.diplom
        bg_f.initial['ofghdiplom'] = bg.ofghdiplom
        bg_f.initial['lisans'] = bg.lisans
        bg_f.initial['ofghlisans'] = bg.ofghlisans
        bg_f.initial['doctra'] = bg.doctra
        bg_f.initial['shie'] = bg.shie
        bg_f.initial['ahle_tasnon'] = bg.ahle_tasnon
        bg_f.initial['zarfiat'] = bg.zarfiat
        bg_f.initial['takmilzarmit'] = bg.takmilzarmit
        bg_f.initial['order'] = bg.order
        bg_f.initial['salemm'] = bg.salemm
        bg_f.initial['moafazrazm'] = bg.moafazrazm
        bg_f.initial['moafazrazm_gorehbe'] = bg.moafazrazm_gorehbe
        bg_f.initial['gorehbe'] = bg.gorehbe
        bg_f.initial['is_active'] = bg.is_active
        bg_f.initial['commander'] = bg.commander
        
        cx = {'form': bg_f,'bg':bg}
        return render(request, self.template, cx)

    def post(self, request, pk):
        bg_f = BattalionGroupForm(request.POST, request.FILES or None)
        bg = battalion_group.objects.filter(pk=pk).first()
        bt_list = []
        my_bt = battalion.objects.filter().all()
        for item in my_bt:
            bt_list.append((item.id, item.name))
       
        bg_f.fields['status_types'].choices = Soldier.status_types_options()
        
        bg_f.fields['gordan'].choices = bt_list
        bg_f.fields['gordan'].initial = bg.gordan.id
        if not bg_f.is_valid():
            cx = {'form': bg_f,'bg':bg}
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
        bg.is_active = bg_f.cleaned_data['is_active']
        bg.commander = bg_f.cleaned_data['commander']

        status_types_choiced = list(bg_f.cleaned_data['status_types'])

        bg.set_status_types_list(status_types_choiced)
        bg.save()
        
        bg_f.fields['status_types'].initial = bg.status_types_active 
        messages.success(request,'ویرایش با موفقیت انجام شد.')
        
        cx = {'form': bg_f,'bg':bg}
        return render(request, self.template, cx)
    
    
def add_battalion_group_batch(request,battalation_pk=None):
    redirect_url = request.GET.get('redirect_url','')
    bg = battalion_group.objects.filter(pk=battalation_pk).first()
    if bg:
        try:
                batch = battalion_group_batch.objects.create(gorhan=bg)
                batch.save()
                messages.success(request,'دسته جدید ایجاد شد')
        except:
            messages.error(request,'ایجاد دسته با خطا مواجه شد')
    else:    
        messages.error(request,'گروهان مورد نظر یافت نشد')

    
    return redirect(redirect_url)

def remove_battalion_group_batch(request,pk=None):
    redirect_url = request.GET.get('redirect_url','')
    
    try:
        batch = battalion_group_batch.objects.filter(pk=pk)
        batch.delete()
        messages.success(request,'حذف دسته با موفقیت انجام شد')
    except:
        messages.error(request,'حذف دسته با خطا مواجه شد')

    return redirect(redirect_url)

def remove_all_battalion_group_batch(request,battalation_pk=None):
    redirect_url = request.GET.get('redirect_url','')
    
    try:
        batchs = battalion_group_batch.objects.filter(gorhan=battalation_pk)
        
        for b in batchs:
            b.delete()
            
        messages.success(request,'حذف همه دسته ها با موفقیت انجام شد')
    except:
        messages.error(request,'حذف دسته ها با خطا مواجه شد')

    return redirect(redirect_url)



def save_battalion_group_batch(request,pk=None):
    redirect_url = request.GET.get('redirect_url','')
    
    if request.method == 'POST':
        pass

    return redirect(redirect_url)
