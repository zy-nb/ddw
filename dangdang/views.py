import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'emailTest.settings'

from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect, HttpResponse
from regist.models import *

import random, string, os, hashlib
from dangdang.captcha.image import ImageCaptcha

from operapp.views import updateSQL

# 排序函数
def book_sort(sort, booklist,sortStr):

    # sortStr= a : 升序
    # sortStr= b : 降序


    for i in range(len(booklist)):
        for j in range(i + 1, len(booklist)):

            # 销量由高到低
            if sort == 'xl' and sortStr=='b':
                if booklist[i].sales < booklist[j].sales:
                    booklist[i], booklist[j] = booklist[j], booklist[i]
            # 销量从低到高
            elif sort == 'xl' and sortStr=='a':
                if booklist[i].book_dprice > booklist[j].book_dprice:
                    booklist[i], booklist[j] = booklist[j], booklist[i]

            # 默认价格从高到低
            elif sort == 'jg' and sortStr=='b':
                if booklist[i].book_dprice < booklist[j].book_dprice:
                    booklist[i], booklist[j] = booklist[j], booklist[i]
            # 价格由低到高
            elif sort == 'jg' and sortStr=='a':
                if booklist[i].book_dprice > booklist[j].book_dprice:
                    booklist[i], booklist[j] = booklist[j], booklist[i]

            # 出版时间由近到远
            elif sort == 'ot' and sortStr=='b':
                if booklist[i].shelves_date < booklist[j].shelves_date:
                    booklist[i], booklist[j] = booklist[j], booklist[i]
            # 出版时间由远到近
            elif sort == 'ot' and sortStr=='a':
                if booklist[i].shelves_date > booklist[j].shelves_date:
                    booklist[i], booklist[j] = booklist[j], booklist[i]
            # 默认
            else:
                if booklist[i].book_dprice > booklist[j].book_dprice:
                    booklist[i], booklist[j] = booklist[j], booklist[i]
    return booklist



# 生成验证码
def getcaptcha(request):
    image = ImageCaptcha(fonts=[os.path.abspath('dangdang\captcha\data\DroidSansMono.ttf')])
    code = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 5)
    random_code = "".join(code)

    request.session['code'] = random_code
    print(random_code)
    data = image.generate(random_code)

    return HttpResponse(data, 'image/png')






# 渲染主页
def index(request):
    name = request.session.get('nickname', '')

    one_category = DCategory.objects.filter(category_pid='0').order_by('id')
    two_category = DCategory.objects.exclude(category_pid='0')

    # 最新上架书籍
    books = TBook.objects.all().order_by('-shelves_date')[0:10]
    books1 = books[0:8]

    # 高价书籍
    books_money = TBook.objects.all().order_by('-book_dprice')[0:12]
    # print(books_money)

    seles_raw = TBook.objects.raw('select * from (select * from t_book order by shelves_date desc limit 8) AS a order by a.sales desc')

    return render(request, 'index.html', {'one_category': one_category,
                                          'two_category': two_category,
                                          'books': books1,
                                          'books_money': books_money,
                                          'books_sales': seles_raw,
                                          'name': name
                                          })


# 渲染书籍列表页
def booklist(request):
    nickname = request.session.get('nickname')
    category = request.GET.get('category')  # 分类
    num = request.GET.get('num', '1')  # 页码
    sort = request.GET.get('sort', 'jg')  # 排序方式
    sortStr = request.GET.get('sortStr', '')  # 升/降序
    dcate = DCategory.objects.filter(category_id=category)[0].category_pid
    book_list = []
    # keyword =request.GET.get("keyword","book_id")

    if dcate == '0':
        # 一级分类
        category_list = DCategory.objects.filter(category_pid=category)
        book_category = [category]

        for i in category_list:
            book_category.append(i.category_id)

        book_all = TBook.objects.all()
        for i in book_category:
            for j in book_all:
                if j.book_category_id == i:
                    book_list.append(j)

    else:
        # 二级分类
        book_all = TBook.objects.all()
        for j in book_all:
            if j.book_category_id == category:
                book_list.append(j)

    one_category = DCategory.objects.filter(category_pid='0').order_by('id')
    two_category = DCategory.objects.exclude(category_pid='0')

    # 排序方法排序
    book_list = book_sort(sort, book_list,sortStr)

    pagtor = Paginator(book_list, per_page=3)
    pages_count = pagtor.count
    pages_num = pagtor.num_pages

    # 控制输入页码格式
    try:
        if int(num) > pages_num:
            num = pages_num
        elif int(num) < 0:
            num = 1
    except:
        num = 1

    page = pagtor.page(int(num))

    return render(request, 'booklist.html', {
                                             'nickname':nickname,
                                              'one_category': one_category,  # 一级分类
                                             'two_category': two_category,  # 二级分类
                                             'book_list': book_list,  # 书籍列表，备用
                                             'page': page,  # 分页对象
                                             'pages_num': pages_num,  # 总页数
                                             'pages_count': pages_count,  # 该类别书籍数量
                                             'category': category,  # 分类目标
                                             'dcate': dcate,  # 父级分类目标
                                             'sort': sort,
                                             'sortStr':sortStr,
                                             # "keyword": keyword,
                                             })





