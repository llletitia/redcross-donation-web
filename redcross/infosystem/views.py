from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User

from .forms import UserForm, DonateMoneyForm,DonateResourcesForm, ReceiveMoneyForm, ReceiveResourcesForm
from .models import DonateMoney, DonateResources, ReceiveMoney, ReceiveResources

import datetime
import pytz
from operator import attrgetter
from django.db.models import Sum, Count

# donatemoneyresult的import
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

ADMIN_ID = 1


# 主页
def index(request):
    return render(request, 'infosystem/index.html')

# 用户登录后主页
def userindex(request):
    return render(request, 'infosystem/userindex.html')


# 登录界面
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None:  # 登录成功
            if user.is_active:
                login(request, user)
                context = {
                    'username': request.user.username
                }
                if user.id == ADMIN_ID:  # 若id判定为管理员，则跳转至管理员数据统计界面
                    context = admin_stat(request)  # 接收管理员界面提交的数据
                    return render(request, 'infosystem/admin_stat.html', context)
                else:  # 若id判定为普通用户，则跳转至已登录状态的用户主页
                    return render(request, 'infosystem/userindex.html', context)
            else:  # 用户账户已失效，退回登录页并显示错误信息
                return render(request, 'infosystem/login.html', {'error_message': 'Your account has been disabled.'})
        else:  # 登录失败，退回登录页并显示错误信息
            return render(request, 'infosystem/login.html', {'error_message': 'Invalid login.'})
    return render(request, 'infosystem/login.html')


# 注册界面
def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)  # 注册
        if user is not None:
            if user.is_active:
                login(request, user)
                context = {
                    'username': request.user.username
                }
                return render(request, 'infosystem/login.html', context)  # 注册成功则跳转至用户登录页面
    context = {
        "form": form,
    }
    return render(request, 'infosystem/register.html', context)


#  个人中心界面中用户自主退出登录
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'infosystem/login.html', context)


# 管理员统计信息管理界面
# 1. 统计当月接受物资总次数、月接受款项总额、月发放物资次数与月发放款项总额
# 2. 可视化呈现统计数据（各月捐款总额等的柱形图）
# 3. 用户登录信息列表（以最后登录时间倒序排序）

def admin_stat(request):
    # 显示用户信息列表，并按用户最后一次登录时间排序
    informationtable = User.objects.values('username', 'last_login').order_by('-last_login').all()
    # print(informationtable)


    # 向红十字会数据统计图表提供数据
    # 各省款项接收与发放总额
    # 应用objects的filter()进行省份的筛选，聚合函数Sum()求和，并类型转换为变量值
    JS_Money_Out = DonateMoney.objects.filter(province='江苏').aggregate(Sum('quantity'))
    JS_Money_Out = JS_Money_Out['quantity__sum'] if (JS_Money_Out['quantity__sum'] is not None) else 0
    ZJ_Money_Out = DonateMoney.objects.filter(province='浙江').aggregate(Sum('quantity'))
    ZJ_Money_Out = ZJ_Money_Out['quantity__sum'] if (ZJ_Money_Out['quantity__sum'] is not None) else 0
    SH_Money_Out = DonateMoney.objects.filter(province='上海').aggregate(Sum('quantity'))
    SH_Money_Out = SH_Money_Out['quantity__sum'] if (SH_Money_Out['quantity__sum'] is not None) else 0

    JS_Money_Get = ReceiveMoney.objects.filter(province='江苏').aggregate(Sum('quantity'))
    JS_Money_Get = JS_Money_Get['quantity__sum'] if (JS_Money_Get['quantity__sum'] is not None) else 0
    ZJ_Money_Get = ReceiveMoney.objects.filter(province='浙江').aggregate(Sum('quantity'))
    ZJ_Money_Get = ZJ_Money_Get['quantity__sum'] if (ZJ_Money_Get['quantity__sum'] is not None) else 0
    SH_Money_Get = ReceiveMoney.objects.filter(province='上海').aggregate(Sum('quantity'))
    SH_Money_Get = SH_Money_Get['quantity__sum'] if (SH_Money_Get['quantity__sum'] is not None) else 0

    # 各省物资接收与发放笔数
    JS_Res_Out = DonateResources.objects.filter(province='江苏').count()
    ZJ_Res_Out = DonateResources.objects.filter(province='浙江').count()
    SH_Res_Out = DonateResources.objects.filter(province='上海').count()
    JS_Res_Get = ReceiveResources.objects.filter(province='江苏').count()
    ZJ_Res_Get = ReceiveResources.objects.filter(province='浙江').count()
    SH_Res_Get = ReceiveResources.objects.filter(province='上海').count()

    # print(JS_Money_Out)
    # print(JS_Res_Out)
    
    context = {
        'JS_Money_Out' : JS_Money_Out,
        'ZJ_Money_Out' : ZJ_Money_Out,
        'SH_Money_Out' : SH_Money_Out,
        'JS_Money_Get' : JS_Money_Get,
        'ZJ_Money_Get' : ZJ_Money_Get,
        'SH_Money_Get' : SH_Money_Get,
        'JS_Res_Out' : JS_Res_Out,
        'ZJ_Res_Out' : ZJ_Res_Out,
        'SH_Res_Out' : SH_Res_Out,
        'JS_Res_Get' : JS_Res_Get,
        'ZJ_Res_Get' : ZJ_Res_Get,
        'SH_Res_Get' : SH_Res_Get,

        # 用户信息表
        'informationtable' : informationtable,
    } 

    return context



