from django.db import models
from PIL import Image
import io
import cv2
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os

#画像をアップロードするモデル
class UploadImage(models.Model):
    img = models.ImageField(upload_to='img/')
    result_img = models.ImageField(upload_to='result/')
    # Create your models here.
    def transform(self,angle,gray):
        #アップロードされたファイルから画像オブジェクトを生成
        org_img = Image.open(self.img)
        #PILでの画像処理
        ret_img = org_img.rotate(angle)
        if gray:
            ret_img = ret_img.convert('L')
        #画像処理後の画像データをbufferに保存
        #この content にはPIL 画像オブジェクトを直接指定することはできない
        #なのでいったんio.BytesIOに対してPIL画像を保存し、contentにio.BytesIOを指定
    
        buffer = io.BytesIO()
        ret_img.save(fp=buffer,format=org_img.format)
        #画像ファイルの削除
        self.result_img.delete()
        #レコード(DB)の削除
        self.delete()
        #id = self.result_img.earliest("created_on")
        #id.result_img.delete()
        self.result_img.save(name=self.img.name,content=buffer)
    
    def find_difference(self,url):
        print(self.img)
        imgA = Image.open(self.img)
        imgA = np.array(imgA,dtype=np.float32)
        print(url)
        imgB = Image.open('.' + url)
        imgB = np.array(imgB,dtype=np.float32)
        imgA = cv2.cvtColor(imgA, cv2.COLOR_BGR2RGB)
        imgB = cv2.cvtColor(imgB, cv2.COLOR_BGR2RGB)
        # 画像サイズを取得
        hA, wA, cA = imgA.shape[:3]
        hB, wB, cA = imgB.shape [:3]
        # 特徴量検出器を作成
        akaze = cv2.AKAZE_create()
        # 二つの画像の特徴点を抽出
        kpA, desA = akaze.detectAndCompute(imgA,None)
        kpB, desB = akaze.detectAndCompute(imgB,None)
        # imageBを透視変換する
        # 透視変換: 斜めから撮影した画像を真上から見た画像に変換する感じ
        # BFMatcher型のオブジェクトを作成する
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # 記述子をマッチさせる。※スキャン画像(B2)の特徴抽出はforループ前に実施済み。
        matches = bf.match(desA,desB)
        # マッチしたものを距離順に並べ替える。
        matches = sorted(matches, key = lambda x:x.distance)
        # マッチしたもの（ソート済み）の中から上位★%（参考：15%)をgoodとする。
        good = matches[:int(len(matches) * 0.15)]
        # 対応が取れた特徴点の座標を取り出す？
        src_pts = np.float32([kpA[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dst_pts = np.float32([kpB[m.trainIdx].pt for m in good]).reshape(-1,1,2)
        # findHomography:二つの画像から得られた点の集合を与えると、その物体の投射変換を計算する
        M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC,5.0) # dst_img作成の際だけ使う。warpperspectiveの使い方がわかってない。
        # imgBを透視変換。
        imgB_transform = cv2.warpPerspective(imgB, M, (wA, hA))
        # imgAとdst_imgの差分を求めてresultとする。グレースケールに変換。
        result = cv2.absdiff(imgA, imgB_transform)
        result_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # 二値化
        _, result_bin = cv2.threshold(result_gray, 50, 255, cv2.THRESH_BINARY) # 閾値は50
        # カーネルを準備（オープニング用）
        kernel = np.ones((2,2),np.uint8)
        # オープニング（収縮→膨張）実行 ノイズ除去
        result_bin = cv2.morphologyEx(result_bin, cv2.MORPH_OPEN, kernel) # オープニング（収縮→膨張）。ノイズ除去。
        # 二値画像をRGB形式に変換し、2枚の画像を重ねる。
        result_bin_rgb = cv2.cvtColor(result_bin, cv2.COLOR_GRAY2RGB)
        result_add = cv2.addWeighted(imgA, 0.3, result_bin_rgb, 0.7, 2.2) # ２.２はガンマ値。大きくすると白っぽくなる
        #PIL変換
        print(type(result_add))
        result_add = result_add.astype(np.uint8)
        result_add = Image.fromarray(result_add)
        image_io = io.BytesIO()
        result_add.save(image_io,format="JPEG")
    
            #画像ファイルの削除
        self.result_img.delete()
        #レコード(DB)の削除
        self.delete()
        #id = self.result_img.earliest("created_on")
        #id.result_img.delete()
        self.result_img.save(name=self.img.name,content=image_io)
    
        
        