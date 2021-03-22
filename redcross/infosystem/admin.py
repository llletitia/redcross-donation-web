from django.contrib import admin
from .models import DonateMoney,DonateResources
from .forms import DonateMoneyForm,DonateResourcesForm
from .models import ReceiveMoney,ReceiveResources
from .forms import ReceiveMoneyForm, ReceiveResourcesForm
from django.contrib.auth.models import User
from .forms import UserForm



#后台：信息增删改查
class DonateMoneyAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'org_name', 'province', 'date', 'quantity', 'receipt_id', 'intention')

    search_fields = ('id', 'org_name', 'date', 'quantity', 'receipt_id', 'intention')
    list_filter = ('province', 'date')   #指定列表过滤器，右边将会出现一个快捷的日期过滤选项，
    #以方便开发人员快速地定位到想要的数据，同样也可以指定非日期型类型的字段                

    #自定义编辑表单，在编辑表单的时候 显示哪些字段，显示的属性
    fields = ( 'id','org_name', 'province', 'date', 'quantity', 'receipt_id', 'intention')    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(DonateMoneyAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct
    form = DonateMoneyForm  # 在Form中自定义需要在后台中输入哪些信息


class ReceiveMoneyAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'rec_name', 'province', 'date', 'quantity')

    search_fields = ('id', 'rec_name', 'date', 'quantity')
    list_filter = ('province', 'date')   #指定列表过滤器，右边将会出现一个快捷的日期过滤选项，
    #以方便开发人员快速地定位到想要的数据，同样也可以指定非日期型类型的字段                

    #自定义编辑表单，在编辑表单的时候 显示哪些字段，显示的属性
    fields = ( 'id','rec_name', 'province', 'date', 'quantity')    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(ReceiveMoneyAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct
    form = ReceiveMoneyForm  # 在Form中自定义需要在后台中输入哪些信息


class DonateResourcesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'org_name', 'res_name', 'province', 'date', 'size', 'unit', 'quantity')

    search_fields = ('id', 'org_name','res_name', 'date', 'size', 'unit', 'quantity')
    list_filter = ('province', 'date')   #指定列表过滤器，右边将会出现一个快捷的日期过滤选项，
    #以方便开发人员快速地定位到想要的数据，同样你也可以指定非日期型类型的字段                

    fields = ( 'id', 'org_name', 'res_name', 'province', 'date', 'size', 'unit', 'quantity')    #自定义编辑表单，在编辑表单的时候 显示哪些字段，显示的属性
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(DonateResourcesAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct
    form = DonateResourcesForm  # 在Form中自定义需要在后台中输入哪些信息


class ReceiveResourcesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'rec_name', 'res_name', 'province', 'date', 'size', 'unit', 'quantity')

    search_fields = ('id', 'rec_name','res_name', 'date', 'size', 'unit', 'quantity')
    list_filter = ('province', 'date')   #指定列表过滤器，右边将会出现一个快捷的日期过滤选项，
    #以方便开发人员快速地定位到想要的数据，同样你也可以指定非日期型类型的字段                

    fields = ( 'id', 'rec_name', 'res_name', 'province', 'date', 'size', 'unit', 'quantity')    #自定义编辑表单，在编辑表单的时候 显示哪些字段，显示的属性
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(ReceiveResourcesAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct
    form = ReceiveResourcesForm  # 在Form中自定义需要在后台中输入哪些信息



# Register your models here.
admin.site.register(DonateMoney, DonateMoneyAdmin)
admin.site.register(ReceiveMoney, ReceiveMoneyAdmin)
admin.site.register(DonateResources, DonateResourcesAdmin)
admin.site.register(ReceiveResources, ReceiveResourcesAdmin)