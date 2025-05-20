# evolve/templatetags/product_filters.py
from django import template

register = template.Library()

@register.filter
def calculate_discount(price, offer_price):
    if offer_price and offer_price != 0:  # Avoid division by zero
        discount = 100 - (price / offer_price * 100)
        return round(discount)  # Round to the nearest integer
    return 0