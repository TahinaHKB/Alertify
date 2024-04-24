from django.shortcuts import render, HttpResponse
import requests 
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
def clear(s):
    s = s.replace('\n\t\t\t\t\t\t\t\t', '')
    s = s.replace('\n\t\t\t\t\t\t\t', '')
    s = s.replace('\n\t\t\t\t\t\t', '')
    s = s.replace('\t\t\t\t\t\t\t', '')
    return s
def scraping() : 
    page = requests.get('https://inscriptioncgm.mg/71-a2')
    soup = BeautifulSoup(page.text, 'html.parser')
    quote_elements = soup.find_all('div', class_='right-block')
    offers = []
    number = len(quote_elements)
    for t in quote_elements :
        title = t.find('a', class_='product-name').text
        price = t.find('span', class_='price product-price').text
        offer = {
        'title' : '', 
        'price' : '',
        }
        offer['title'] = clear(title)
        offer['price'] = clear(price)
        offers.append(offer)
    
    data = {
        'offers' : offers,
        "number" : str(number),
    }
    return data

@api_view(['GET'])
def send(request):
    data = scraping()
    return Response({'number': data["number"], 'offers':data['offers']})