# 个人中心界面
# 查询个人信息
def personal_info(request):
    if request.user.is_authenticated:
        # myusername = user.username(user=request.user) 
        # print(request.user.username)
        # print(request.user.last_login)
        context = {
            'username': request.user.username,
            'user_email': request.user.email,  
            'login_time':request.user.last_login,
        }
        return render(request, 'infosystem/UserCenter.html', context)
    return render(request, 'infosystem/login.html')  # 用户如果没登录，render登录页面


# 修改个人信息
def edit_info(request):
    form = UserForm(request.POST or None)
    if request.user.is_authenticated:
        # username = request.POST.get('username', False)
        # password = request.POST.get('password', False)
        cur_email = request.POST.get('user_email', False)
        request.user.email = cur_email
        request.user.save()
        # print(request.user.email)
    
    return render(request, 'infosystem/edit_info.html')




# 搜索结果页面
def donate_money_result(request):

    # 获得查询条件
    form = DonateMoneyForm(request.GET)

    donatemoney_org_name = request.GET.get('org_name',"")
    donatemoney_province = request.GET.get('province')
    donatemoney_begin_date = request.GET.get('begin_date')
    donatemoney_end_date = request.GET.get('end_date')
    donatemoney_min_quantity = request.GET.get('min_quantity')
    donatemoney_max_quantity = request.GET.get('max_quantity')
    donatemoney_intention = request.GET.get('intention',"")
    donatemoney_sortkey = request.GET.get('sortkey')
 
    # 从donatemoney数据库中筛选province、orgname、intention满足条件的数据
    all_donate_money = DonateMoney.objects.filter(
        province = donatemoney_province,
        org_name__icontains = donatemoney_org_name, #模糊查询
        intention__icontains = donatemoney_intention, #模糊查询
        )

    usable_dm = []#all_donate_money
    
    # 在日期区间和数量/金额区间内筛选出符合的数据，加入usable_dm队列
    for dm in all_donate_money:  # off-set aware
        if datetime.datetime.date(datetime.datetime.strptime(donatemoney_begin_date, '%Y-%m-%d')) <dm.date < datetime.datetime.date(datetime.datetime.strptime(donatemoney_end_date, '%Y-%m-%d')) and int(donatemoney_min_quantity) < dm.quantity < int(donatemoney_max_quantity): 
            usable_dm.append(dm)

    # 按给出的sortkey进行排序  
    sorted_dm = usable_dm
    if donatemoney_sortkey == '捐赠方':
        sorted_dm = sorted(usable_dm, key=attrgetter('org_name'))
    elif donatemoney_sortkey == '省份':
        sorted_dm = sorted(usable_dm, key=attrgetter('province')) 
    elif donatemoney_sortkey == '日期':
        sorted_dm = sorted(usable_dm, key=attrgetter('date'))  
    elif donatemoney_sortkey == '数量':
        sorted_dm = sorted(usable_dm, key=attrgetter('quantity'))
    elif donatemoney_sortkey == '定向项目':
        sorted_dm = sorted(usable_dm, key=attrgetter('intention'))  

    # 转换时间格式
    time_format = '%Y-%m-%d'
    for dm in sorted_dm:
        dm.date = dm.date.strftime(time_format)

    #告知前端查询结果是否为空
    dis_search_head = 'block'
    dis_search_failure = 'none'
    if len(usable_dm) == 0: 
        dis_search_head = 'none'
        dis_search_failure = 'block'

    #分页
    if len(sorted_dm) > 0: # 查询结果有数据
        paginator = Paginator(sorted_dm, 25) # 每页显示25个数据
        page = request.GET.get('page') # 获取当前页码
        totalPages = paginator.num_pages
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger: # 页码非整数时，显示第一页
            contacts = paginator.page(1)
        except EmptyPage: # 超过最大页码时，显示最后一页
            contacts = paginator.page(paginator.num_pages)
        
        context = {
            'dis_search_head': dis_search_head,
            'dis_search_failure': dis_search_failure,  #
            'contacts' : contacts,
            'totalPages' : totalPages,
            'total_num' : len(usable_dm),
            # 保留筛选信息
            'org_name' : donatemoney_org_name,
            'province' : donatemoney_province,
            'begin_date' : donatemoney_begin_date,
            'end_date' : donatemoney_end_date,
            'min_quantity' : donatemoney_min_quantity,
            'max_quantity' : donatemoney_max_quantity,
            'intention' : donatemoney_intention,
            'sortkey' : donatemoney_sortkey
        }
        return render(request, 'infosystem/donate_money_result.html', context)
    else: # 查询结果为空
        info = '暂无数据'
        totalPages = 0
        context = {
            'dis_search_head': dis_search_head,
            'dis_search_failure': dis_search_failure,  # 导航栏信息更新    
            'totalPages' : totalPages,
            'total_num' : len(usable_dm),
            # 保留筛选信息
            'org_name' : donatemoney_org_name,
            'province' : donatemoney_province,
            'begin_date' : donatemoney_begin_date,
            'end_date' : donatemoney_end_date,
            'min_quantity' : donatemoney_min_quantity,
            'max_quantity' : donatemoney_max_quantity,
            'intention' : donatemoney_intention,
            'sortkey' : donatemoney_sortkey
        }
        return render(request, 'infosystem/donate_money_result.html', context)
    return render(request, 'infosystem/donate_money_result.html', context)
    

 

