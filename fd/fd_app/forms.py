from django import forms
from .models import UploadImage
#なぜforms.Formでははくforms.ModelFormなのか
#Form は、requestの情報からインスタンスを作成しなおす
#ModelFormは、requestの情報をそのままモデルに反映できる
#ModelFormに入力されたデータは.is_valid()で検査できる
#モデルへの保存は.save()


class Upload(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['img']#model.pyでimgが変数なのでimageとしてはいけない
        #fields = ['result_img']
        
        
class SettingForm(forms.Form):
    angle = forms.IntegerField()
    gray = forms.BooleanField(required=False)
    
#input用フォーム
class input_img(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['img']
        
#output用フォーム
class output_img(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['result_img']