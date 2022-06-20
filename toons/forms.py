from django import forms

from toons.models import Toon, Comment


class UploadToonForm(forms.ModelForm):
    class Meta:
        model = Toon # 어떤 모델 기반인가
        fields = ('episode', 'hook', 'thumbnail') # 어떤 필드를 사용할 것인가, content 하나만 사용하겠다.

    episode = forms.IntegerField()
    hook = forms.CharField(max_length=150)
    thumbnail = forms.ImageField()
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class UpdateToonForm(forms.ModelForm):
    class Meta:
        model = Toon # 어떤 모델 기반인가
        fields = ('hook', 'thumbnail') # 어떤 필드를 사용할 것인가, content 하나만 사용하겠다.

    hook = forms.CharField(max_length=150)
    thumbnail = forms.ImageField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment # 어떤 모델 기반인가
        fields = ('content', ) # 어떤 필드를 사용할 것인가, content 하나만 사용하겠다.