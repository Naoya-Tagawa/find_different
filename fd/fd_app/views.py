from django.shortcuts import render,get_object_or_404
from .forms import Upload,SettingForm,input_img,output_img
from .models import UploadImage
import cv2
import numpy as np
from PIL import Image
import io
def index(request):
    params = {
        'title':'画像のアップロード',
        'upload_form':Upload(),
        'id':None,
        'url':None,
    }
    
    if (request.method == 'POST'):
        form = Upload(request.POST,request.FILES)
        if form.is_valid():
            upload_img = form.save()
            #upload_img.img.delete()
            
            params['id'] = upload_img.id
            params['url'] = upload_img.img.url
        print(params['url'])
    return render(request,'fd_app/home.html',params)
#renderすることでhome.htmlを表示させている。最初に出るのはindex
def home(request,image_id):
    upload_img = get_object_or_404(UploadImage,id = image_id)
    
    params = {
        'title':'画像のアップロード',
        'upload_form':Upload(),
        'id':image_id,
        'url':upload_img.img.url,
    }
    
    if (request.method == 'POST'):
        form = Upload(request.POST,request.FILES)
        if form.is_valid():
            upload_img = form.save()
            #upload_img.img.delete()
            
            params['id'] = upload_img.id
            params['url'] = upload_img.img.url
            #delete(upload_img.id)
            
    return render(request,'fd_app/home.html',params)

def preview(request,image_id):
    print(image_id)
    form = Upload(request.POST,request.FILES)
    #upload_img = UploadImage.objects.get(id = image_id)
    upload_img = get_object_or_404(UploadImage,id=image_id)
    params = {
        'title': '画像の表示',
        'id':upload_img.id,
        'url':upload_img.img.url
    }
    print(params['url'])
    return render(request, 'fd_app/preview.html', params)

def transform(request, image_id=0):
    #get_object_or_404(クラス名,引数)
    #対象のオブジェクトを取得、取得できない場合は404頁を返す
    upload_img = get_object_or_404(UploadImage, id=image_id)
    if (request.method == 'POST'):
        form = SettingForm(request.POST)
        
        if form.is_valid():
            #cleaned_dataはデータベースから取ってきて消す
            angle = form.cleaned_data.get('angle')
            gray = form.cleaned_data.get('gray')

            upload_img.transform(angle, gray)

            params = {
                'title': '画像処理',
                'id': upload_img.id,
                'setting_form': form,
                'original_url': upload_img.img.url,
                'result_url': upload_img.result_img.url
            }

            return render(request, 'fd_app/transform.html', params)


    params = {
        'title': '画像処理',
        'id': upload_img.id,
        'setting_form': SettingForm({'angle':0, 'gray':False}),
        'original_url': upload_img.img.url,
        'result_url': ''
    }

    return render(request, 'fd_app/transform.html', params)
# Create your views here.

def input_form(request):
    params = {
        'title':'間違い探し',
        'input_upload':input_img(),
        'output_upload':output_img(),
        'input_id':None,
        'input_url':None,
        #'output_id':None,
        #'output_url':None,
        'deal':None,
    }
    
    if (request.method == 'POST'):
        form = input_img(request.POST,request.FILES)
        if form.is_valid():
            upload_img = form.save()
            #upload_img.img.delete()
            print("gggggggggggggggg")
            params['input_id'] = upload_img.id
            params['input_url'] = upload_img.img.url
        #print(params['id'])
    return render(request,'fd_app/find.html',params)

#form.as_pは「formの内容をpタグで囲って表示
def output_form(request,image_id):
    params = {
        'title':'間違い探し(支援)',
        'input_upload':input_img(),
        'output_upload':output_img(),
        'input_id':None,
        'input_url':None,
        'output_id':None,
        'output_url':None,
        'deal':None,
    }
    inputed_img = get_object_or_404(UploadImage,id=image_id)
    print(type(inputed_img))
    if (request.method == 'POST'):
        form = output_img(request.POST,request.FILES)
        if form.is_valid():
            upload_img = form.save()
            #upload_img.img.delete()
            
            params['output_id'] = upload_img.id
            params['output_url'] = upload_img.result_img.url
            params['input_id'] = image_id
            params['input_url'] = inputed_img.img.url
        print(params['output_id'])
    return render(request,'fd_app/find.html',params)

def delete(request,image_id):
    if (request.method == 'POST'):
        upload_img = get_object_or_404(UploadImage,id=image_id)
        upload_img.img.delete()
        upload_img.delete()
        
    return render(request,'fd_app/delete_img.html')

def find_different(request,input_id,input_url2):
    params = {
        'title':'白く浮かび上がるところを参考に間違い探しをしてください',
        'input_upload':input_img(),
        'output_upload':output_img(),
        'input_id':None,
        'input_url':None,
        'output_id':None,
        'output_url':None,
        'deal':None,
    }
    if (request.method == 'POST'):
        input_image1 = get_object_or_404(UploadImage,id=input_id)
        input_image2 = get_object_or_404(UploadImage,id=input_url2)
        
        print(input_image2.result_img.url)
        input_image1.find_difference(input_image2.result_img.url)
    
        params['output_url'] = input_image1.result_img.url
        params['deal'] = 1
        params['input_id'] = input_id
        params['input_url'] = input_image1.img.url
        
    return render(request,'fd_app/find.html',params)
            