from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ItemModelSerializer
from rest_framework import status
from .models import Item


class ItemModelView(APIView):

    serializer_class = ItemModelSerializer

    def get(self, request): # 一覧(http://127.0.0.1:8000/api/item/)
        items = Item.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)

        # バリデーション
        if serializer.is_valid(raise_exception=True):
            serializer.save() # 保存(create) or 更新(update)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)


class ItemModelDetailView(APIView):
    
    serializer_class = ItemModelSerializer

    def get(self, request, pk):
        item = Item.objects.get(pk=pk)
        serializer = self.serializer_class(item)
        return Response(serializer.data)
    
    def put(self, request, pk):
        item = Item.objects.get(pk=pk)
        serializer = self.serializer_class(item, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
        
    def delete(self, request, pk):
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        item = Item.objects.get(pk=pk)
        serializer = self.serializer_class(item, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)