def donate_resources_result(request):
    form = DonateResourcesForm(request.GET)

    donateresources_res_name = request.GET.get('res_name',"")
    donateresources_province = request.GET.get('province')
    donateresources_begin_date = request.GET.get('begin_date')   
    donateresources_end_date = request.GET.get('end_date')
    donateresources_min_quantity = request.GET.get('min_quantity')
    donateresources_max_quantity = request.GET.get('max_quantity')
    donateresources_intention = request.GET.get('intention',"")
    donateresources_sortkey = request.GET.get('sortkey')
   
    #现写法
    all_donate_money = DonateResources.objects.filter(# id = donateresources_id,
        province = donateresources_province,
        res_name__icontains = donateresources_res_name,# 包含
        
        intention__icontains = donateresources_intention,
        )
    # ds=DonateResources
    usable_ds = []#all_donate_money
    
    for ds in all_donate_money:
        if datetime.datetime.date(datetime.datetime.strptime(donateresources_begin_date, '%Y-%m-%d')) < ds.date < datetime.datetime.date(datetime.datetime.strptime(donateresources_end_date, '%Y-%m-%d')) and int(donateresources_min_quantity) < ds.quantity < int(donateresources_max_quantity): 
            usable_ds.append(ds)
    sorted_ds = usable_ds
    #sorted_ds = []#排好序的
    if donateresources_sortkey == '捐赠方':
        sorted_ds = sorted(usable_ds, key=attrgetter('org_name'))
    if donateresources_sortkey == '物资名称':
        sorted_ds = sorted(usable_ds, key=attrgetter('res_name'))
    elif donateresources_sortkey == '省份':
        sorted_ds = sorted(usable_ds, key=attrgetter('province')) 
    elif donateresources_sortkey == '日期':
        sorted_ds = sorted(usable_ds, key=attrgetter('date'))  
    elif donateresources_sortkey == '数量':
        sorted_ds = sorted(usable_ds, key=attrgetter('quantity'))
    elif donateresources_sortkey == '定向':
        sorted_ds = sorted(usable_ds, key=attrgetter('intention'))     
    # 转换时间格式
    time_format = '%Y-%m-%d'#这段不知到还有没有用
    for ds in sorted_ds:# 这里可能为了显示原因，要给每个usable_ds_by都转换一次
        ds.date = ds.date.strftime(time_format)  # 转成了str

    dis_search_head = 'block'
    dis_search_failure = 'none'
    if len(usable_ds) == 0:   
        dis_search_head = 'none'
        dis_search_failure = 'block'
    else: 
        print('is not zero!!')

    if len(sorted_ds) > 0:
        paginator = Paginator(sorted_ds, 25)#每页25个数据
        page = request.GET.get('page')
        totalPages = paginator.num_pages
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        
        context = {
            'dis_search_head': dis_search_head,
            'dis_search_failure': dis_search_failure,  # 导航栏信息更新
            'contacts' : contacts,
            'totalPages' : totalPages,
            #保留筛选信息
            'res_name' : donateresources_res_name,
            'province' : donateresources_province,
            'begin_date' : donateresources_begin_date,
            'end_date' : donateresources_end_date,
            'min_quantity' : donateresources_min_quantity,
            'max_quantity' : donateresources_max_quantity,
            'intention' : donateresources_intention,
            'sortkey' : donateresources_sortkey,

            'total_num' : len(usable_ds)
        }
        return render(request, 'infosystem/donate_resources_result.html', context)
    else:
        info = '暂无数据'
        print('暂无数据\n')
        totalPages = 0
        context = {
            'dis_search_head': dis_search_head,
            'dis_search_failure': dis_search_failure,  # 导航栏信息更新
            
            'totalPages' : totalPages,

            'Res_Name' : donateresources_res_name,
            'province' : donateresources_province,
            'begin_date' : donateresources_begin_date,
            'end_date' : donateresources_end_date,
            'min_quantity' : donateresources_min_quantity,
            'max_quantity' : donateresources_max_quantity,
            'intention' : donateresources_intention,
            'sortkey' : donateresources_sortkey,

            'total_num' : len(usable_ds)

        }
        return render(request, 'infosystem/donate_resources_result.html', context)
    return render(request, 'infosystem/donate_resources_result.html', context)





