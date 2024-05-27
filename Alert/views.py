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
    s = s.replace('\n\t\t', '')
    s = s.replace('\t\n', '')
    s = s.replace('\t', '')
    return s

def scrap() : 
    page = requests.get('https://inscriptioncgm.mg')
    soup = BeautifulSoup(page.text, 'html.parser')
    quote_elements = soup.find('div', class_='sf-contener clearfix col-lg-12')
    bloc = quote_elements.find_all('li')
    i = 0
    exam = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    point = 0
    number = 0
    offers = []
    for b in bloc : 
        if i >= 3 : 
            url = b.find('a')['href']
            off = scraping(url, exam[point])
            number += len(off)
            point = point+1
            offers.append(off)
        i = i+1
    data = {
        'offers' : offers,
        "number" : str(number),
    }
    return data
def scraping(url, type) : 

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    quote_elements = soup.find_all('div', class_='right-block')
    offers = []
    number = len(quote_elements)
    for t in quote_elements :
        title = t.find('a', class_='product-name').text
        price = t.find('span', class_='price product-price').text
        availability = t.find('span', class_='availability').text
        offer = {
        'category' : '',
        'title' : '', 
        'price' : '',
        'availability' : '',
        }
        offer['title'] = clear(title)
        offer['price'] = clear(price)
        offer['availability'] = clear(availability)
        offer['category'] = type
        offers.append(offer)
    
    return offers

@api_view(['GET'])
def send(request):
    data = scrap()
    return Response({'number': data["number"], 'offers':data['offers']})
