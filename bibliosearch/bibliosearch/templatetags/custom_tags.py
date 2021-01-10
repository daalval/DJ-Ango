from bibliosearch.controllers.dbController import delete_all_data
from bibliosearch.views.buscar import MAX_ROWS
from django.template import Library
import math

register = Library()

@register.filter
def get_range( value ):
  return range(value)

@register.filter
def multiply(value, arg):
    return value * arg

@register.simple_tag
def index(indexable, i,j):
    return indexable[i * 3 + j]

@register.simple_tag
def columns(indexable,row):
    return math.ceil(len(indexable) - row * 3)

@register.simple_tag
def call_delete_all_data():
    delete_all_data()