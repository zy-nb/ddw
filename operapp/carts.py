from regist.models import  *

# �鼮��
class CartItem():
    def __init__(self,book,amount):
        # book��QuerySet����
        self.book=book
        self.amount=amount

# ���ﳵ��
class Cart():
    def __init__(self):
        # ��ʡ�۸�
        self.save_price=0
        # �ܼ�
        self.total_price=0
        # ���ﳵ��Ʒ
        self.cart_items=[]
        # ɾ��������Ʒ
        self.del_cart_items=[]

     # ����۸�
    def sums(self):
        self.save_price=0
        self.total_price=0
        for i in self.cart_items:
            self.total_price +=i.book.book_dprice * int(i.amount)
            self.save_price += (i.book.book_price-i.book.book_dprice) * int(i.amount)

    # �����Ʒ
    def add_cart(self,bookid,amount):
        bookid=str(bookid)
        for i in self.cart_items:
            if i.book.book_id==bookid:
                i.amount=int(i.amount)+int(amount)
                self.sums()
                return

        self.cart_items.append(CartItem((TBook.objects.filter(book_id=bookid)[0]),amount))
        self.sums()


    # �޸���Ʒ����
    def change_book_amount(self,amount,bookid):
        for i in self.cart_items:
            if i.book.book_id == bookid:
                i.amount=int(amount)
        self.sums()

    # ɾ����Ʒ
    def delete_book(self,bookid):
        for i in self.cart_items:
            if i.book.book_id==bookid:
                self.cart_items.remove(i)
                self.del_cart_items.append(i)
        self.sums()


