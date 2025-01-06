from django.shortcuts import render,HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from .models import Student 
from .models import EntryExitTime

from twilio.rest import Client
from django.conf import settings
import easyocr
import base64
from PIL import Image
from io import BytesIO
import re
import datetime

@csrf_exempt
def getIndexPage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.user.is_authenticated)
            base64_image_data = request.POST['snapshotData']
            data=base64_image_data.split(',')
            base64_image_data=data[1]
            reader = easyocr.Reader(['en'])
            image_data = base64.b64decode(base64_image_data)
            image = Image.open(BytesIO(image_data))
            result = reader.readtext(image)
            extracted_text = ' '.join([entry[1] for entry in result])
            print("Extracted Text:", extracted_text)
            match = re.search(r'\b[A-Z0-9]{10}\b', extracted_text)
            if match:
                extracted_number = match.group(0)
                print("Extracted Number:", extracted_number)
                try:
                    stu=Student.objects.get(id=extracted_number)
                except:
                    return render(request,"index.html",{"msg":"student data doesnot matched",'color':'red'})
                objs=EntryExitTime.objects.filter(stu=stu).order_by("-EntryTime")
                data=objs.values()
                if data:
                    if str(data[0]['EntryTime'])[:10] == str(datetime.datetime.now())[:10]:
                        print(str(data[0]['ExitTime'])=="None")
                        if str(data[0]['ExitTime'])=="None":
                            obj=EntryExitTime.objects.filter(stu=Student.objects.get(id=extracted_number),EntryTime=data[0]['EntryTime'])
                            obj.update(ExitTime=timezone.now())
                            return render(request,"index.html",{"msg":"exited @"+str(timezone.now()),'color':"green"})
                        else:
                            obj=EntryExitTime(stu=Student.objects.get(id=extracted_number),EntryTime=timezone.now())
                            obj.save()
                            return render(request,"index.html",{"msg":"Entry @"+str(timezone.now()),'color':'green'})
                    elif str(data[0]['EntryTime'])[:10] < str(datetime.datetime.now())[:10]:
                        obj=EntryExitTime(stu=Student.objects.get(id=extracted_number),EntryTime=timezone.now())
                        obj.save()
                        return render(request,"index.html",{"msg":"Entry @"+str(timezone.now()),'color':'green'})
                else:
                    obj=Student.objects.get(id=extracted_number)
                    if obj:
                        obj=EntryExitTime(stu=Student.objects.get(id=extracted_number),EntryTime=timezone.now())
                        obj.save()
                        return render(request,"index.html",{"msg":"Entry @"+str(timezone.now()),'color':'green'})
                    else:
                        return render(request,"home.html",{"msg":"no record found with the extracted info",'color':'red'})
            else:
                return render(request,"index.html",{"msg":"no data is extracted",'color':'red'})
        return render(request,"index.html")
    else:
        return HttpResponseRedirect('login/')
def loginView(request):
    if request.method == "POST":
        uname=request.POST['username']
        upass=request.POST['password']
        print(uname,upass)
        user=authenticate(username=uname,password=upass)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        return render(request,"login.html",{'msg':'username  name or  password is wrong','color':'red'})
    return render(request,"login.html")
def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('../login/')

def send_whatsapp_message(request):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Hello, this is a WhatsApp message!",
        from_=f"whatsapp:{+19382532165}",
        to="whatsapp:7842166999"  # Replace with the recipient's phone number
    )

    return render(request, 'success.html', {'message_sid': message.sid})