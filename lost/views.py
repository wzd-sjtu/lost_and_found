from django.shortcuts import render
from lost.models import KindL,PageL
from lost.forms import KindLForm,PageLForm
# Create your views here.
from django.http import HttpResponse

def index(request):
    kinds_list = KindL.objects.order_by('-likes')[:]
    context_dict = {'kinds': kinds_list}
    return render(request, 'lost/index.html',context_dict)


def kind(request,kind_name_slug):
    context_dict={}
    try:
        kind = KindL.objects.get(slug=kind_name_slug)
        context_dict['kind_name'] = kind.name
        pages = PageL.objects.filter(kind=kind)
        context_dict['pages'] = pages
        context_dict['kind'] = kind
    except KindL.DoesNotExist:

        pass

    return render(request, 'lost/kind.html', context_dict)




def add_kind(request):

    if request.method == 'POST':
        form = KindLForm(request.POST)#实例化表单数据，并且把表单实例对象传递给html页面
        if form.is_valid():  #  一旦is_valid成功，就会保存输入的数据

            form.save(commit=True)
            #  这里的save函数是在models里面存在的  把数据存储到数据库里面
            #  返回之前的界面  返回之前的界面
            return index(request)
        else:
            print(form.errors)
    else:

        form = KindLForm()

    return render(request, 'lost/add_kind.html', {'form': form})

def add_page(request,kind_name_slug=None):
    try:
        cat = KindL.objects.get(slug=kind_name_slug)
    except KindL.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageLForm(request.POST)#  实例化表单数据，并且把表单实例对象传递给html页面
        if form.is_valid():  #  一旦is_valid成功，就会保存输入的数据
            if cat:
                page = form.save(commit=False)
                page.kind = cat
                page.views = 0
                page.save()
                return kind(request,kind_name_slug)
            #  这里的save函数是在models里面存在的  把数据存储到数据库里面
        else:
            print(form.errors)
    else:

        form = PageLForm()
    context_dict = {'form': form, 'kind': cat}
    return render(request, 'lost/add_page.html', context_dict)

#   views是进行二者之间的连接而生成的  某种程度上是可以接受的