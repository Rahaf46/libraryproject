from django.shortcuts import render ,get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Max, Min
from django.db.models import Count
from .models import Address, Student
from .models import Book
from .models import Department
from .models import Course
from django.urls import path
from . import views
from .forms import BookForm
from .forms import StudentForm, AddressForm
from .forms import Student2Form, Address2Form
from .models import Student2 
from .forms import BookCoverForm

def add_book_cover(request):
    if request.method == 'POST':
        form = BookCoverForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_book_covers')
    else:
        form = BookCoverForm()
    return render(request, 'bookmodule/add_book_cover.html', {'form': form})

def list_book_covers(request):
    from .models import BookCover
    covers = BookCover.objects.all()
    return render(request, 'bookmodule/list_book_covers.html', {'covers': covers})

def list_students2(request):
    students = Student2.objects.all()
    return render(request, 'bookmodule/list_students2.html', {'students': students})

def add_student2(request):
    if request.method == 'POST':
        form = Student2Form(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            form.save_m2m()  # هذا مهم لحفظ العلاقة many-to-many
            return redirect('list_students2')
    else:
        form = Student2Form()
    return render(request, 'bookmodule/add_student2.html', {'form': form})



def student_list(request):
    students = Student.objects.select_related('address').all()
    return render(request, 'bookmodule/student_list.html', {'students': students})

def student_add(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        student_form = StudentForm(request.POST)
        if address_form.is_valid() and student_form.is_valid():
            address = address_form.save()
            student = student_form.save(commit=False)
            student.address = address
            student.save()
            return redirect('student_list')
    else:
        address_form = AddressForm()
        student_form = StudentForm()
    return render(request, 'bookmodule/student_form.html', {'address_form': address_form, 'student_form': student_form})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    address = student.address
    if request.method == 'POST':
        student_form = StudentForm(request.POST, instance=student)
        address_form = AddressForm(request.POST, instance=address)
        if student_form.is_valid() and address_form.is_valid():
            address_form.save()
            student_form.save()
            return redirect('student_list')
    else:
        student_form = StudentForm(instance=student)
        address_form = AddressForm(instance=address)
    return render(request, 'bookmodule/student_form.html', {'student_form': student_form, 'address_form': address_form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.address.delete()  # Delete address first
    student.delete()
    return redirect('student_list')

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_address')
    else:
        form = AddressForm()
    return render(request, 'bookmodule/add_address.html', {'form': form})

def add_address2(request):
    if request.method == 'POST':
        form = Address2Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_address2')
    else:
        form = Address2Form()
    return render(request, 'bookmodule/add_address2.html', {'form': form})


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

def task1_lab9(request):
    data = Department.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/lab9_task1.html', {'data': data})

def task2_lab9(request):
    data = Course.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/lab9_task2.html', {'data': data})

def task3_lab9(request):
    departments = Department.objects.all()
    oldest_students = []

    for department in departments:
        oldest_student = Student.objects.filter(department=department).order_by('-id').first()  
        oldest_students.append({
            'department': department.name,
            'oldest_student': oldest_student.name if oldest_student else 'No students'
        })

    return render(request, 'bookmodule/lab9_task3.html', {'oldest_students': oldest_students})


def task4_lab9(request):
    departments = Department.objects.annotate(num_students=Count('student')).filter(num_students__gt=2).order_by('-num_students')
    return render(request, 'bookmodule/lab9_task4.html', {'departments': departments})


def add_books(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books_part2')
    else:
        form = BookForm()
    return render(request, 'bookmodule/add_book.html', {'form': form})

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
    books = Book.objects.all()
    return render(request, 'bookmodule/list_books.html', {'books': books})

def edit_book(request, id):
    book = get_object_or_404(Book, pk=id)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('list_books_part2')
    return render(request, 'bookmodule/edit_book.html', {'form': form, 'book': book})

def delete_book(request, id):
    book = get_object_or_404(Book, pk=id)
    book.delete()
    return redirect('list_books_part2')



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

