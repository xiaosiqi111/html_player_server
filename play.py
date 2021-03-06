#-*- coding: UTF-8 -*-
from flask import Flask , url_for,send_from_directory, render_template ,request,redirect
from flask_cors import CORS
import os, sys

app = Flask(__name__)
CORS(app, supports_credentials=True)

video_format = ( 'WEBM', 'MP4', 'OGG','FLV','AAC','MOV','MKV','M3U8')
photo_format = ( 'JPEG', 'PNG', 'GIF','JPG','BMP')

def get_file_list(file_path, sort_typt="1"):#返回按日期排序的文件列表
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        if sort_typt=="1": #文件名升序
            dir_list.sort(reverse = False)
        if sort_typt == "2":#文件名升序文件名降序
            dir_list.sort(reverse = True)
        if sort_typt=="3":#文件名升序文件名降序时间升序
        # os.path.getmtime()函数是返回最近文件修改时间

            dir_list = sorted(dir_list,  key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        if sort_typt == "4":  # 文件名升序文件名降序时间降序
            dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)), reverse=True)
        return dir_list



@app.route('/')
def index():
    files = get_file_list('static/file')
    file_type = []
    for file in files: #拿到目录下的所有的文件夹和文件名，判断文件类型
        if os.path.isdir('static/file/'+ file):
            file_type.append([file, "文件夹"])
        else:
            file_type.append([file, file.split(".")[-1]])
    return render_template('index.html', file_type=file_type, dir="/",sort_typt=1)


@app.route('/file/')
def play():
    file_path = request.args.get('file_path') #文件路径
    sort_typt = request.args.get('sort_typt') #排序方式
    print(file_path)
    print(sort_typt)
    user_agent = request.headers.get('User-Agent')
    #得到用户浏览器的类型
    file_path=file_path.replace('&','/')
    print(file_path)
    #在get 传文件路路径时，使用“&”作为分隔符，在程序内部使用“/”作为分隔符，在这里进行转换

    if os.path.isdir('static/file/' + file_path) : #判断路径是否为文件夹，是则返回文件列表模板
        files = get_file_list('static/file/'+ file_path,sort_typt)
        file_type=[]
        if files is not None:#判断文件夹是否为空
            for file in files:#拿到该目录下的所有的文件夹和文件名，判断文件类型
                if os.path.isdir('static/file/' + file_path+"/"+file):#判断是否为文件夹
                   file_type.append([file,"文件夹"])
                else:
                   file_type.append([file,file.split(".")[-1]])#拿到文件的扩展名
        return render_template('index.html', file_type=file_type,dir=file_path+"/",sort_typt=sort_typt)

    elif os.path.exists('static/file/' + file_path) and file_path.split('.')[-1].upper()in photo_format:#判断路径是否为图片，返回图片展示模板
        files = get_file_list(os.path.split('static/file/' + file_path)[0],sort_typt)  # 得到当前文件所在的目录
        photolist = []
        for file in files:
            if file.split('.')[-1].upper() in photo_format:  # 找到当前目录的所有图片文件，展示在一个页面上
                photolist.append(file)
        path = os.path.split(file_path)[0] + "/"
        print(path)
        return render_template('photo.html' ,path=path,photolist=photolist)

    elif os.path.exists('static/file/' + file_path) and file_path.split('.')[-1].upper()in video_format:#判断路径是否为视频，返回视频播放模板
        files = get_file_list(os.path.split('static/file/' + file_path)[0],sort_typt) #得到当前文件所在的目录
        videolist = []
        for file in files:
            if file.split('.')[-1].upper() in video_format:  # 找到当前目录的所有视频文件，作为播放页面的播放列表
                videolist.append(file)
        path=os.path.split(file_path)[0]
        if path!="":
            path=path+"/"
        print(path)
        print("file_path："+file_path)
        return render_template('player.html', user_agent=user_agent, file_path=file_path,videolist=videolist,path=path,sort_typt=sort_typt)

    elif os.path.exists('static/file/' + file_path):#不支持的文件类型返回下载界面
        return render_template("download.html",link=file_path)

    else:#返回错误页面
        return render_template('404.html', error_message="打开路径出错：/"+file_path,error="不能打开此路径，可能是文件已被删除" ), 404

@app.errorhandler(404)
def miss(e):
    return render_template('404.html',error="非法的路径"), 404

if __name__ == '__main__':
    #app.run(port=8000)
    app.run( host='0.0.0.0',port=8000 )#host='0.0.0.0'，允许任任意IP访问

