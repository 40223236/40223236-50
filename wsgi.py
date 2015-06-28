#@+leo-ver=5-thin
#@+node:2014fall.20141212095015.1775: * @file wsgi.py
# coding=utf-8
# 上面的程式內容編碼必須在程式的第一或者第二行才會有作用

################# (1) 模組導入區
# 導入 cherrypy 模組, 為了在 OpenShift 平台上使用 cherrypy 模組, 必須透過 setup.py 安裝


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:2014fall.20141212095015.1776: ** <<declarations>> (wsgi)
import cherrypy
# 導入 Python 內建的 os 模組, 因為 os 模組為 Python 內建, 所以無需透過 setup.py 安裝
import os
# 導入 random 模組
import random
# 導入 gear 模組
import gear

################# (2) 廣域變數設定區
# 確定程式檔案所在目錄, 在 Windows 下有最後的反斜線
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
# 設定在雲端與近端的資料儲存目錄
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示程式在雲端執行
    download_root_dir = os.environ['OPENSHIFT_DATA_DIR']
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
else:
    # 表示程式在近端執行
    download_root_dir = _curdir + "/local_data/"
    data_dir = _curdir + "/local_data/"

'''以下為近端 input() 與 for 迴圈應用的程式碼, 若要將程式送到 OpenShift 執行, 除了採用 CherryPy 網際框架外, 還要轉為 html 列印
# 利用 input() 取得的資料型別為字串
toprint = input("要印甚麼內容?")
# 若要將 input() 取得的字串轉為整數使用, 必須利用 int() 轉換
repeat_no = int(input("重複列印幾次?"))
for i in range(repeat_no):
    print(toprint)
'''
#@-<<declarations>>
#@+others
#@+node:2014fall.20141212095015.1777: ** class Hello
################# (3) 程式類別定義區
# 以下改用 CherryPy 網際框架程式架構
# 以下為 Hello 類別的設計內容, 其中的 object 使用, 表示 Hello 類別繼承 object 的所有特性, 包括方法與屬性設計
class Hello(object):

    # Hello 類別的啟動設定
    _cp_config = {
    'tools.encode.encoding': 'utf-8',
    'tools.sessions.on' : True,
    'tools.sessions.storage_type' : 'file',
    #'tools.sessions.locking' : 'explicit',
    # session 以檔案儲存, 而且位於 data_dir 下的 tmp 目錄
    'tools.sessions.storage_path' : data_dir+'/tmp',
    # session 有效時間設為 60 分鐘
    'tools.sessions.timeout' : 60
    }

    #@+others
    #@+node:2014fall.20141212095015.2004: *3* __init__
    def __init__(self):
        # 配合透過案例啟始建立所需的目錄
        if not os.path.isdir(data_dir+'/tmp'):
            os.mkdir(data_dir+'/tmp')
        if not os.path.isdir(data_dir+"/downloads"):
            os.mkdir(data_dir+"/downloads")
        if not os.path.isdir(data_dir+"/images"):
            os.mkdir(data_dir+"/images")
    #@+node:2015.20150330144929.1713: *3* aaa
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def aaa(self, n_g1=15, n_g2=24,M=5, P=15):

         n_g1 = int(str(n_g1))
         n_g2 = int(str(n_g2))


     
         if n_g1 < 15:
            return "齒輪1 低於15" + self.threeDgear()
         elif n_g1 > 80:
            return "齒輪1 超過80 " + self.threeDgear()
         elif n_g2 < 15:
            return "齒輪2 低於15 " + self.threeDgear()
         elif n_g2 > 80:
            return "齒輪2 超過80 " + self.threeDgear()
         else:

            cherrypy.session['g1'] =  n_g1
            cherrypy.session['g2'] =  n_g2
            outstring = '''
                <!DOCTYPE html> 
                <html>
                <head>
                齒輪1='''+str(n_g1)+'''<br />
                齒輪2='''+str(n_g2)+'''<br />
                <br /><a href="mygeartest2">繪製齒輪</a><br />
                <head>
                </html>
            '''
            return outstring







    #@+node:2014fall.20141212095015.1778: *3* index_orig
    # 以 @ 開頭的 cherrypy.expose 為 decorator, 用來表示隨後的成員方法, 可以直接讓使用者以 URL 連結執行
    @cherrypy.expose
    # index 方法為 CherryPy 各類別成員方法中的內建(default)方法, 當使用者執行時未指定方法, 系統將會優先執行 index 方法
    # 有 self 的方法為類別中的成員方法, Python 程式透過此一 self 在各成員方法間傳遞物件內容
    def index_orig(self, toprint="40223250"):
        return toprint
    #@+node:2014fall.20141212095015.1779: *3* hello
    @cherrypy.expose
    def hello(self, toprint="Hello World!"):
        return toprint
    #@+node:2014fall.20141215194146.1791: *3* index
    @cherrypy.expose
    def index(self):
        outstring = '''
        <!DOCTYPE html> 
        <html>
        <head>
         
        </head>
        <body>
        <a href="threeDgear">1人2齒輪組合</a><br />
-----------------------------------------------------------
         <br /><a href="threeDgear1">2人2齒輪組合</a><br />
         <br /><a href="threeDgear2">2人2齒輪組合another Ver.</a><br />
        </body>





        </html>
        '''
        
        return outstring
    #@+node:2015.20150615085301.1: *3* index1
    @cherrypy.expose
    def index1(self, n_g1=15, n_g2=24,n_g3=15,n_g4=24,M=5, P=15):
         n_g1 = int(str(n_g1))
         n_g2 = int(str(n_g2))
         n_g3 = int(str(n_g3))
         n_g4 = int(str(n_g4))

     
         if n_g1 < 15:
            return "齒輪1 低於15" + self.threeDgear1()
         elif n_g1 > 80:
            return "齒輪1 超過80 " + self.threeDgear1()
         elif n_g2 < 15:
            return "齒輪2 低於15 " + self.threeDgear1()
         elif n_g2 > 80:
            return "齒輪2 超過80 " + self.threeDgear1()
         elif n_g3 < 15:
            return "齒輪3 超過80 " + self.threeDgear1()
         elif n_g3 > 80:
            return "齒輪3 超過80 " + self.threeDgear1()
         elif n_g4 < 15:
            return "齒輪3 超過80 " + self.threeDgear1()
         elif n_g4 > 80:
            return "齒輪3 超過80 " + self.threeDgear1()


         else:

            cherrypy.session['g1'] =  n_g1
            cherrypy.session['g2'] =  n_g2
            cherrypy.session['g3'] =  n_g3
            cherrypy.session['g4'] =  n_g4

            outstring = '''
            <!DOCTYPE html> 
            <html>
            <head>
            齒輪1-1='''+str(n_g1)+'''<br />
            齒輪1-2='''+str(n_g2)+'''<br />
            齒輪2-1='''+str(n_g3)+'''<br />
            齒輪2-2='''+str(n_g4)+'''<br />
            <br /><a href="mygeartest3">繪製齒輪</a><br />
            <head>
            </html>
             '''
            return outstring
    #@+node:2015.20150330144929.1762: *3* index2
    @cherrypy.expose
    def index2(self, n_g1=15, n_g2=24,M=5, P=15):
         n_g1 = int(str(n_g1))
         n_g2 = int(str(n_g2))

     
         if n_g1 < 15:
            return "齒輪1 低於15" + self.threeDgear2()
         elif n_g1 > 80:
            return "齒輪1 超過80 " + self.threeDgear2()
         elif n_g2 < 15:
            return "齒輪2 低於15 " + self.threeDgear2()
         elif n_g2 > 80:
            return "齒輪2 超過80 " + self.threeDgear2()
       

         else:

            cherrypy.session['g1'] =  n_g1
            cherrypy.session['g2'] =  n_g2
     
            outstring = '''
            <!DOCTYPE html> 
            <html>
            <head>
            齒輪1-1='''+str(n_g1)+'''<br />
            齒輪1-2='''+str(n_g2)+'''<br />
      
            <br /><a href="mygeartest4">繪製齒輪</a><br />
            <head>
            </html>
             '''
            return outstring
    #@+node:2015.20150331094055.1737: *3* index3
    @cherrypy.expose
    def index3(self, n_g3=15, n_g4=24,M=5, P=15):

         n_g3 = int(str(n_g3))
         n_g4 = int(str(n_g4))

     

         if n_g3 < 15:
            return "齒輪3 超過80 " + self.threeDgear3()
         elif n_g3 > 80:
            return "齒輪3 超過80 " + self.threeDgear3()
         elif n_g4 < 15:
            return "齒輪3 超過80 " + self.threeDgear3()
         elif n_g4 > 80:
            return "齒輪3 超過80 " + self.threeDgear3()


         else:


            cherrypy.session['g3'] =  n_g3
            cherrypy.session['g4'] =  n_g4

            outstring = '''
            <!DOCTYPE html> 
            <html>
            <head>

            齒輪2-1='''+str(n_g3)+'''<br />
            齒輪2-2='''+str(n_g4)+'''<br />
            <br /><a href="mygeartest5">繪製齒輪</a><br />
            <head>
            </html>
             '''
            return outstring
    #@+node:2015.20150331094055.1733: *3* threeDgear
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def threeDgear(self, n_g1=15, n_g2=24,M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">

    </head>


    <body>
        
    <form method=POST action=aaa>

    齒數1(範圍:15~80):<input type=text name=n_g1 value='''+str(n_g1)+'''><br />
    齒數2(範圍:15~80):<input type=text name=n_g2 value = '''+str(n_g2)+'''><br />
    <input type=submit value=輸入齒數>
    </form>
    <br /><a href="index">返回首頁</a><br />
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script>
    window.onload=function(){
    brython();
    }
    </script>
    </body>
    </html>
     '''
     
        return outstring
    #@+node:2015.20150622011853.1: *3* threeDgear1
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def threeDgear1(self, n_g1=15, n_g2=24,n_g3=15,n_g4=24,M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    </head>
    <body>
        
    <form method=POST action=index1>
    齒數1(範圍:15~80):<input type=text name=n_g1 value='''+str(n_g1)+'''><br />
    齒數2(範圍:15~80):<input type=text name=n_g2 value = '''+str(n_g2)+'''><br />
    齒數3(範圍:15~80):<input type=text name=n_g3 value='''+str(n_g3)+'''><br />
    齒數4(範圍:15~80):<input type=text name=n_g4 value = '''+str(n_g4)+'''><br />

    <input type=submit value=輸入齒數>
    </form>
    <br /><a href="index">返回首頁</a><br />
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script>
    window.onload=function(){
    brython();
    }
    </script>
    </body>
    </html>
    '''

        return outstring
    #@+node:2015.20150622102244.1: *3* threeDgear2
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def threeDgear2(self,  n_g1=15,  n_g2=24,M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">
        
    <form method=\"post\" action=\"index2">
    <fieldset>

    齒數1(範圍:15~80):<br /><input type=\"text\" name=\"n_g1\"><br />
    齒數2(範圍:15~80):<br /><input type=\"text\" name=\"n_g2\"><br />


    <input type=\"submit\" value=\"輸入齒數">
    </form>
    </body>
    </html>
    '''
      
        return outstring
    #@+node:2015.20150331094055.1735: *3* threeDgear3
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def threeDgear3(self,  n_g3=15,  n_g4=24,M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">
        
    <form method=\"post\" action=\"index3">
    <fieldset>

    齒數3(範圍:15~80):<br /><input type=\"text\" name=\"n_g3\"><br />
    齒數4(範圍:15~80):<br /><input type=\"text\" name=\"n_g4\"><br />


    <input type=\"submit\" value=\"輸入齒數">
    </form>
    </body>
    </html>
    '''
      
        return outstring
    #@+node:amd.20150415215023.1: *3* mygeartest2
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def mygeartest2(self, n_g1=15, n_g2=24,M=5, P=15):
        g1= int(cherrypy.session.get('g1'))
        g2= int(cherrypy.session.get('g2'))
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <form method=\"post\" action=\"index">
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>


    <input type=\"submit\" value=\"return\">
    </form>


    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">


    <fieldset>

     <legend>齒輪組合:</legend>

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *
    # 請注意, 這裡導入位於 Lib/site-packages 目錄下的 spur.py 檔案
    import spur

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")


    # 以下利用 spur.py 程式進行繪圖, 接下來的協同設計運算必須要配合使用者的需求進行設計運算與繪圖
    # 其中並將工作分配給其他組員建立類似 spur.py 的相關零件繪圖模組
    # midx, midy 為齒輪圓心座標, rp 為節圓半徑, n 為齒數, pa 為壓力角, color 為線的顏色
    # Gear(midx, midy, rp, n=20, pa=20, color="black"):
    # 模數決定齒的尺寸大小, 囓合齒輪組必須有相同的模數與壓力角
    # 壓力角 pa 單位為角度

    pa = 20
    # m 為模數
    m = 20
    # 第1齒輪齒數
    n_g1 ='''+str( g1)+'''
    # 第2齒輪齒數
    n_g2 ='''+str( g2)+'''

    # 計算兩齒輪的節圓半徑
    rp_g1 = m*n_g1/2
    rp_g2 = m*n_g2/2


    # 將第1齒輪順時鐘轉 90 度
    # 使用 ctx.save() 與 ctx.restore() 以確保各齒輪以相對座標進行旋轉繪圖
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820)
    # rotate to engage
    ctx.rotate(pi)
    # put it back
    ctx.translate(-820,-820)
    spur.Spur(ctx).Gear(820,820,rp_g1,n_g1, pa, "blue")
    ctx.restore()

    # 將第2齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820+rp_g1+rp_g2)
    # rotate to engage
    ctx.rotate(-pi/n_g2)
    # put it back
    ctx.translate(-820,-(820+rp_g1+rp_g2))
    spur.Spur(ctx).Gear(820,820+rp_g1+rp_g2,rp_g2,n_g2, pa, "black")
    ctx.restore()


    </script>
    <canvas id="plotarea" width="3800" height="4000"></canvas>

    </body>
    </html>
    '''

        return outstring
    #@+node:2015.20150622011937.1: *3* mygeartest3
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def mygeartest3(self, n_g1=15, n_g2=24, n_g3=15, n_g4=24,M=5, P=15):
        g1= int(cherrypy.session.get('g1'))
        g2= int(cherrypy.session.get('g2'))
        g3= int(cherrypy.session.get('g3'))
        g4= int(cherrypy.session.get('g4'))
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <form method=\"post\" action=\"index">
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>

    <input type=\"submit\" value=\"return\">
    </form>

    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">


    <fieldset>

     <legend>齒輪組合:</legend>

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *
    # 請注意, 這裡導入位於 Lib/site-packages 目錄下的 spur.py 檔案
    import spur

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")


    # 以下利用 spur.py 程式進行繪圖, 接下來的協同設計運算必須要配合使用者的需求進行設計運算與繪圖
    # 其中並將工作分配給其他組員建立類似 spur.py 的相關零件繪圖模組
    # midx, midy 為齒輪圓心座標, rp 為節圓半徑, n 為齒數, pa 為壓力角, color 為線的顏色
    # Gear(midx, midy, rp, n=20, pa=20, color="black"):
    # 模數決定齒的尺寸大小, 囓合齒輪組必須有相同的模數與壓力角
    # 壓力角 pa 單位為角度

    pa = 20
    # m 為模數
    m = 20

    # 第1齒輪齒數
    n_g1 = '''+str(g1)+'''
    # 第2齒輪齒數
    n_g2 = '''+str(g2)+'''
    # 第3齒輪齒數
    n_g3 = '''+str(g3)+'''
    # 第4齒輪齒數
    n_g4 = '''+str(g4)+'''


    # 計算兩齒輪的節圓半徑
    rp_g1 = m*n_g1/2
    rp_g2 = m*n_g2/2
    rp_g3 = m*n_g3/2
    rp_g4 = m*n_g4/2


    ##############################################################################################

    # 將第1齒輪順時鐘轉 90 度
    # 使用 ctx.save() 與 ctx.restore() 以確保各齒輪以相對座標進行旋轉繪圖
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820)
    # rotate to engage
    ctx.rotate(pi)
    # put it back
    ctx.translate(-820,-820)
    spur.Spur(ctx).Gear(820,820,rp_g1,n_g1, pa, "blue")
    ctx.restore()

    ###############################################################################################

    # 將第2齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820+rp_g1+rp_g2)
    # rotate to engage
    ctx.rotate(-pi/n_g2)
    # put it back
    ctx.translate(-820,-(820+rp_g1+rp_g2))
    spur.Spur(ctx).Gear(820,820+rp_g1+rp_g2,rp_g2,n_g2, pa, "black")
    ctx.restore()

    ##############################################################################################

    # 將第3齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820+rp_g2+rp_g3,820+rp_g1+rp_g2)
    # rotate to engage
    ctx.rotate((pi/n_g3*0.5)*(n_g2%4)-pi/n_g3*(n_g3/2))
    # put it back
    ctx.translate(-(820+rp_g2),-(820+rp_g1+rp_g2))
    spur.Spur(ctx).Gear(820+rp_g2,820+rp_g1+rp_g2,rp_g3,n_g3, pa, "red")
    ctx.restore()

    ##############################################################################################

    # 將第4齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820+rp_g2+rp_g3,820+rp_g1+rp_g2+rp_g3+rp_g4)
    # rotate to engage
    ctx.rotate(-(pi/n_g4*0.5)*(n_g2%4)-(pi/n_g4*0.5)*(n_g3%4)+(pi/n_g4))
    # put it back
    ctx.translate(-(820+rp_g2),-(820+rp_g1+rp_g2+rp_g3+rp_g4))
    spur.Spur(ctx).Gear(820+rp_g2,820+rp_g1+rp_g2+rp_g3+rp_g4,rp_g4,n_g4, pa, "black")
    ctx.restore()

    ##############################################################################################


    </script>
    <canvas id="plotarea" width="3800" height="12000"></canvas>


    </body>
    </html>
    '''

        return outstring
    #@+node:2015.20150622102228.1: *3* mygeartest4
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def mygeartest4(self, n_g1=15, n_g2=24,M=5, P=15):
        g1= int(cherrypy.session.get('g1'))
        g2= int(cherrypy.session.get('g2'))
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <form method=\"post\" action=\"threeDgear3\">
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>


    <input type=\"submit\" value=\"Next">
    </form>


    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">


    <fieldset>

     <legend>齒輪組合:</legend>

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *
    # 請注意, 這裡導入位於 Lib/site-packages 目錄下的 spur.py 檔案
    import spur

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")


    # 以下利用 spur.py 程式進行繪圖, 接下來的協同設計運算必須要配合使用者的需求進行設計運算與繪圖
    # 其中並將工作分配給其他組員建立類似 spur.py 的相關零件繪圖模組
    # midx, midy 為齒輪圓心座標, rp 為節圓半徑, n 為齒數, pa 為壓力角, color 為線的顏色
    # Gear(midx, midy, rp, n=20, pa=20, color="black"):
    # 模數決定齒的尺寸大小, 囓合齒輪組必須有相同的模數與壓力角
    # 壓力角 pa 單位為角度

    pa = 20
    # m 為模數
    m = 20
    # 第1齒輪齒數
    n_g1 ='''+str( g1)+'''
    # 第2齒輪齒數
    n_g2 ='''+str( g2)+'''

    # 計算兩齒輪的節圓半徑
    rp_g1 = m*n_g1/2
    rp_g2 = m*n_g2/2


    # 將第1齒輪順時鐘轉 90 度
    # 使用 ctx.save() 與 ctx.restore() 以確保各齒輪以相對座標進行旋轉繪圖
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820)
    # rotate to engage
    ctx.rotate(pi)
    # put it back
    ctx.translate(-820,-820)
    spur.Spur(ctx).Gear(820,820,rp_g1,n_g1, pa, "blue")
    ctx.restore()

    # 將第2齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820+rp_g1+rp_g2)
    # rotate to engage
    ctx.rotate(-pi/n_g2)
    # put it back
    ctx.translate(-820,-(820+rp_g1+rp_g2))
    spur.Spur(ctx).Gear(820,820+rp_g1+rp_g2,rp_g2,n_g2, pa, "black")
    ctx.restore()


    </script>
    <canvas id="plotarea" width="3800" height="4000"></canvas>

    </body>
    </html>
    '''

        return outstring
    #@+node:2015.20150330144929.1765: *3* mygeartest5
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def mygeartest5(self, n_g1=15, n_g2=24, n_g3=15, n_g4=24,M=5, P=15):
        g1= int(cherrypy.session.get('g1'))
        g2= int(cherrypy.session.get('g2'))
        g3= int(cherrypy.session.get('g3'))
        g4= int(cherrypy.session.get('g4'))
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <form method=\"post\" action=\"index">
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>

    <input type=\"submit\" value=\"return\">
    </form>

    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">


    <fieldset>

     <legend>齒輪組合:</legend>

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *
    # 請注意, 這裡導入位於 Lib/site-packages 目錄下的 spur.py 檔案
    import spur

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")


    # 以下利用 spur.py 程式進行繪圖, 接下來的協同設計運算必須要配合使用者的需求進行設計運算與繪圖
    # 其中並將工作分配給其他組員建立類似 spur.py 的相關零件繪圖模組
    # midx, midy 為齒輪圓心座標, rp 為節圓半徑, n 為齒數, pa 為壓力角, color 為線的顏色
    # Gear(midx, midy, rp, n=20, pa=20, color="black"):
    # 模數決定齒的尺寸大小, 囓合齒輪組必須有相同的模數與壓力角
    # 壓力角 pa 單位為角度

    pa = 20
    # m 為模數
    m = 20

    # 第1齒輪齒數
    n_g1 = '''+str(g1)+'''
    # 第2齒輪齒數
    n_g2 = '''+str(g2)+'''
    # 第3齒輪齒數
    n_g3 = '''+str(g3)+'''
    # 第4齒輪齒數
    n_g4 = '''+str(g4)+'''


    # 計算兩齒輪的節圓半徑
    rp_g1 = m*n_g1/2
    rp_g2 = m*n_g2/2
    rp_g3 = m*n_g3/2
    rp_g4 = m*n_g4/2


    ##############################################################################################

    # 將第1齒輪順時鐘轉 90 度
    # 使用 ctx.save() 與 ctx.restore() 以確保各齒輪以相對座標進行旋轉繪圖
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820)
    # rotate to engage
    ctx.rotate(pi)
    # put it back
    ctx.translate(-820,-820)
    spur.Spur(ctx).Gear(820,820,rp_g1,n_g1, pa, "blue")
    ctx.restore()

    ###############################################################################################

    # 將第2齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820+rp_g1+rp_g2)
    # rotate to engage
    ctx.rotate(-pi/n_g2)
    # put it back
    ctx.translate(-820,-(820+rp_g1+rp_g2))
    spur.Spur(ctx).Gear(820,820+rp_g1+rp_g2,rp_g2,n_g2, pa, "black")
    ctx.restore()

    ##############################################################################################

    # 將第3齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820+rp_g2+rp_g3,820+rp_g1+rp_g2)
    # rotate to engage
    ctx.rotate((pi/n_g3*0.5)*(n_g2%4)-pi/n_g3*(n_g3/2))
    # put it back
    ctx.translate(-(820+rp_g2),-(820+rp_g1+rp_g2))
    spur.Spur(ctx).Gear(820+rp_g2,820+rp_g1+rp_g2,rp_g3,n_g3, pa, "red")
    ctx.restore()

    ##############################################################################################

    # 將第4齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820+rp_g2+rp_g3,820+rp_g1+rp_g2+rp_g3+rp_g4)
    # rotate to engage
    ctx.rotate(-(pi/n_g4*0.5)*(n_g2%4)-(pi/n_g4*0.5)*(n_g3%4)+(pi/n_g4))
    # put it back
    ctx.translate(-(820+rp_g2),-(820+rp_g1+rp_g2+rp_g3+rp_g4))
    spur.Spur(ctx).Gear(820+rp_g2,820+rp_g1+rp_g2+rp_g3+rp_g4,rp_g4,n_g4, pa, "black")
    ctx.restore()

    ##############################################################################################


    </script>
    <canvas id="plotarea" width="3800" height="12000"></canvas>


    </body>
    </html>
    '''

        return outstring
    #@+node:2014fall.20141215194146.1793: *3* doCheck
    @cherrypy.expose
    def doCheck(self, guess=None):
        # 假如使用者直接執行 doCheck, 則設法轉回根方法
        if guess is None:
            raise cherrypy.HTTPRedirect("/")
        # 從 session 取出 answer 對應資料, 且處理直接執行 doCheck 時無法取 session 值情況
        try:
            theanswer = int(cherrypy.session.get('answer'))
        except:
            raise cherrypy.HTTPRedirect("/")
        # 經由表單所取得的 guess 資料型別為 string
        try:
            theguess = int(guess)
        except:
            return "error " + self.guessform()
        # 每執行 doCheck 一次,次數增量一次
        cherrypy.session['count']  += 1
        # 答案與所猜數字進行比對
        if theanswer < theguess:
            return "big " + self.guessform()
        elif theanswer > theguess:
            return "small " + self.guessform()
        else:
            # 已經猜對, 從 session 取出累計猜測次數
            thecount = cherrypy.session.get('count')
            return "exact: <a href=''>再猜</a>"
    #@+node:2014fall.20141215194146.1789: *3* guessform
    def guessform(self):
        # 印出讓使用者輸入的超文件表單
        outstring = str(cherrypy.session.get('answer')) + "/" + str(cherrypy.session.get('count')) + '''<form method=POST action=doCheck>
    請輸入您所猜的整數:<input type=text name=guess><br />
    <input type=submit value=send>
    </form>'''
        return outstring
    #@-others
#@-others
################# (4) 程式啟動區
# 配合程式檔案所在目錄設定靜態目錄或靜態檔案
application_conf = {'/static':{
        'tools.staticdir.on': True,
        # 程式執行目錄下, 必須自行建立 static 目錄
        'tools.staticdir.dir': _curdir+"/static"},
        '/downloads':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/downloads"},
        '/images':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/images"}
    }
    
root = Hello()
root.gear = gear.Gear()

cherrypy.server.socket_port = 8081
cherrypy.server.socket_host = '127.0.0.1'
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示在 OpenSfhit 執行
    application = cherrypy.Application(root, config=application_conf)
else:
    # 表示在近端執行
    cherrypy.quickstart(root, config=application_conf)
#@-leo
