from django.shortcuts import render
from django.http import HttpResponse
from app.config import load_config
import json

# Create your views here.
def index(request):
    context = {"data": load_config()}
    return render(request, 'index.html', context)


def form(request):
    data = dict(request.GET)
    tickers = data['tickers']
    data['tickers'] = {}

    for ticker in tickers:
        data['tickers'][ticker] = data[ticker]
        data.pop(ticker)
    for key in data:
        if key != 'tickers':
            data[key] = data[key][0]
    with open('./app/config.json', 'w') as f:
        json.dump(data, f, indent=4)
    return HttpResponse('Success saved!')
