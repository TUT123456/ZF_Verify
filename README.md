# ZF_Verify
正方教务系统验证码识别api  
只能识别正方教务系统的验证码！！  
  
1. 调用接口识别  
使用requests调用接口:  

  url = "http://127.0.0.1:6000/b"  
  files = {'image_file': (image_file_name, open('captcha.jpg', 'rb'), 'application')}  
  r = requests.post(url=url, files=files)  
  返回的结果是一个json：  

  {  
      'time': '1542017705.9152594',  
      'value': 'jsp1',  
  }  

2. 部署  
  部署的时候，把webserver_recognize_api.py文件的最后一行修改为如下内容：  
  
  app.run(host='0.0.0.0',port=5000,debug=False)  
  然后开启端口访问权限，就可以通过外网访问了。  
