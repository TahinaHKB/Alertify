from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
import requests 
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django_globals import globals
# Create your views here.
def clear(s):
    s = s.replace('\n\t\t\t\t\t\t\t\t', '')
    s = s.replace('\n\t\t\t\t\t\t\t', '')
    s = s.replace('\n\t\t\t\t\t\t', '')
    s = s.replace('\t\t\t\t\t\t\t', '')
    s = s.replace('\n\t\t', '')
    s = s.replace('\t\n', '')
    s = s.replace('\t', '')
    s = s.replace('\n\t\t', '')
    s = s.replace('\t\n', '')
    s = s.replace('\t', '')
    return s

def scrap(request) : 
    page = requests.get('https://inscriptioncgm.mg')
    soup = BeautifulSoup(page.text, 'html.parser')
    quote_elements = soup.find('div', class_='sf-contener clearfix col-lg-12')
    bloc = quote_elements.find_all('li')
    i = 0
    exam = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    number = 0
    offers = []
    lvlNumber = request.session.get("level")
    for b in bloc : 
        if str(i) in lvlNumber: 
            url = b.find('a')['href']
            off = scraping(url, exam[i-3])
            number += len(off)
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

def send(request, nb):
    data = scrap(request)
    request.session["nb"] = data["number"]
    request.session["offers"] = data["offers"]
    if nb < int(data["number"]) and nb>0: 
        send_mail('Examen CGM ALERTE', 'Un nouveau examen vient d\'apparaitre', 'tahinaandriantsoa2004.com', ['myhkb.tah@gmail.com', 'hobyraobison@gmail.com'],
              fail_silently=False)
        return JsonResponse({"msg" : "Positive", "nb" : data["number"], "n" : nb,})
    else : 
        return JsonResponse({"msg" : "Negative", "nb" : data["number"], "n" : nb})
    # return Response({'number': data["number"], 'offers':data['offers']})

def trans(lvl):
    if lvl == "3" : return "A1"
    elif lvl == "4" : return "A2"
    elif lvl == "5" : return "B1"
    elif lvl == "6" : return "B2"
    elif lvl == "7" : return "C1"
    elif lvl == "8" : return "C2"

def home(request):
    if request.method=='POST' : 
        request.session["level"] = request.POST.getlist('level')
    request.session["levelEcrit"] = list()
    for l in request.session.get("level") : 
        request.session["levelEcrit"].append(trans(l))
    return render(request, 'home.html', {
        "lvl" : request.session.get("levelEcrit"),
        "nb" : request.session.get("nb"),
    })

def connection(request):
    request.session["level"] = ""
    request.session["nb"] = 0
    request.session["offers"] = ""
    request.session["levelEcrit"] = list()
    return redirect("home/")
