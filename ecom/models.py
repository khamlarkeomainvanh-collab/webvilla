from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Category(models.Model):
    name = models.CharField(max_length=60)
    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """A body-type/sub-group within a Category (e.g. ລົດໃຫຍ່ → SUV, Pickup, MPV)."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name     = models.CharField(max_length=60)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.category.name} → {self.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name=models.CharField(max_length=40)
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=500)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.name

    @property
    def total_stock_qty(self):
        return sum(c.stock_qty for c in self.colors.all())

    @property
    def total_remaining_qty(self):
        return sum(c.remaining_qty for c in self.colors.all())


class ProductImage(models.Model):
    """An extra gallery photo for a Product, beyond its primary product_image —
    lets the customer swipe through up to 5 photos total in the detail view."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='extra_images')
    image   = models.ImageField(upload_to='product_image/gallery/')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.product.name} — photo #{self.id}"


class ProductColor(models.Model):
    """A single color variant of a Product, with its own stock ledger —
    admin sets stock_qty when receiving units and sold_qty as they sell."""
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color_name = models.CharField(max_length=40)
    stock_qty  = models.PositiveIntegerField(default=0)
    sold_qty   = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['id']

    @property
    def remaining_qty(self):
        return max(self.stock_qty - self.sold_qty, 0)

    def __str__(self):
        return f"{self.product.name} — {self.color_name}"


STATUS_CHOICES = (
    ('Pending',    'ລໍຖ້າການຢືນຢັນ'),
    ('Confirmed',  'ຮັບ/ຢືນຢັນອໍເດີ'),
    ('Processing', 'ກຳລັງຈັດສົ່ງ'),
    ('Delivered',  'ຈັດສົ່ງສຳເລັດ'),
    ('Cancelled',  'ຍົກເລີກ'),
)


class Orders(models.Model):
    customer    = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    product     = models.ForeignKey('Product',  on_delete=models.CASCADE, null=True)
    quantity    = models.PositiveIntegerField(default=1)
    amount      = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    order_group = models.CharField(max_length=36, null=True, blank=True)
    email       = models.CharField(max_length=50,  null=True)
    address     = models.CharField(max_length=500, null=True)
    mobile      = models.CharField(max_length=20,  null=True)
    order_date     = models.DateTimeField(auto_now_add=True, null=True)
    status         = models.CharField(max_length=50, null=True, choices=STATUS_CHOICES, default='Pending')
    delivery_type  = models.CharField(max_length=20, null=True, blank=True, default='Delivery')
    delivery_km    = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    delivery_fee   = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    payment_method = models.CharField(max_length=20, null=True, blank=True, default='COD')
    note           = models.CharField(max_length=300, blank=True, default='')
    # Set only for "ຈອງລ່ວງໜ້າ" (advance booking) orders — the day/time the
    # customer will come collect it, instead of being prepared/queued today.
    pickup_date    = models.DateField(null=True, blank=True)
    pickup_time    = models.TimeField(null=True, blank=True)
    # Set when an advance booking is actually collected (marked "ຮັບແລ້ວ") —
    # revenue for advance bookings counts on this day, not the booking day.
    fulfilled_at   = models.DateTimeField(null=True, blank=True)



class Feedback(models.Model):
    name = models.CharField(max_length=40)
    feedback = models.TextField(max_length=500) # ປ່ຽນເປັນ TextField ເພື່ອໃຫ້ກອກໄດ້ຍາວ
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


ANNOUNCEMENT_KIND_CHOICES = (
    ('closed', 'ປິດຮ້ານ'),
    ('promo',  'ໂປໂມຊັ່ນ'),
)


class Announcement(models.Model):
    kind       = models.CharField(max_length=10, choices=ANNOUNCEMENT_KIND_CHOICES, default='promo')
    title      = models.CharField(max_length=100)
    message    = models.CharField(max_length=300, blank=True, default='')
    icon       = models.CharField(max_length=10, blank=True, default='📢')
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'[{self.kind}] {self.title}'


class CustomOrderRequest(models.Model):
    customer    = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    message     = models.CharField(max_length=300)
    created_at  = models.DateTimeField(auto_now_add=True)
    is_done     = models.BooleanField(default=False)
    order_group = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.message[:40]


class FinanceSettings(models.Model):
    """Singleton row holding the admin-editable profit-margin percentage used
    on the finance dashboard: profit = revenue * (profit_percent / 100)."""
    profit_percent = models.DecimalField(max_digits=5, decimal_places=2, default=30)

    def __str__(self):
        return f"ອັດຕາກຳໄລ {self.profit_percent}%"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


EXPENSE_CATEGORY_CHOICES = (
    ('ອະໄຫຼ່ລົດ', 'ອະໄຫຼ່ລົດ'),
    ('ແບັດເຕີຣີ', 'ແບັດເຕີຣີ'),
    ('ຄ່າຂົນສົ່ງ', 'ຄ່າຂົນສົ່ງ'),
    ('ຄ່າໂຄສະນາ', 'ຄ່າໂຄສະນາ'),
    ('ຄ່າພະນັກງານ', 'ຄ່າພະນັກງານ'),
    ('ຄ່າເຊົ່າຮ້ານ', 'ຄ່າເຊົ່າຮ້ານ'),
    ('ຄ່າໄຟ/ນ້ຳ', 'ຄ່າໄຟ/ນ້ຳ'),
    ('ອຸປະກອນຮ້ານ', 'ອຸປະກອນຮ້ານ'),
    ('ອື່ນໆ', 'ອື່ນໆ'),
)


class Expense(models.Model):
    date        = models.DateField()
    # Free text — EXPENSE_CATEGORY_CHOICES above still seeds the quick-pick list in the
    # admin UI, but the field itself accepts any category name the admin types in.
    category    = models.CharField(max_length=30, default='ອື່ນໆ')
    description = models.CharField(max_length=200, blank=True, default='')
    amount      = models.PositiveIntegerField()

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.date} | {self.category} | {self.amount:,} ກີບ"


class CustomerNotification(models.Model):
    """In-site order-status inbox — shown on the customer's my-order page so
    status updates reach them even if they never enabled browser push."""
    customer   = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='notifications')
    title      = models.CharField(max_length=200)
    body       = models.CharField(max_length=500)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f"{self.customer} | {self.title}"
