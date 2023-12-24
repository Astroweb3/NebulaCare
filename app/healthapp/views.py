from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Data
from .serializers import DataSerializer
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors 
import os
from openai import OpenAI
# Create your views here.

def index(request):
    return render(request, 'index.html')

def med(request,data):
    api_key = "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"
    client = OpenAI(api_key = api_key)
    
    prompt = f"Generate a medical treatment proposal based:{data}"
    
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role":"system","content":"you create medical documents based on treatment proposal data."},
            {"role":"user","content":prompt}
        ]
    )
    
    Text = response.choices[0].message.content
    
    c = canvas.Canvas("prescription.pdf",pagesize = letter)
    c.setFillColor(colors.grey)
    c.setFont("Helvetica-bold",24)
    c.drawString(50,700,"NebulaCare MedAI")
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica",14)
    c.drawString(50,660, Text)
    
    image_path = os.path.join(os.getcwd(),"MedAi.png")
    c.drawImage(image_path,50,400,width = 150,height = 150)
    
    c.save()
    
    a = {"context":Text}
    return render(request,"index.html",a)


@api_view(['POST'])
def postData(request):
    sym = str(request.POST["sym"])
    name = str(request.POST["Patient_Name"])
    
    dek = {"name":name,
           "description":sym}
    serializer = DataSerializer(data = dek)
    if serializer.is_valid():
        serializer.save()
    return med(request,serializer.data)