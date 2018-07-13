import re

from django import forms
from django.contrib.auth import authenticate

from mbou.models import News, LessonTiming, Document, DocumentCategory,\
    StaffMember, Subject, StafferCategory, Photo, Album, UrlUser


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
    doc = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', }), label=u'Файл')
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


class StaffMemberForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': u'Введите имя', }),
        max_length=60, label=u'Имя')
    middle_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': u'Введите отчество', }),
        max_length=60, label=u'Отчество')
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': u'Введите фамилию', }),
        max_length=60, label=u'Фамилия')
    is_chairman = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control', }),
                                     label=u'Является администрацией', initial=False, required=False, )
    chair_position = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': u'нет'}),
        label=u'Должность в администрации', empty_value=u'нет')
    is_combiner = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control', }),
                                     label=u'Является совместителем', initial=False, required=False, )
    subject = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': u'Введите предмет'}), label=u'Преподаваемый предмет')
    category = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': u'Введите категорию'}), label=u'Категория')
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': u'email', }),
        label=u'Электронная почта (необязательно)', empty_value=u'', required=False)
    experience = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', }),
                                    label=u'Преподавательский стаж', min_value=0, max_value=100)

    def save(self):
        data = self.cleaned_data
        StaffMember().add_or_update(data.get('first_name'), data.get('middle_name'), data.get('last_name'),
                                    data.get('is_chairman'), data.get('chair_position'),
                                    data.get('is_combiner'), data.get('subject'), data.get('category'),
                                    data.get('email'), data.get('experience'))
        return self


class AlbumAddForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder': u'Название альбома', }),
      label=u'Название альбома', max_length=60)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3, 'placeholder': u'Краткое описание альбома (необязательно)', }),
        label=u'Описание альбома', required=False, empty_value=u'')

    def save(self):
        data = self.cleaned_data
        album = Album()
        album.title = data.get('title')
        album.title_id = album.make_title_id()
        album.description = data.get('description')
        album.save()
        return self


class PhotoAddForm(forms.Form):
    label = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder': u'Название фотографии', }),
      label=u'Название фотографии', max_length=60, required=False, empty_value=u'')
    description = forms.CharField(widget=forms.Textarea(
      attrs={'class': 'form-control', 'rows': 3, 'placeholder': u'Краткое описание фотографии (необязательно)', }),
      label=u'Описание фотографии', required=False, empty_value=u'')
    photo = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), label=u'Фотография')
    album = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                   queryset=Album.objects.all(), label=u'Альбом')

    def __init__(self, *args, **kwargs):
        album_id = kwargs.pop('album_id', None)
        super(PhotoAddForm, self).__init__(*args, **kwargs)
        if album_id:
            self.fields['album'].queryset = Album.objects.filter(pk=album_id)

    def clean(self):
        if not self.cleaned_data['label']:
            raise forms.ValidationError(u'Введите название фотографии')
        if not self.cleaned_data['photo']:
            raise forms.ValidationError(u'Загрузите фотографию!')

    def save(self):
        data = self.cleaned_data
        photo = Photo()
        photo.label = data.get('label')
        photo.description = data.get('description')
        album = data.get('album')
        photo.album = album
        photo.save()
        if data.get('photo') is not None:
            photo_file = data.get('photo')
            photo_namext = re.split('[.]+', photo_file.name)
            photo.photo.save('%s_%s.%s' % (photo_namext[0], str(photo.id), photo_namext[1]), photo_file, save=True)
        photo.save()
        album.photo_set.add(photo)
        return photo


class UrlUserCreationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': u'Логин', }),
        max_length=30, label=u'Логин')
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
        min_length=6, label=u'Пароль еще раз')

    def clean_password2(self):
        password = self.cleaned_data.get('password1', '')
        confirm = self.cleaned_data.get('password2', '')
        if password != confirm:
            forms.ValidationError('Введенные пароли не совпадают')

    def save(self):
        data = self.cleaned_data
        user = UrlUser()
        user.username = data.get('username')
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data.get('email')
        password = self.cleaned_data.get('password1', '')
        if password != '':
            user.set_password(password)
        user.is_active = True
        user.is_superuser = False
        user.is_staff = True
        user.save()
        return self
