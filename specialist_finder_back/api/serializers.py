from rest_framework import serializers

from .models import Category, Specialist, Comment, MyUser


class MyUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = MyUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class SpecialistSerializer(serializers.ModelSerializer):
    followers = MyUserSerializer(many=True, read_only=True)

    class Meta:
        model = Specialist
        fields = ['id', 'title', 'age', 'gender', 'city', 'likes', 'front_image', 'images', 'category', 'author', 'followers']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'title', 'text', 'specialist', 'author']