from rest_framework import serializers
from .models import Dormitory, Rooms, Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'birth_date',
                  'course', 'group', 'is_study', 'room', 'city', 'nation',
                  'visa_num', 'visa_ending', 'photo', 'slug', 'owner')
        read_only_fields = ('slug', 'owner')

    def validate_first_name(self, value):
        if not value.replace('-', '').isalpha():
            raise serializers.ValidationError('Недопустимые символы в имени')
        return value

    def validate(self, attrs):
        nation = attrs.get('nation', getattr(self.instance, 'nation', True))
        visa_num = attrs.get('visa_num', getattr(self.instance, 'visa_num', None))
        if not nation and not visa_num:
            raise serializers.ValidationError({'visa_num': 'Для иностранного студента укажите номер визы'})
        return attrs


class StudentDetailSerializer(serializers.ModelSerializer):
    living = serializers.SerializerMethodField()
    owner = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'birth_date',
                  'course', 'group', 'is_study', 'city', 'nation',
                  'visa_num', 'visa_ending', 'photo', 'slug', 'owner', 'living')

    def get_living(self, obj):
        room = obj.room
        if room is None:
            return 'Не размещён'
        if room.dorm is None:
            return f'Комната {room.num_room}'
        return f'Общежитие №{room.dorm.num_dorm}, комната {room.num_room}'


class DormitorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dormitory
        fields = ('id', 'num_dorm', 'total_room')


class RoomSerializer(serializers.ModelSerializer):
    facilities = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    residents = serializers.IntegerField(source='residents_count', read_only=True)

    class Meta:
        model = Rooms
        fields = ('id', 'dorm', 'num_room', 'residents', 'facilities')
