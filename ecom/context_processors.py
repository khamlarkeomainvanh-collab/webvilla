# context_processors.py
def cart_count(request):
    cart = request.session.get('cart', {})
    # ບວກຈຳນວນ (Value) ທັງໝົດໃນກະຕ່າ
    total = sum(int(qty) for qty in cart.values())
    total += len(request.session.get('custom_cart_items', []))

    unread_notif_count = 0
    if request.user.is_authenticated:
        try:
            from . import models
            customer = models.Customer.objects.get(user_id=request.user.id)
            unread_notif_count = customer.notifications.filter(is_read=False).count()
        except models.Customer.DoesNotExist:
            pass

    return {'cart_total_items': total, 'unread_notif_count': unread_notif_count}


def admin_missed_orders(request):
    """Pops a one-time session flag set at admin login — orders that came in
    while the admin was signed out, shown as a notification popup on the
    first admin page they land on after signing back in."""
    data = request.session.pop('admin_missed_orders', None)
    return {'admin_missed_orders_json': data}