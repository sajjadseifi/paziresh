from django.contrib import admin
from .models import (
    NormalLetterModels,
    CheckoutLetterModels,
    RegisterNormalLetter,
    RunawayNormallLetter,
    FarajaNormallLetter,
    MoarefiNormallLetter
)


class RegisterNormalLetterInline(admin.StackedInline):
    model = RegisterNormalLetter
    extra = 0
    max_num = 1


class RunawayNormallLetterInline(admin.StackedInline):
    model = RunawayNormallLetter
    extra = 0
    max_num = 1


class FarajaNormallLetterInline(admin.StackedInline):
    model = FarajaNormallLetter
    extra = 0
    max_num = 1


class MoarefiNormallLetterInline(admin.StackedInline):
    model = MoarefiNormallLetter
    extra = 0
    max_num = 1


@admin.register(NormalLetterModels)
class NormalLetterAdmin(admin.ModelAdmin):
    list_display = ('number', 'subject', 'soldire', 'create_time', 'destination', 'status')
    search_fields = ('number', 'subject', 'soldire__first_name', 'soldire__last_name')
    list_filter = ('create_time', 'status')
    ordering = ('-create_time',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []

        inlines = []

        if RegisterNormalLetter.objects.filter(normal_letter=obj).exists():
            inlines.append(RegisterNormalLetterInline(self.model, self.admin_site))

        if RunawayNormallLetter.objects.filter(normal_letter=obj).exists():
            inlines.append(RunawayNormallLetterInline(self.model, self.admin_site))

        if FarajaNormallLetter.objects.filter(normal_letter=obj).exists():
            inlines.append(FarajaNormallLetterInline(self.model, self.admin_site))

        if MoarefiNormallLetter.objects.filter(normal_letter=obj).exists():
            inlines.append(MoarefiNormallLetterInline(self.model, self.admin_site))

        return inlines



@admin.register(CheckoutLetterModels)
class CheckoutLetterModelsAdmin(admin.ModelAdmin):
    list_display = ('soldire', 'description', 'number', 'c_type', 'status')
    search_fields = ('soldire', 'description', 'number', 'c_type', 'status')
    list_filter = ('create_time', 'status')
    ordering = ('-create_time',)