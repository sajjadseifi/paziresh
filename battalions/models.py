from django.db import models
from django.apps import apps

class battalion(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام گردان')
    commander = models.CharField(max_length=100, null=True, blank=True,default='',verbose_name='فرمانده گردان')
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')
    order = models.IntegerField(null=True, blank=True, verbose_name='اولویت مرتب سازی')
    gcode = models.CharField(max_length=150 ,null=True,blank=True,default='', verbose_name='کد گردانی')

    @property
    def grohans(self):
        return list(battalion_group.objects.filter(gordan=self))

    @property
    def soldiers_counts_after_tatbigh(self):
        Soldier = apps.get_model('soldiers', 'Soldier')

        return Soldier.objects.filter(t_Gordan__pk=self.pk).count()


    @property
    def soldiers_counts_before_tatbigh(self):
        Soldier = apps.get_model('soldiers', 'Soldier')
        
        return Soldier.objects.filter(Gordan__pk=self.pk).count()

    def reduce_soldiers(self):
        diffrence = self.soldiers_counts_after_tatbigh - self.soldiers_counts_before_tatbigh
        reduce ='up' if diffrence > 0 else 'down'  
        counts = diffrence if reduce == 'up' else diffrence * -1
        if counts == 0:
            reduce =''
        return {'counts' :counts,'reduce':reduce }
        
    class Meta:
        verbose_name = "گردان"
        verbose_name_plural = "گردان ها"


    def __str__(self):
        return self.name


class battalion_group(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام گروهان')
    commander = models.CharField(max_length=100,blank=True,null=True,default='', verbose_name='فرمانده گروهان')
    gordan = models.ForeignKey(battalion, on_delete=models.CASCADE, verbose_name='گردان')
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')

    status_types_data = models.JSONField(default=dict,blank=True,verbose_name="نوع برگه اعزام")
    zirediplom = models.BooleanField(default=False, verbose_name='زیر دیپلم')
    diplom = models.BooleanField(default=False, verbose_name='دیپلم')
    ofghdiplom = models.BooleanField(default=False, verbose_name='فوق دیپلم')
    lisans = models.BooleanField(default=False, verbose_name='لیسانس')
    ofghlisans = models.BooleanField(default=False, verbose_name='فوق لیسانس')
    doctra = models.BooleanField(default=False, verbose_name='دکترا')
    shie = models.BooleanField(default=False, verbose_name='شیعه')
    ahle_tasnon = models.BooleanField(default=False, verbose_name='اهل تسنن')
    zarfiat = models.CharField(max_length=250, verbose_name='ظرفیت گروهان')
    takmilzarmit = models.BooleanField(default=False, verbose_name='تکمیل بودن ظرفیت')
    order = models.IntegerField(null=True, blank=True, verbose_name='اولویت مرتب سازی')
    salemm = models.BooleanField(default=False, verbose_name='سالم')
    moafazrazm = models.BooleanField(default=False, verbose_name='معاف ازرزم')
    gorehbe = models.BooleanField(default=False, verbose_name='گروه ب')
    moafazrazm_gorehbe = models.BooleanField(default=False, verbose_name='معاف از رزم + گروه ب')
    zarfiat_total = models.CharField(max_length=250, verbose_name='ظرفیت گروهان کل', null=True, blank=True)
    
    # gharagah_sazandegi_khatam = models.BooleanField(default=False,null=True, blank=True, verbose_name='قرارگاه سازندگی خاتم')
    @property
    def batchs(self):
        return battalion_group_batch.objects.filter(gorhan=self.pk)

    
    @property
    def fill_space(self):
        Soldier = apps.get_model('soldiers', 'Soldier')
        return Soldier.objects.filter(battalion_group=self.pk).count()
        
    @property
    def free_space(self):
        try:
            return int(self.zarfiat) - self.fill_space
        except:
            return 0 - self.fill_space

    @property
    def status_types(self):
        return self.status_types_data
    
    @property
    def status_types_active(self):
        if not self.status_types_data:
            self.status_types_data = dict()
             
        return list(filter(lambda std:self.status_types_data[std],self.status_types_data.keys()))
    
    def set_status_types_list(self,status_types_list=[]):
        Soldier = apps.get_model('soldiers', 'Soldier')
        
        obj = dict()
        for st in Soldier.status_types_list():
            obj[st] =  False
        
        for st in status_types_list:
            obj[st] =  True

        print(obj)
        self.status_types_data = obj 
            
    @property
    def settings_list(self):
        boolean_fields = [
            'zirediplom','diplom','ofghdiplom','lisans','ofghlisans','doctra',
            'shie','ahle_tasnon',
            'salemm','moafazrazm','gorehbe','moafazrazm_gorehbe',
        ] 

        active_settings = []
        for field in boolean_fields:
            if getattr(self, field):
                active_settings.append(self._meta.get_field(field).verbose_name)

        status_types = list(map(lambda s: f'اعزام ( {s} )',self.status_types_active))
        return status_types + active_settings 

    @classmethod
    def clean_data(cls):
        return {
            'zirediplom':False,
            'diplom':False,
            'ofghdiplom':False,
            'lisans':False,
            'ofghlisans':False,
            'doctra':False,
            'shie':False,
            'ahle_tasnon':False,
            'salemm':False,
            'moafazrazm':False,
            'gorehbe':False,
            'moafazrazm_gorehbe':False,
            'order':1,
            'zarfiat_total':0,
            'zarfiat':100,
            'is_active':False,
            'takmilzarmit':False,
            'status_types_data':[],
        }
    
    class Meta:
        verbose_name = "گروهان"
        verbose_name_plural = "گروهان ها"

    def __str__(self):
        return self.name + self.gordan.name

class battalion_group_batch(models.Model):
    gorhan = models.ForeignKey(battalion_group, on_delete=models.CASCADE, verbose_name='گروهان')
    name = models.CharField(max_length=150, default='',verbose_name='نام دسته')
    commander = models.CharField(max_length=100,blank=True,null=True,default='', verbose_name='مسئول دسته')
    batch_range_start = models.IntegerField(null=True, blank=True, default=0 , verbose_name='شروع شماره دسته')
    batch_range_end   = models.IntegerField(null=True, blank=True, default=-1, verbose_name='پایان شماره دسته')

    class Meta:
        verbose_name = "دسته های گروهان"
        verbose_name_plural = "دسته های گروهان"

    def __str__(self):
        return self.gorhan.gordan.gcode + self.gorhan.name + self.name
