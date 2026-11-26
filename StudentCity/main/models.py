from django.db import models
from datetime import date

class Dormitory(models.Model):
    num_dorm = models.CharField(verbose_name='Номер общежития', max_length=10)
    total_room = models.CharField(verbose_name='Количество комнат', max_length=10)

    def __str__(self):
        return f"Общежитие №{self.num_dorm}"

class Facility(models.Model):
    name = models.CharField(verbose_name='Название удобства', max_length=50, unique=True)

    def __str__(self):
        return self.name

class Rooms(models.Model):
    dorm = models.ForeignKey(to='Dormitory', on_delete=models.PROTECT, verbose_name='Номер общежития', null=True)
    num_room = models.CharField(verbose_name='Номер комнаты', max_length=10)
    # Связь многие ко многим
    facilities = models.ManyToManyField(to='Facility', verbose_name='Удобства', blank=True)

    def __str__(self):
        return f"Комната {self.num_room} (Общ. №{self.dorm.num_dorm})"

    def residents_count(self):
        return self.student_set.count()

class Student(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    middle_name = models.CharField(verbose_name='Отчество', max_length=50, null=True, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    birth_date = models.DateField(verbose_name='Дата рождения', default=date(year=2000, month=1, day=1))
    course = models.CharField(verbose_name='Курс', max_length=1)
    group = models.CharField(verbose_name='Группа', max_length=10)
    is_study = models.BooleanField(verbose_name='Обучается', default=True)
    room = models.ForeignKey(to='Rooms', on_delete=models.PROTECT, verbose_name='Номер комнаты', null=True, blank=True)
    city = models.CharField(verbose_name='Город', max_length=50)
    nation = models.BooleanField(verbose_name='Гражданин РФ', default=True)
    visa_num = models.CharField(verbose_name='Номер визы', max_length=20, blank=True, null=True)
    visa_ending = models.DateField(verbose_name='Дата окончания визы', default=date(year=2000, month=1, day=1), blank=True, null=True)
    photo = models.ImageField(verbose_name='Фото', upload_to='photos/%Y/%m/%d', null=True, blank=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True, db_index=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"