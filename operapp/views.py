import time

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from regist.models import *
from operapp.carts import Cart,CartItem


# Create your views here.

# 渲染购物车页面
def cart(request):
    nickname=request.session.get('nickname')
    userid=request.session.get('userid')
    # 没有登录信息显示session中的购物车信息
    cart = request.session.get('cart')
    if cart:
        del_caer_items=cart.del_cart_items
    else:
        del_caer_items=[]
    # 如果有登陆信息就显示数据库中的购物车
    if userid:
        cart=readCart(userid)
        cart.del_cart_items=del_caer_items
    request.session['cart']=cart
    return render(request,'car.html',{'nickname':nickname,
                                      'cart':cart
                                      })


# 书籍详情页
def book_intro(request):
    bookId=request.GET.get('bookid')
    nickname = request.session.get('nickname')

    bookIntro=TBook.objects.filter(book_id=bookId)[0]
    cateObj=DCategory.objects.filter(category_id=bookIntro.book_category_id)[0]


    return render(request,'Bookdetails.html',{'bookIntor':bookIntro,
                                              'nickname':nickname,
                                              'cateObj':cateObj,
                                              })





# 添加商品到购物车
def add_cart(request):
    bookid=int(request.GET.get('bookid'))
    amount=int(request.GET.get('amount'))
    cart=request.session.get('cart','')
    delBook=request.GET.get('delBook','')
    userid = request.session.get('userid')

    def add(cart):
        if cart:
            # 购物车存在
            cart.add_cart(bookid, amount)
            request.session['cart'] = cart
            if userid:
                updateSQL(cart,userid)
        else:
            # 购物车不存在
            cart = Cart()
            cart.add_cart(bookid, amount)
            request.session['cart'] = cart
            if userid:
                updateSQL(cart,userid)

    # 如果是从已删除区添加商品，走下面代码块
    if delBook:
        for i in cart.del_cart_items:
            if str(i.book.book_id)==str(bookid):
                cart.del_cart_items.remove(i)
                add(cart)
                return redirect('operapp:cart')

    # 如用户登录状态存在，则作用到数据库
    add(cart)
    return HttpResponse('ok')


# 修改购物车商品数量
def update_cart(request):

    cart =request.session.get('cart','')
    userid = request.session.get('userid')
    if userid:
        cart=readCart(userid)
    amount=request.GET.get('amount')
    bookid=request.GET.get('bookid')

    cart.change_book_amount(amount,bookid)
    request.session['cart']=cart

    userid = request.session.get('userid')
    if userid:
        updateSQL(cart, userid)
    return HttpResponse('ok')


# 删除购物车商品
def del_book(request):
    bookid=request.GET.get('bookid')
    cart=request.session.get('cart')
    cart.delete_book(bookid)
    request.session['cart']=cart

    userid = request.session.get('userid')
    if userid:
        userobj=TUser.objects.filter(user_id=userid)[0]
        bookobj=TBook.objects.filter(book_id=bookid)[0]
        Shoppingcart.objects.filter(user=userobj,bookid=bookobj)[0].delete()

    return redirect('operapp:cart')


# 读取SQL中的购物车数据
def readCart(id):
    userobj=TUser.objects.filter(user_id=id)[0]
    books = Shoppingcart.objects.filter(user=userobj)
    cart=Cart()
    # 读取数据库中的购物车信息
    for i in books:
        bookid=i.bookid.book_id
        amount=i.book_number
        cart.add_cart(bookid, amount)
    return cart


# 登录用户更新数据库中购物车
def updateSQL(cart, id):
    if cart:
        userobj=TUser.objects.filter(user_id=id)[0]
        books=Shoppingcart.objects.filter(user=userobj).all()
        for i in books:
            i.delete()
        for i in cart.cart_items:
            bookid = i.book.book_id
            amount = i.amount
            bookobj=TBook.objects.filter(book_id=bookid)[0]
            Shoppingcart.objects.create(id=bookid+userobj.user_id, bookid=bookobj, book_number=amount, user=userobj)




