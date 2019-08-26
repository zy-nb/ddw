from regist.models import  *

# 书籍类
class CartItem():
    def __init__(self,book,amount):
        # book即QuerySet对象
        self.book=book
        self.amount=amount

# 购物车类
class Cart():
    def __init__(self):
        # 节省价格
        self.save_price=0
        # 总价
        self.total_price=0
        # 购物车商品
        self.cart_items=[]
        # 删除掉的商品
        self.del_cart_items=[]

     # 计算价格
    def sums(self):
        self.save_price=0
        self.total_price=0
        for i in self.cart_items:
            self.total_price +=i.book.book_dprice * int(i.amount)
            self.save_price += (i.book.book_price-i.book.book_dprice) * int(i.amount)

    # 添加商品
    def add_cart(self,bookid,amount):
        bookid=str(bookid)
        for i in self.cart_items:
            if i.book.book_id==bookid:
                i.amount=int(i.amount)+int(amount)
                self.sums()
                return

        self.cart_items.append(CartItem((TBook.objects.filter(book_id=bookid)[0]),amount))
        self.sums()


    # 修改商品数量
    def change_book_amount(self,amount,bookid):
        for i in self.cart_items:
            if i.book.book_id == bookid:
                i.amount=int(amount)
        self.sums()

    # 删除商品
    def delete_book(self,bookid):
        for i in self.cart_items:
            if i.book.book_id==bookid:
                self.cart_items.remove(i)
                self.del_cart_items.append(i)
        self.sums()


