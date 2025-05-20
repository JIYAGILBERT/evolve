def cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())  # Sum of quantities
    return {'cart_count': cart_count}