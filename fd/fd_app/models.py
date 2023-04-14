from django.db import models
from PIL import Image
import io

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
        #self.delete()
        #id = self.result_img.earliest("created_on")
        #id.result_img.delete()
        self.result_img.save(name=self.img.name,content=buffer)
        
        