# ajax保存结算购物车信息
def AjaxSaveCart(request):
    bookList = request.GET.get('bookList').split(',')
    request.session['bookList'] = bookList
    total = request.GET.get('total')
    request.session['total'] = total
    return HttpResponse ('ok')



# 渲染提交订单页面
def cartSubmit(request):
    bookList = request.GET.get('bookList','').split(',')
    if bookList==['']:
        bookList=request.session.get('bookList')
    total = request.GET.get('total')
    if not total:
        total=request.session.get('total')
    request.session['bookList'] = bookList
    userid = request.session.get('userid')
    user_id = TUser.objects.filter(user_id=userid)[0]
    result = TAddress.objects.filter(user=user_id)
    nickname = request.session.get('nickname')

    return render(request,'indent.html',{'total':total,
                                         'nickname':nickname,
                                         'addressList':result
                                         })

# 处理使用历史地址请求（AJAX）
def Ajaxaddress(request):
    addressList=request.session.get('addressList')
    name=request.GET.get('name')
    for i in addressList:
        if i[0]==name:
            return JsonResponse(i,safe=False)
    return HttpResponse('no')




# 渲染订单提交成功页面
def cartSubmitOK(request):
    torderobj=request.session.get('torderobj')
    countsums=request.session.get('countsums')
    nickname = request.session.get('nickname')
    return render(request,'indent ok.html',{'torderobj':torderobj,'countsums':countsums,'nickname':nickname,})


# 处理订单提交请求
def submitOK(request):
    userid = request.session.get('userid')
    userobj = TUser.objects.filter(user_id=userid)[0]
    userID=userobj.user_id
    name=request.POST.get('name')
    region=request.POST.get('region')
    site=request.POST.get('site')
    postal_code=request.POST.get('postal_code')
    number=request.POST.get('number')
    addressFlag=request.POST.get('addressFlag')


    # 如果是新地址则存入数据库
    result=None
    if addressFlag != '1':
        addressID = str(int(time.time())) + number
        result = TAddress.objects.create(id=addressID,name=name,site=site,region=region,postal_code=postal_code,number=number,user=userobj)
    else:
        result = TAddress.objects.filter(name=name, site=site, region=region, postal_code=postal_code,number=number, user=userobj)[0]

    try:
        with transaction.atomic():
            # 添加商品到订单表
                cart = request.session.get('cart')
                total=request.POST.get('total')
                bookList = request.session.get('bookList',[])
                print(bookList,236)
                modelList=[]
                # 保存商品数量
                countsums=0
                orderID = str(int(time.time()))
                str_time = time.strftime("%Y-%m-%d %H:%M:%S")
                for i in range(len(bookList)):

                    for j in cart.cart_items:
                        if bookList[i] == j.book.book_id:
                            cart.delete_book(j.book.book_id)
                            updateSQL(cart, userID)
                            countsums += int(j.amount)

                            bookobj = TBook.objects.filter(book_id=j.book.book_id)[0]
                            dorderobj = DOrderltem.objects.create(shop_id=orderID+j.book.book_id,shop_num=j.amount,total_price =(j.book.book_dprice*int(j.amount)),shop_bookid=bookobj)
                            modelList.append(dorderobj)
                torderobj = TOrder.objects.create(id=orderID+userID, num=orderID+userID, create_date=str_time, price=total, status='0',order_uid=userobj,order_addrid=result)
                request.session['torderobj']=torderobj
                request.session['countsums']=countsums

                # 更新订单详情表外键
                for i in modelList:
                    i.shop_ordlid=torderobj
                    i.save()
    except:
        return redirect('dangdang:index')
    del request.session['cart']
    return redirect('operapp:cartSubmitOK')




# 渲染订单详情页

def Orderdetail(request):
    bookList=request.session.get('bookList')
    for i in bookList:
        pass
    return render(request,'Orderdetail.html')
