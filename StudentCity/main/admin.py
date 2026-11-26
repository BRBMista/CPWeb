from django.contrib import admin
from .models import Student, Dormitory, Rooms, Facility


class DormitoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'num_dorm', 'total_room')
    list_display_links = ('id', 'num_dorm')
    search_fields = ('id', 'num_dorm')


class RoomsAdmin(admin.ModelAdmin):
    list_display = ('id', 'num_room', 'dorm')
    list_display_links = ('id', 'num_room')
    search_fields = ('id', 'num_room')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'room', 'owner')
    list_display_links = ('id', 'last_name')
    search_fields = ('last_name', 'first_name')
    prepopulated_fields = {'slug': ('last_name',)}


admin.site.register(Student, StudentAdmin)
admin.site.register(Dormitory, DormitoryAdmin)
admin.site.register(Rooms, RoomsAdmin)
admin.site.register(Facility)
