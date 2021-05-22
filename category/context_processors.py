from .models import Category
# 중복되는 코드를 제거하기 위해서 context를 만들어주는 함수를 생성한다.

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
