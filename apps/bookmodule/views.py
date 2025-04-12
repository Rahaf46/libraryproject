from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Max, Min
from django.db.models import Count
from .models import Address, Student
from .models import Book

def task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/task1.html', {'books': books})

def task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains='co') | Q(author__icontains='co'))
    )
    return render(request, 'bookmodule/task2.html', {'books': books})

def task3(request):
    books = Book.objects.filter(
        ~Q(edition__gt=3) & ~Q(title__icontains='co') & ~Q(author__icontains='co')
    )
    return render(request, 'bookmodule/task3.html', {'books': books})

def task4(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/task4.html', {'books': books})

def task5(request):
    stats = Book.objects.aggregate(
        total_books=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/task5.html', {'stats': stats})

def student_count_by_city(request):
    data = Student.objects.values('address__city').annotate(total=Count('id'))
    return render(request, 'bookmodule/student_count.html', {'data': data})

def add_students(request):
    # إنشاء المدن
    a1 = Address.objects.create(city='Riyadh')
    a2 = Address.objects.create(city='Jeddah')
    a3 = Address.objects.create(city='Dammam')

    # إضافة طلاب مرتبطين بهذه المدن
    Student.objects.create(name='Ahmed', age=20, address=a1)
    Student.objects.create(name='Sara', age=22, address=a1)
    Student.objects.create(name='Mona', age=21, address=a2)
    Student.objects.create(name='Ali', age=23, address=a3)
    Student.objects.create(name='Fahad', age=20, address=a3)

    return HttpResponse("Sample students and addresses added successfully!")


def add_books(request):
    Book.objects.create(title='Continuous Delivery', author='J.Humble and D. Farley', edition=1)
    Book.objects.create(title="Django and Python", author="John Doe", price=150, edition=3)
    Book.objects.create(title="AI and Machine Learning", author="Jane Smith", price=200, edition=2)
    Book.objects.create(title="Data Science Handbook", author="Alice Brown", price=80, edition=1)

    return HttpResponse("Data added successfully!")

def simple_query(request):
    mybooks=Book.objects.filter(title__icontains='and') # <- multiple objects
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def complex_query(request):
    mybooks=books=Book.objects.filter(author__isnull = False).filter(title__icontains='and').filter(edition__gte = 2).exclude(price__lte = 100)[:10]
    if len(mybooks)>=1:
        return render(request, 'bookmodule/bookList.html', {'books':mybooks})
    else:
        return render(request, 'bookmodule/index.html')



def index(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, 'bookmodule/list_books.html')

def viewbook1(request, bookId):
    return render(request, 'bookmodule/one_book.html')

def about_us(request):
    return render(request, 'bookmodule/aboutus.html')

def html5_links(request):
    return render(request, 'bookmodule/html5_links.html') 

def text_formatting(request):
    return render(request, 'bookmodule/formatting.html')

def listing_page(request):
    return render(request, 'bookmodule/listing.html')

def tables_page(request):
    return render(request, 'bookmodule/tables.html')


def search_books(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword', '').lower()
        is_title = request.POST.get('option1') 
        is_author = request.POST.get('option2') 
        
        books = __getBooksList()
        filtered_books = []

        for book in books:
            found = False
            if is_title and keyword in book['title'].lower():
                found = True
            if not found and is_author and keyword in book['author'].lower():
                found = True

            if found:
                filtered_books.append(book)

        return render(request, 'bookmodule/bookList.html', {'books': filtered_books})

    return render(request, "bookmodule/search.html")

def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

