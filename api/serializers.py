from rest_framework import serializers
from .models import Item


def check_divide_by_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError("10で割り切れる値にしてください")

class ItemModelSerializer(serializers.ModelSerializer):
    discounted_price = serializers.IntegerField(min_value=0, 
                                                validators=[check_divide_by_ten,]
                                                )
    class Meta:
        model = Item
        # fields = '__all__'
        fields = ['pk', 'name', 'price', 'discounted_price']
        # read_only_fields = ['pk', 'price']
        '''extra_kwargs = {
            'name': {'write_only': True, 'required': False},
        }'''
    
    def validate_price(self, value):
        if self.partial and value is None:
            return value
        # 1桁目が0以外を弾く
        if value % 10 != 0:
            raise serializers.ValidationError("priceの1桁目は0である必要があります")
        return value
    
    def validate_name(self, value):
        # nameがitemで始まることを強制する
        if value[0].islower():
            raise serializers.ValidationError("最初の文字は大文字である必要があります")
        return value
    
    def validate(self, data):
        price = data.get('price', self.instance.price if self.instance is not None else None)
        discounted_price = data.get('discounted_price', self.instance.discounted_price if self.instance is not None else None)
        if price < discounted_price:
            raise serializers.ValidationError("割引価格は元の価格よりも低くすること")
        return data