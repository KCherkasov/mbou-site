import re

from django import forms
from django.contrib.auth import authenticate

from mbou.models import News, LessonTiming, Document, DocumentCategory


class AddNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mbou-input-wide',
                                            'placeholder': u'Тема новости', }),
            'content': forms.Textarea(attrs={'class': 'form-control mbou-input-wide',
                                             'placeholder': u'Текст новости', }),
        }
        labels = {
            'title': u'Тема',
            'content': u'Текст',
        }


class LessonTimingForm(forms.ModelForm):
    class Meta:
        model = LessonTiming
        fields = ['number', 'start', 'end']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Номер урока', }),
            'start': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Время начала', }),
            'end': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Время конца', }),
        }
        labels = {
            'number': u'Урок',
            'start': u'Начало',
            'end': u'Конец',
        }

    def save(self):
        data = self.cleaned_data
        les, upd = LessonTiming.objects.update_or_create(number=data.get('number'),
                                                         defaults={'start': data.get('start'),
                                                                   'end': data.get('end'), })
        les.save()
        return les


class DocumentForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder': u'Название документа', }),
      label=u'Название документа', max_length=150)
    description = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder': u'Краткое описание документа (необязательно)', }),
      label=u'Описание документа', required=False)
    doc = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', }), label=u'Файл')
    categories = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder': u'Категории документа (каждая категория начинается с #)', }),
      label=u'Категории')

    def save(self):
        data = self.cleaned_data
        document = Document()
        document.title = data.get('title')
        document.title_id = document.make_title_id()
        document.description = data.get('description')
        document.save()
        if data.get('doc') is not None:
            doc_file = data.get('doc')
            doc_namext = re.split('[.]+', doc_file.name)
            document.doc.save('%s_%s.%s' % (doc_namext[0], str(document.id), doc_namext[1]), doc_file, save=True)
        document.save()
        categories_raw = data.get('categories')
        categories_raw.lower()
        categories = re.split('[#]+', categories_raw)
        for cat_name in categories:
            if cat_name is not None and cat_name != '':
                category = DocumentCategory.objects.get_or_create(name=cat_name)
                document.categories.add(category)
        return document


class SignInForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder': u'Введите логин', }),
      max_length=30,
      label=u'Логин')
    password = forms.CharField(widget=forms.PasswordInput(
      attrs={'class': 'form-control', 'placeholder': u'Введите пароль', }),
      label=u'Пароль')

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('login'), password=data.get('password'))
        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError('Учетная запись не активна')
        else:
            raise forms.ValidationError('Неверный логин и/или пароль')


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder': u'Имя Отчество', }),
      max_length=30, label=u'Имя')
    last_name = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder': 'Фамилия', }),
      max_length=30,
      label=u'Фамилия')
    email = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder': u'Введите e-mail', }),
      max_length=30, label=u'Электронная почта')
    password1 = forms.CharField(widget=forms.PasswordInput(
      attrs={'class': 'form-control', 'placeholder': u'Введите пароль', }),
      min_length=6, label=u'Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(
      attrs={'class': 'form-control', 'placeholder': u'Подтвердите пароль', }),
      min_length=6,
      label=u'Пароль еще раз')

    def clean_password2(self):
        password = self.cleaned_data.get('password1', '')
        confirm = self.cleaned_data.get('password2', '')
        if password != confirm:
            forms.ValidationError('Введенные пароли не совпадают')

    def save(self, user):
        data = self.cleaned_data
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data.get('email')
        password = self.cleaned_data.get('password1', '')
        if password != '':
            user.set_password(password)
        user.save()
        return self
