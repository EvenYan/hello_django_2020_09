from django.shortcuts import render
from django.http import HttpResponse
import json
from first_app.models import UserInfo, Host
import hashlib
import os
from hello_django.settings import BASE_DIR


# Create your views here.

def index(request):
    return HttpResponse("Hello Django!")


def ret_json_data(request):
    face_dict = {'ImageWidth': 1824, 'ImageHeight': 2736, 
             'FaceInfos': [{'X': 385, 'Y': 134, 'Width': 1055, 
              'Height': 1417, 'FaceAttributesInfo': 
              {'Gender': 0, 'Age': 21, 'Expression': 15, 'Glass': False,
              'Pitch': 9, 'Yaw': 7, 'Roll': 8, 'Beauty': 93, 
               'Hat': False, 'Mask': False, 'Hair': 
                     {'Length': 3, 'Bang': 1, 'Color': 0}, 'EyeOpen': True}, 
                     'FaceQualityInfo': {'Score': 0, 'Sharpness': 0, 
                      'Brightness': 0, 'Completeness': 
                            {'Eyebrow': 0, 'Eye': 0, 'Nose': 0, 'Cheek': 0, 
                             'Mouth': 0, 'Chin': 0
                }}}], 'FaceModelVersion': '2.0',
             'RequestId': 'ea82f374-f6a6-48bd-a4c0-5035e7ea87a6'}
    return HttpResponse(json.dumps(face_dict), \
        content_type="application/json")


def insert_data(request):
    name = request.GET.get("name")
    age = request.GET.get("age")
    passwd = request.GET.get("password")
    UserInfo.objects.create(name=name, age=age, password=passwd)
    return HttpResponse("数据插入成功！")


def get_data(request):
    user_list = UserInfo.objects.all().values()
    user_list = list(user_list)
    print(user_list)
    return HttpResponse(json.dumps(user_list), \
        content_type="application/json")

def upload_data(request):
    return render(request, "first_app/upload.html")


def upload_file(request):
    return render(request, "first_app/upload_file.html")


def deal_upload_file(request):
    file = request.FILES.get("demo_file")
    path = os.path.join(BASE_DIR, "resources", file.name)
    if not file:
        HttpResponse("文件为空，请先选择文件！")
    with open(path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)
    return HttpResponse("Sucess!")

def save_data(request):
    name = request.POST.get("username")
    age = request.POST.get("age")
    password = request.POST.get("password")
    sha512 = hashlib.sha512()
    sha512.update(password.encode("utf-8"))
    password = sha512.hexdigest()
    UserInfo.objects.create(name=name, age=age, password=password)
    return HttpResponse("数据提交成功！")


def upload_script(request):
    return render(request, "first_app/upload_script.html")


def handout_script(request):
    import os
    from hello_django.settings import BASE_DIR
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        path = os.path.join(BASE_DIR, "resources", myFile.name)
        if not myFile:
            return HttpResponse("no files for upload!")
        destination = open(path,'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        handout_script_to_host(path)
        # return HttpResponse("upload over!")
        return HttpResponse("脚本下发成功！")


def handout_script_to_host(path):
    import paramiko
    import os
    hostname = "192.168.101.89"
    username = "root"
    password = "root"
    port = 22
    try:
        file = os.path.basename(path)
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(path, os.path.join("/data", file))
        t.close()
    except Exception as e:
        print(e)
    return 


def scan_host(request):
    import os
    import nmap
    from hello_django.settings import BASE_DIR

    scan_row=[]
    input_data = "192.168.101.0/24 22"
    scan_row = input_data.split(" ")
    if len(scan_row)!=2:
        print('Input errors,example \"192.168.1.0/24 80,443,22\"')
    hosts=scan_row[0]    #接收用户输入的主机
    port=scan_row[1]    #接收用户输入的端口

    try:
        nm = nmap.PortScanner()    #创建端口扫描对象
    except Exception as e:
        print("Unexpected error:")

    try:
        nm.scan(hosts=hosts, arguments=' -v -sS -p '+port)    #调用扫描方法，参数指定扫描主机hosts，nmap扫描命令行参数arguments
    except Exception as e:
        print("Scan erro:"+str(e))
    with open(os.path.join(BASE_DIR, 'resources', 'hosts'), 'w+', encoding='utf-8') as f:
        for host in nm.all_hosts():    #遍历扫描主机
            if nm[host].state()=="up":
                print('----------------------------------------------------')
                print('Host : %s (%s)' % (host, nm[host].hostname()))    #输出主机及主机名
                print('State : %s' % nm[host].state())    #输出主机状态，如up、down
                f.write(host)
                f.write("\n")
                f.write(nm[host].state())
                f.write("\n")
    return HttpResponse("主机扫描完成！")



def search_host_info(request):
    return render(request, "first_app/search_host.html")


def get_host_info(request):
    import json
    import datetime
    ip = request.GET.get("ip")
    print(ip)
    info_list = Host.objects.filter(ip=ip).order_by("createtime").values_list("createtime", "mem")
    time_list = [info[0].strftime("%H:%M") for info in info_list[::20]]
    mem_list = [info[1] for info in info_list[::20]]
    print(time_list, mem_list)
    context = {"time_list":time_list, "mem_list": mem_list}
    return HttpResponse(json.dumps(context))