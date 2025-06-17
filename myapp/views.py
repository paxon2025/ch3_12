from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt






#Create your views here.
def search_list(request):
    if 'cName' in request.GET:
        cName = request.GET['cName']
        print(cName)
        #resultlist = students.objects.filter(cName=cName)
        resultlist = students.objects.filter(cName__contains=cName)
    else:
        resultlist = students.objects.all()
    
    errorMessage = ""
    if not resultlist:
        errorMessage = "無此資料"


    # for data in resultlist:
    #     print(model_to_dict(data))
    #return HttpResponse("Hello World")
    return render(request,"search_list.html",locals()) 

def index(request):
    if "site_search" in request.GET:
        site_search = request.GET["site_search"]
        site_search = site_search.strip() #去前後空白
        #print(site_search)
        #一個關鍵字，搜尋一個欄位
        #resultlist = students.objects.filter(cName__contains=site_search)
        #一個關鍵字，搜尋多個欄位
        # resultlist = students.objects.filter(
        #     Q(cName__contains=site_search) |
        #     Q(cBirthday__contains=site_search) |
        #     Q(cEmail__contains=site_search) |
        #     Q(cPhone__contains=site_search) |
        #     Q(cAddr__contains=site_search)
        # )
        #多個關鍵字，搜尋多個欄位
        keywords=site_search.split()
        print(keywords)
        #resultlist = []
        q_object = Q()
        for keyword in keywords:
            q_object.add(Q(cName__contains=keyword),Q.OR)
            q_object.add(Q(cBirthday__contains=keyword),Q.OR)
            q_object.add(Q(cEmail__contains=keyword),Q.OR)
            q_object.add(Q(cName__contains=keyword),Q.OR)
            q_object.add(Q(cName__contains=keyword),Q.OR)
        resultlist=students.objects.filter(q_object)
    else:
        resultlist = students.objects.all().order_by("cID")
    dataCount = len(resultlist)
    status = True
    errormessage=""
    if not resultlist:
        status = False
        errormessage = "無此資料"
    
        # print(dataCount)
    

    #分頁設定，每頁顯示3筆
    # from django.db.models import Q
    # from django.core.paginator import Paginator
    paginator = Paginator(resultlist,2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) #根據取得page_number，取得對應頁數的資料
    # page_obj 包含該頁資料的物件
    # page_obj.object_list:該頁資料
    # page_obj.has_next,page_obj.has_next:是否有下一頁，上一頁頁碼
    # page_obj.number: 目前的頁碼
    # paginator.num_pages:總頁數

    return render(request,"index.html",locals()) 

