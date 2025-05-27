from django.shortcuts import render
from .models import Place, Photo
from django.db.models import Q

def index(request):
    return render(request, 'food/index.html')

def search(request):
    query = request.GET.get('q')
    print(f"Search query: {query}")  # 用來查看是否抓取搜尋關鍵字
    if query:
        place_list = Place.objects.filter(
            Q(name__icontains=query) |
            Q(time__icontains=query) |
            Q(address__icontains=query) |
            Q(food__icontains=query) 
        )
    else:
        place_list = Place.objects.all()
    context = {
        'query': query,
        'place_list': place_list,
    }
    return render(request, 'food/search.html', context)