from rest_framework import serializers

from core.constants import CHARS_FOR_CODE, CHARS_FOR_USERNAME
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .utils import rating_avg


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        return rating_avg(self, obj)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class CommentSerializers(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'review')


class ReviewSerializers(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        author_id = self.context['request'].user.id
        if self.context['request'].method == 'POST':
            if len(Review.objects.filter(
                    author_id=author_id, title_id=title_id)) != 0:
                raise serializers.ValidationError('Отзыв уже существует')
        return data


class CodeEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        if data['username'] == "me":
            raise serializers.ValidationError('Нельзя использовать данное имя')
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=CHARS_FOR_USERNAME)
    confirmation_code = serializers.CharField(max_length=CHARS_FOR_CODE)