def post(request):
    if request.method == "POST":
        cName=request.POST["cName"]
        cSex=request.POST["cSex"]
        cEmail=request.POST["cEmail"]
        cPhone=request.POST["cPhone"]
        cAddr=request.POST["cAddr"]
        print(f"cName:{cName}\t,cSex:{cSex}\t,cEmail:{cEmail}\t,cPhone:{cPhone}\t,cAddr:{cAddr}\t") # html把資料抓回來
        # 資料存到 orm 
        add= students(cName=cName,cSex=cSex,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        add.save()
        return redirect('/index/')
    else:
        return render(request,"post.html",locals()) 
        
def edit(request,id=None):
    print(f"id={id}")
    if request.method == "POST":
        cName=request.POST["cName"]
        cSex=request.POST["cSex"]
        cEmail=request.POST["cEmail"]
        cPhone=request.POST["cPhone"]
        cAddr=request.POST["cAddr"]
        print(f"cName:{cName}\t,cSex:{cSex}\t,cEmail:{cEmail}\t,cPhone:{cPhone}\t,cAddr:{cAddr}\t") 
        #orm
        update = students.objects.get(cID=id)
        update.cName = cName
        update.cSex = cSex
        update.cEmail = cEmail
        update.cPhone = cPhone
        update.cAddr = cAddr
        update.save()
        return redirect('/index/')
        #return HttpResponse("Hello Edit")
    else:
        obj_data = students.objects.get(cID=id)
        print(model_to_dict(obj_data))
        return render(request,"edit.html",locals())
    
def delete(request,id=None):
    print(f"id={id}")
    if request.method == "POST":
        delete_data = students.objects.get(cID=id)
        delete_data.delete()
        return redirect('/index/')
        #return HttpResponse("Hello delete")
    else:
        obj_data = students.objects.get(cID=id)
        print(model_to_dict(obj_data))
        return render(request,"delete.html",locals())
    
def getallitems(request):
    resultlistObject = students.objects.all().order_by("cID")
    # for data in resultlistObject:
    #     print(model_to_dict(data))
    # querySet->object 轉成list ->dict
    resultListDict= list(resultlistObject.values())
    return JsonResponse(resultListDict,safe=False)
    #return HttpResponse("Hello getallitems")

def getitem(request,id=None):
    print(f"id={id}")
    resultListObj= students.objects.filter(cID=id) #要用 filter
    #print(type(resultListObj))
    # print(resultListObj.values())
    # print(type(resultListObj.values()))
    if not resultListObj.exists():
        return JsonResponse({"message":"無此資料"},safe=False)     
    resultListDict=list(resultListObj.values())
    print(resultListDict)
    # print()
    # print(type(resultListDict))
    return JsonResponse(resultListDict,safe=False)

    #print(model_to_dict(resultlist))
    
    #return HttpResponse("hello getitem")
@csrf_exempt
def createItem(request):
    if request.method == "GET":
        cName=request.GET["cName"]
        cSex=request.GET["cSex"]
        cBirthday=request.GET["cBirthday"]
        cEmail=request.GET["cEmail"]
        cPhone=request.GET["cPhone"]
        cAddr=request.GET["cAddr"]
        print(f"cName:{cName}\t,cSex:{cSex}\t,cBirthday:{cBirthday}\t,cEmail:{cEmail}\t,cPhone:{cPhone}\t,cAddr:{cAddr}\t")
    elif request.method == "POST":
        cName=request.POST["cName"]
        cSex=request.POST["cSex"]
        cBirthday=request.POST["cBirthday"]
        cEmail=request.POST["cEmail"]
        cPhone=request.POST["cPhone"]
        cAddr=request.POST["cAddr"]
        print(f"cName:{cName}\t,cSex:{cSex}\t,cBirthday:{cBirthday}\t,cEmail:{cEmail}\t,cPhone:{cPhone}\t,cAddr:{cAddr}\t")
    try:
        add= students(cName=cName,cSex=cSex,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        add.save()
    except:
        return JsonResponse({"message":"缺少資料"})
        
    #return HttpResponse("hello createItem")

@csrf_exempt
def upadteItem(request,id=None):
    print(f"id={id}")
    try:
        if request.method == "GET":
            cName=request.GET["cName"]
            cSex=request.GET["cSex"]
            cBirthday=request.GET["cBirthday"]
            cEmail=request.GET["cEmail"]
            cPhone=request.GET["cPhone"]
            cAddr=request.GET["cAddr"]
            print(f"cName:{cName}\t,cSex:{cSex}\t,cBirthday:{cBirthday}\t,cEmail:{cEmail}\t,cPhone:{cPhone}\t,cAddr:{cAddr}\t")
        elif request.method == "POST":
            cName=request.POST["cName"]
            cSex=request.POST["cSex"]
            cBirthday=request.POST["cBirthday"]
            cEmail=request.POST["cEmail"]
            cPhone=request.POST["cPhone"]
            cAddr=request.POST["cAddr"]
            print(f"cName:{cName}\t,cSex:{cSex}\t,cBirthday:{cBirthday}\t,cEmail:{cEmail}\t,cPhone:{cPhone}\t,cAddr:{cAddr}\t")
    except:
        return JsonResponse({"message":"缺少資料"},safe=False)
    try:
        #ORM
        update = students.objects.get(cID=id)
        update.cName = cName
        update.cSex = cSex
        update.cEmail = cEmail
        update.cPhone = cPhone
        update.cAddr = cAddr
        update.save()
        return JsonResponse({"message":"更新成功"},safe=False)
    except:
        return JsonResponse({"message":"更新失敗，無此資料"},safe=False)
    

    #return HttpResponse("hello updateItem")

@csrf_exempt
def deleteItem(request,id=None):
    print(f"id={id}")
    try:
        delete_data = students.objects.get(cID=id)
        delete_data.delete()
        return JsonResponse({"message":"刪除成功"},safe=False)
    except:
        return JsonResponse({"message":"刪除失敗"},safe=False)
        #注意此為JsonResponse
    
    #return HttpResponse("hello deleteItem")