from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Dormitory, Rooms, Student
from .utils import DataMixin, menu
from .forms import AddStudentForm, RegisterUserForm, LoginUserForm
from .filters import StudentFilter


def index(request):
    context = {
        'menu': menu,
        'title': 'Главная страница'
    }
    return render(request, 'main/index.html', context=context)


class Dorm(DataMixin, ListView):
    model = Dormitory
    template_name = 'main/dorm.html'
    context_object_name = 'dormitory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Общежитие')
        return {**context, **c_def}


class DormRooms(DataMixin, DetailView):
    model = Dormitory
    template_name = 'main/dorm_rooms.html'
    pk_url_kwarg = 'dorm_id'
    context_object_name = 'dorm'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dorm = self.object
        context['dorm_rooms'] = Rooms.objects.filter(dorm=dorm)
        c_def = self.get_user_context(title=f'Комнаты в общежитии {dorm.num_dorm}')
        return {**context, **c_def}


class StudentsInRoom(DataMixin, DetailView):
    model = Rooms
    template_name = 'main/students_in_room.html'
    pk_url_kwarg = 'room_id'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.object
        context['students'] = Student.objects.filter(room=room)
        c_def = self.get_user_context(title=f'Комната {room.num_room} - Общежитие №{room.dorm.num_dorm}')
        return {**context, **c_def}


class Students(DataMixin, ListView):
    paginate_by = 3
    model = Student
    template_name = 'main/students.html'
    context_object_name = 'students'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('last_name', 'first_name')
        self.st_filter = StudentFilter(self.request.GET, queryset)
        return self.st_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop('page', None)
        c_def = self.get_user_context(title='Список студентов',
                                      st_filter=self.st_filter,
                                      query=params.urlencode())
        return {**context, **c_def}


class ShowStudent(DataMixin, DetailView):
    model = Student
    template_name = 'main/show_student.html'
    slug_url_kwarg = 'stud_slug'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Страница студента', today=timezone.localdate())
        return {**context, **c_def}


class AddStudent(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddStudentForm
    template_name = 'main/addstudent.html'
    success_url = reverse_lazy('students')
    login_url = reverse_lazy('login')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['photo'].widget.attrs['accept'] = 'image/*'
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление студента')
        return {**context, **c_def}


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return {**context, **c_def}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
