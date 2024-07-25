import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Exchange, Comment


class ExchangeSerializer(serializers.ModelSerializer):  # создаем сериализатор для данных точно  связанных с таблицей
    # нужно для того чтобы юзер присваивал автоматически и на странице ввода данных не было выбора пользователя
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Exchange  # модель, которую берем за основу

        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'name', 'parent', 'replies', 'bank', 'user']

    def get_replies(self, obj):
        # Фильтруем ответы для текущего комментария
        replies = Comment.objects.filter(parent=obj)
        # Сериализуем ответы с использованием того же класса `CommentSerializer`
        return CommentSerializer(replies, many=True, read_only=True).data

# Добавляем replies после основного определения сериализатора
#
# class ExchangeModel:
#     def __init__(self, currency_exchange, data):
#         self.currency_exchange = currency_exchange
#         self.data = data


# # функция кодирования данных модели в json формат
#
# def encode():
#     exchange = ExchangeModel(55.90,"2024-09-30")
#     exchange_sr = ExchangeSerializer(exchange)
#     print(exchange_sr.data, type(exchange_sr.data), sep='\n')
#     json = JSONRenderer().render(exchange_sr.data)
#     print(json)
#
# # функция декодирования данных модели в json формат
#
# def decode():
#     stream = io.BytesIO(b'{"currency_exchange":"55.90","data":"2024-09-30"}')
#     data = JSONParser().parse(stream)
#     serializer = ExchangeSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
#
# class ExchangeSerializer(serializers.Serializer):
#     # создаем сериализатор (простой без базовой привязки к модели. может быть вообще не привязан к модели)
#     currency_exchange = serializers.DecimalField(max_digits=10, decimal_places=2)
#     date = serializers.DateField()
#     bank_id = serializers.IntegerField()   # в сериализаторе прописывать нужно конкретным образом к чему привязка поля
#     currency_id = serializers.IntegerField()
#
#     def create(self, validated_data):  # переопределение функции создания таблицы
#         return Exchange.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         # переопределение функции обновления данных таблицы
#         instance.currency_exchange = validated_data.get('currency_exchange', instance.currency_exchange)
#         instance.date = validated_data.get('date', instance.date)
#         instance.bank_id = validated_data.get('bank_id', instance.bank_id)
#         instance.currency_id = validated_data.get('currency_id', instance.currency_id)
#         instance.save()
#         return instance