# ajax检测验证码
def ajax_code(request):
    code = ''
    if request.method == 'GET':
        code = request.GET.get('code_num')
    if code.upper() == request.session.get('code').upper():
        return HttpResponse('ok')
    return HttpResponse('no')







# 渲染注册页面
def regist(request):
    request.session['regist_flag']=request.GET.get('regist_flag')
    return render(request, 'register.html')


# 处理注册逻辑
def regist_logic(request):
    regist_flag = request.session.get('regist_flag')
    try:
        with transaction.atomic():
            name = request.POST.get('username')
            pwd = request.POST.get('pwd')
            nickname = request.POST.get('nickname')
            h = hashlib.sha256()
            h.update(name.encode() + pwd.encode())
            en_pwd = h.hexdigest()
            print(name,pwd,nickname)
            relust = TUser.objects.create(user_id=name, user_email=name, user_password=en_pwd, user_name=nickname)
            if relust:
                # 注册成功，将昵称保存到session
                request.session['nickname'] = nickname
                request.session['userid'] = name
                request.session['login'] = 'ok'
                cart = request.session.get('cart', '')
                cartSQL(cart, name)
                if regist_flag == 'cart':
                    return redirect('operapp:cartSubmit')
                return redirect('dangdang:registOk')
    except:
        del request.session['nickname']
        regist_in = 'no'
        return render(request, 'register.html', {'regist_in': regist_in, 'regist_flag': regist_flag})


# 注册ajax用户名验证
def ajax_name(request):
    username = ''
    if request.method == 'GET':
        username = request.GET.get('name')
    elif request.method == 'POST':
        username = request.POST.get('name')

    relust = TUser.objects.filter(user_email=username)
    if relust:
        return HttpResponse('no')
    return HttpResponse('ok')

# 渲染注册成功页面
def regist_ok(request):
    name = request.session.get('userid')
    regist_flag = request.session.get('regist_flag')
    cart = request.session.get('cart', '')
    cartSQL(cart, name)
    if regist_flag == 'cart':
        return redirect('operapp:cartSubmit')
    return render(request, 'register ok.html', {'regist_flag': regist_flag, 'name': name})


# ajax登出
def ajaxOut(request):
    res = HttpResponse('out')
    # 删除登录状态
    if request.session.get('login'):
        del request.session['login']
    # 删除登录ID
    if request.session.get('userid'):
        del request.session['userid']
    # 删除cookies
    if request.COOKIES.get('name'):
        res.set_cookie('name', 0, max_age=0)
        res.set_cookie('pwd', 0, max_age=0)
    # 删除昵称
    del request.session['nickname']
    # 删除session购物车
    if request.session.get('cart'):
        del request.session['cart']
    return res

# 渲染登录界面
def login(request):
    login_flag = request.GET.get('login_flag')
    name = request.COOKIES.get('name')
    pwd = request.COOKIES.get('pwd')

    res = render(request, 'login.html', {'login_flag': login_flag, })

    if name and pwd:
        result = TUser.objects.filter(user_email=name, user_password=pwd)
        if result:
            request.session['nickname'] = result[0].user_name
            request.session['userid'] =name
            request.session['login'] = 'ok'
            request.session.set_expiry(0)
            cart=request.session.get('cart','')
            cartSQL(cart,name)
            if login_flag=='cart':
                return redirect('operapp:cartSubmit')
            return redirect('dangdang:index')
    return res



# 处理登录逻辑
def login_logic(request):
    login_flag = request.POST.get('login_flag','index')
    name = request.POST.get('username')
    pwd = request.POST.get('userpwd')

    toLogin = request.POST.get('autologin')
    h=hashlib.sha256()
    h.update(name.encode()+pwd.encode())
    en_pwd=h.hexdigest()

    query = TUser.objects.filter(user_email=name, user_password=en_pwd)
    if query:
        request.session['nickname'] = query[0].user_name
        request.session['userid'] = name
        request.session['login'] = 'ok'
        request.session.set_expiry(0)

        cart = request.session.get('cart', '')
        cartSQL(cart, name)

        if login_flag == 'cart':
            res = redirect('operapp:cartSubmit')
        else:
            res = redirect('dangdang:index')

        if toLogin:
            res.set_cookie('name', name, max_age=7 * 24 * 3600)
            res.set_cookie('pwd', pwd, max_age=7 * 24 * 3600)
        return res

    else:
        login_in = 'no'
    return render(request, 'login.html', {'login_in': login_in})

# 将购物车数据存储到数据库中
def cartSQL(cart,id):
    # 登录时判断有无cart
    if cart:
        userobj = TUser.objects.filter(user_id=id)[0]
        books = Shoppingcart.objects.filter(user=userobj).all()
        if books:
            for i in books:
                cart.add_cart(i.bookid.book_id,i.book_number)
        updateSQL(cart,id)
# # Ajax邮箱验证
# def ajaxEmail(request):
#     Emailcode=request.GET.get('userid')
#     # 邮箱验证码
#     print( '邮箱验证码：',Emailcode)
#     subject, from_email, to = '百知教育注册验证码', '1150979872@qq.com', userid
#     text_content = ''
#     html_content = '<h2>欢迎访问百知教育旗下当当网站，这是一条验证码邮件，请复制下面验证码进行验证！</h2><hr><h3>'+Emailcode+'</h3>'
#     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()
#
#     return HttpResponse(Emailcode)