def receive_money_result(request):
    form = ReceiveMoneyForm(request.GET)

    receivemoney_rec_name = request.GET.get('rec_name',"")
    receivemoney_province = request.GET.get('province')
    receivemoney_begin_date = request.GET.get('begin_date')   
    receivemoney_end_date = request.GET.get('end_date')
    receivemoney_min_quantity = request.GET.get('min_quantity')
    receivemoney_max_quantity = request.GET.get('max_quantity')
    receivemoney_sortkey = request.GET.get('sortkey')
   
    #现写法
    all_receive_money = ReceiveMoney.objects.filter(# id = receivemoney_id,
        province = receivemoney_province,
        rec_name__icontains = receivemoney_rec_name,# 包含

        )
    # rm=ReceiveMoney
    usable_rm = []#all_receive_money
    
    for rm in all_receive_money:
        if datetime.datetime.date(datetime.datetime.strptime(receivemoney_begin_date, '%Y-%m-%d')) < rm.date < datetime.datetime.date(datetime.datetime.strptime(receivemoney_end_date, '%Y-%m-%d')) and int(receivemoney_min_quantity) < rm.quantity < int(receivemoney_max_quantity): 
            usable_rm.append(rm)
    sorted_rm = usable_rm
    #sorted_rm = []#排好序的
    if receivemoney_sortkey == '受赠方':
        sorted_rm = sorted(usable_rm, key=attrgetter('rec_name'))
    elif receivemoney_sortkey == '省份':
        sorted_rm = sorted(usable_rm, key=attrgetter('province')) 
    elif receivemoney_sortkey == '日期':
        sorted_rm = sorted(usable_rm, key=attrgetter('date'))  
    elif receivemoney_sortkey == '数量':
        sorted_rm = sorted(usable_rm, key=attrgetter('quantity'))
    # 转换时间格式
    time_format = '%Y-%m-%d'#这段不知到还有没有用
    for rm in sorted_rm:# 这里可能为了显示原因，要给每个usable_rm_by都转换一次
        rm.date = rm.date.strftime(time_format)  # 转成了str

    dis_search_head = 'block'
    dis_search_failure = 'none'
    if len(usable_rm) == 0:   
        dis_search_head = 'none'
        dis_search_failure = 'block'
    else: 
        print('is not zero!!')

    if len(sorted_rm) > 0:
        paginator = Paginator(sorted_rm, 25)#每页25个数据
        page = request.GET.get('page')
        totalPages = paginator.num_pages
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        
        context = {
            'dis_search_head': dis_search_head,
            'dis_search_failure': dis_search_failure,  # 导航栏信息更新
            'contacts' : contacts,
            'totalPages' : totalPages,
            #保留筛选信息
            'rec_name' : receivemoney_rec_name,
            'province' : receivemoney_province,
            'begin_date' : receivemoney_begin_date,
            'end_date' : receivemoney_end_date,
            'min_quantity' : receivemoney_min_quantity,
            'max_quantity' : receivemoney_max_quantity,
            'sortkey' : receivemoney_sortkey,

            'total_num' : len(usable_rm)
        }
        return render(request, 'infosystem/receive_money_result.html', context)
    else:
        info = '暂无数据'
        print('暂无数据\n')
        totalPages = 0
        context = {
            'dis_search_head': dis_search_head,
            'dis_search_failure': dis_search_failure,  # 导航栏信息更新
            
            'totalPages' : totalPages,

            'rec_name' : receivemoney_rec_name,
            'province' : receivemoney_province,
            'begin_date' : receivemoney_begin_date,
            'end_date' : receivemoney_end_date,
            'min_quantity' : receivemoney_min_quantity,
            'max_quantity' : receivemoney_max_quantity,
            'sortkey' : receivemoney_sortkey,

            'total_num' : len(usable_rm)

        }
        return render(request, 'infosystem/receive_money_result.html', context)
    return render(request, 'infosystem/receive_money_result.html', context)
    


