from rest_framework import serializers, validators
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title
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


class ValueFromViewKeyWordArgumentsDefault:
    requires_context = True

    def __init__(self, context_key):
        self.key = context_key

    def __call__(self, serializer_field):
        return serializer_field.context.get('view').kwargs.get(self.key)

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ReviewSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(
        default=ValueFromViewKeyWordArgumentsDefault('title'),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
            )
        ]

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        author_id = self.context['request'].user.id
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                    author=author_id, title_id=title_id).exists():
                raise serializers.ValidationError('Отзыв уже существует')
        return data
