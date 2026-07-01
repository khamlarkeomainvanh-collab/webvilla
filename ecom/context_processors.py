# context_processors.py
def cart_count(request):
    cart = request.session.get('cart', {})
    # ບວກຈຳນວນ (Value) ທັງໝົດໃນກະຕ່າ
    total = sum(int(qty) for qty in cart.values())
    return {'cart_total_items': total}