def receive_resources_result(request):
    form = ReceiveResourcesForm(request.GET)

    receiveresources_rec_name = request.GET.get('rec_name',"")
    receiveresources_res_name = request.GET.get('res_name',"")
    receiveresources_province = request.GET.get('province')
    receiveresources_begin_date = request.GET.get('begin_date')   
    receiveresources_end_date = request.GET.get('end_date')
    receiveresources_min_quantity = request.GET.get('min_quantity')
    receiveresources_max_quantity = request.GET.get('max_quantity')
    receiveresources_sortkey = request.GET.get('sortkey')
   
    #现写法
    all_receive_resources = ReceiveResources.objects.filter(# id = receiveresources_id,
        province = receiveresources_province,
        rec_name__icontains = receiveresources_rec_name,# 包含
        res_name__icontains = receiveresources_res_name,# 包含
        
        )
    # rr=ReceiveResources
    usable_rr = []#all_receive_resources
    for rr in all_receive_resources:
        if datetime.datetime.date(datetime.datetime.strptime(receiveresources_begin_date, '%Y-%m-%d')) < rr.date < datetime.datetime.date(datetime.datetime.strptime(receiveresources_end_date, '%Y-%m-%d')) and int(receiveresources_min_quantity) < rr.quantity < int(receiveresources_max_quantity): 
            usable_rr.append(rr)
    sorted_rr = usable_rr
    #sorted_rr = []#排好序的
    if receiveresources_sortkey == '受赠方':
        sorted_rr = sorted(usable_rr, key=attrgetter('rec_name'))
    elif receiveresources_sortkey == '物资名称':
        sorted_rr = sorted(usable_rr, key=attrgetter('res_name')) 
    elif receiveresources_sortkey == '省份':
        sorted_rr = sorted(usable_rr, key=attrgetter('province')) 
    elif receiveresources_sortkey == '日期':
        sorted_rr = sorted(usable_rr, key=attrgetter('date'))  
    elif receiveresources_sortkey == '数量':
        sorted_rr = sorted(usable_rr, key=attrgetter('quantity'))
 
    # 转换时间格式
    time_format = '%Y-%m-%d'#这段不知到还有没有用
    for rr in sorted_rr:# 这里可能为了显示原因，要给每个usable_rr_by都转换一次
        rr.date = rr.date.strftime(time_format)  # 转成了str

    dis_search_head = 'block'
    dis_search_failure = 'none'
    if len(usable_rr) == 0:   
        dis_search_head = 'none'
        dis_search_failure = 'block'
    else: 
        print('is not zero!!')

    if len(sorted_rr) > 0:
        paginator = Paginator(sorted_rr, 25)#每页25个数据
        page = request.GET.get('page')
        totalPages = paginator.num_pages
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        
        context = {
            'dis_search_head': dis_search_head,
            'dis_search_failure': dis_search_failure,  # 导航栏信息更新
            'contacts' : contacts,
            'totalPages' : totalPages,
            #保留筛选信息
            'rec_name' : receiveresources_rec_name,
            'res_name' : receiveresources_res_name,
            'province' : receiveresources_province,
            'begin_date' : receiveresources_begin_date,
            'end_date' : receiveresources_end_date,
            'min_quantity' : receiveresources_min_quantity,
            'max_quantity' : receiveresources_max_quantity,
            'sortkey' : receiveresources_sortkey,

            'total_num' : len(usable_rr)
        }
        return render(request, 'infosystem/receive_resources_result.html', context)
    else:
        info = '暂无数据'
        print('暂无数据\n')
        totalPages = 0
        context = {
            'dis_search_head': dis_search_head,
            'dis_search_failure': dis_search_failure,  # 导航栏信息更新
            
            'totalPages' : totalPages,

            'rec_name' : receiveresources_rec_name,
            'Res_Name' : receiveresources_res_name,
            'province' : receiveresources_province,
            'begin_date' : receiveresources_begin_date,
            'end_date' : receiveresources_end_date,
            'min_quantity' : receiveresources_min_quantity,
            'max_quantity' : receiveresources_max_quantity,
            'sortkey' : receiveresources_sortkey,

            'total_num' : len(usable_rr)

        }
        return render(request, 'infosystem/receive_resources_result.html', context)
    return render(request, 'infosystem/receive_resources_result.html', context)