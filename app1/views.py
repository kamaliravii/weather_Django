from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import CityForm
from .models import City
import requests

# Create your views here.
# weatheapi.com
def home(request):
    url='https://api.weatherapi.com/v1/current.json?key=ec2febfb52934f67aa9100740242402&q={}&aqi=yes'
    if request.method=='POST':
        form=CityForm(request.POST)
        if form.is_valid():
            ncity=form.cleaned_data["name"]
            ccity=City.objects.filter(name=ncity).count()
            if ccity==0:
                res=requests.get(url.format(ncity)).json()
                if res['location']:
                    form.save()
                    messages.success(request,"Success..")
                else:
                    messages.warning(request,"City not found...!")
            else:
                messages.warning(request,"City already existed...!")
    form=CityForm()
    Citys=City.objects.all()
    data=[]
    for city in Citys:
        res=requests.get(url.format(city)).json()
        city_data={
            'cityname':city,
            'tempc':res['current']['temp_c'],
            'tempf':res['current']['temp_f'],
            'condition':res['current']['condition']['text'],
            'icon':res['current']['condition']['icon']
            }
        data.append(city_data)

    return render(request,"index.html",{'city':Citys,'datas':data,'form':form})

def deletecity(request,cname):
    City.objects.get(name=cname).delete()
    messages.warning(request,"Deleted successfully..!")
    return redirect('/')