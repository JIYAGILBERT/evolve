from django import template

register = template.Library()

@register.filter
def calculate_discount(price, offer_price):
    try:
        price = float(price)
        offer_price = float(offer_price)
        if offer_price <= 0 or price <= offer_price:
            return 0
        discount = ((offer_price - price) / offer_price) * 100
        return round(discount, 2)
    except (ValueError, TypeError):
        return 0
    




register = template.Library()

@register.filter
def calculate_discount(price, offer_price):
    if offer_price and offer_price > 0:
        return int(100 - (price / offer_price * 100))
    return 0