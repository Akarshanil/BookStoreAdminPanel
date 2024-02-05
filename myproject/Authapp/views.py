from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.urls import reverse
from rest_framework.filters import SearchFilter
from .models import Author,Book
from django.db.models import Q
from django.contrib import messages
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .serializers import AuthorSerializer,BookSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


# Create your views here.
def login_ren(request):
    return render(request,"login.html")
def auther_view(request):
    data = Author.objects.all().order_by('-updated_at')
    data_book=Book.objects.all()
    total_book=data_book.count()
    total_author=data.count()
    paginator=Paginator(data,5)
    page=request.GET.get('page')
    try:
        posts =paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(request,'auther_listing.html',{'auth':posts,'total_author':total_author,'total_book':total_book})

def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            request.session['username'] = username
            return redirect('author_view')
        else:
            return redirect('login_ren')

    return redirect('login_ren')
def logout_view(request):
    logout(request)
    return redirect(reverse('login_ren'))

def save_author_data(request):
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')

        new_author = Author(
            author_name=author_name,
            user_name=user_name,
            email=email
        )
        new_author.save()
        messages.success(request, "The Author data saved")

        return redirect(auther_view)

def search_results(request):
    search_word = request.GET.get('search_word')
    data = Author.objects.all()
    data_book = Book.objects.all()
    total_book = data_book.count()
    total_author = data.count()

    if search_word:
        request.session['search_word'] = search_word
    else:
        search_word = request.session.get('search_word')

    results = Author.objects.filter(
            Q(author_name__icontains=search_word) |
            Q(user_name__icontains=search_word) |
            Q(email__icontains=search_word)
        ).order_by('-updated_at')


    paginator = Paginator(results, 4)
    page = request.GET.get('page')

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, 'search_result.html', {
        'results': results,'total_author':total_author,'total_book':total_book
    })


def edit_author(request):
     if request.method == 'POST':
        author_id=request.POST.get('unq_id')
        author = Author.objects.get(id=author_id)
        author.author_name = request.POST.get('authorname')
        author.user_name = request.POST.get('username')
        author.email = request.POST.get('emailedit')
        author.save()
        messages.success(request, "The Author data is Edited")
        return redirect(auther_view)

def book_view(request):

    book_data = Book.objects.all().order_by('-updated_at')
    data = Author.objects.all().order_by('-updated_at')
    total_author=data.count()
    total_book=book_data.count()
    paginator=Paginator(book_data,4)
    page=request.GET.get('page') #request.Get is a dictionary
    try:
        book_data = paginator.page(page)
    except PageNotAnInteger:
        book_data = paginator.page(1)
    except EmptyPage:
        book_data = paginator.page(paginator.num_pages)
    return render(request,"book_listing.html",{'book_data':book_data,'total_author':total_author,'total_book':total_book})

def save_book_data(request):
        if request.method == 'POST':
            book_name = request.POST.get('book_name')
            author_name = request.POST.get('author_name')
            author_instance, _ = Author.objects.get_or_create(author_name=author_name)

            new_book = Book(
                book_name=book_name,
                author_name=author_instance,
            )
            new_book.save()
            return redirect('book_view')
def book_search_results(request):
    search_word = request.GET.get('search_word')
    if search_word:
        request.session['search_word'] = search_word
    else:
        search_word = request.session.get('search_word')
    book_results = Book.objects.filter(
        Q(book_name__icontains=search_word) |
        Q(author_name__author_name__icontains=search_word)
    )

    paginator = Paginator(book_results, 4)
    page = request.GET.get('page')

    try:
        book_results = paginator.page(page)
    except PageNotAnInteger:
        book_results = paginator.page(1)
    except EmptyPage:
        book_results = paginator.page(paginator.num_pages)
    data = Author.objects.all()
    data_book = Book.objects.all()
    total_book = data_book.count()
    total_author = data.count()
    return render(request, 'book_search_result.html', {'book_results': book_results,'total_book':total_book,'total_author':total_author})

def edit_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_unq_id')
        book = Book.objects.get(id=book_id)
        book.book_name = request.POST.get('bookname')
        author_name = request.POST.get('authorname')
        author_obj=Author.objects.get(author_name=author_name)
        book.author_name=author_obj
        book.save()
        messages.success(request, "The book data is Edited")

        return redirect('book_view')

def author_detailed_view(request,id):
    author_detail=Author.objects.get(id=id)
    book_detail_related_author=Book.objects.filter(author_name=author_detail).order_by('-created_date')
    paginator=Paginator(book_detail_related_author,2)
    page=request.GET.get('page') #request.Get is a dictionary
    try:
        data=paginator.page(page)
    except PageNotAnInteger:
        data=paginator.page(1)
    except EmptyPage:
        data=paginator.page(paginator.num_pages)
    return  render(request,"author_detailed_view.html",{'author_detail':author_detail,'book_author':data})
def edit_author_book(request):
    if request.method == 'POST':
        new_book=request.POST.get('bookname')
        new_author=request.POST.get('authorname')
        org_author=request.POST.get('book_auth')
        if new_author== org_author:
            author_obj = Author.objects.filter(author_name=new_author).first()
            num_id=author_obj.id
            new_book = Book(
                book_name=new_book,
                author_name=author_obj,
            )
            new_book.save()
            return redirect(author_detailed_view,num_id)
        else:
            messages.warning(request, "The author should be same")
            return redirect(request.META.get('HTTP_REFERER'))
def edit_author_old_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('unq_id')
        book = Book.objects.get(id=book_id)
        book.book_name=request.POST.get('editbookname')
        old_author =request.POST.get('author_name')
        author_obj = Author.objects.filter(author_name=old_author).first()
        num_id=author_obj.id
        book.author_name=author_obj
        book.save()
        return redirect(author_detailed_view, num_id)


def author_bk_search(request):
    author_detail_id=request.GET.get('book_auth')
    author_detail=Author.objects.get(id=author_detail_id)
    search_word = request.GET.get('search_word')
    if search_word:
        request.session['search_word'] = search_word
        request.session['author_id']=author_detail_id
    else:
        search_word = request.session.get('search_word')
        author_detail_id=request.session.get('author_id')

    book_results = Book.objects.filter(author_name=author_detail_id, book_name__icontains=search_word)
    paginator = Paginator(book_results, 4)
    page = request.GET.get('page')

    try:
        book_results = paginator.page(page)
    except PageNotAnInteger:
        book_results = paginator.page(1)
    except EmptyPage:
        book_results = paginator.page(paginator.num_pages)

    return render(request, 'author_book_search.html', {'book_results': book_results,'author_detail':author_detail,'author_detail_id':author_detail_id})


def toggle_status_change(request):
    if request.method == 'POST' and request.is_ajax():
        author_id = request.POST.get('author_id')
        status = request.POST.get('status')

        try:
            if status.lower() == "true":
                boolean_value = True
            elif status.lower() == "false":
                boolean_value = False
            else:
                raise ValueError("Status must be either 'true' or 'false'")

            author = Author.objects.get(id=author_id)
            author.status = boolean_value
            author.save()
            return JsonResponse({'success': True})
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'Author not found'})
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
def toggle_status_change_book(request):
    if request.method == 'POST' and request.is_ajax():
        author_id = request.POST.get('author_id')
        status = request.POST.get('status')

        try:
            if status.lower() == "true":
                boolean_value = True
            elif status.lower() == "false":
                boolean_value = False
            else:
                raise ValueError("Status must be either 'true' or 'false'")

            book = Book.objects.get(id=author_id)
            book.status = boolean_value
            book.save()
            return JsonResponse({'success': True})
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'Author not found'})
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
# django rest framwork
class SetPagination(PageNumberPagination):
    page_size = 2

class authsetApi(ListAPIView):
    queryset=Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class =SetPagination
    filter_backends = (SearchFilter,)
    search_fields=('author_name', 'user_name', 'email')

class BookApi(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = SetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('book_name', 'author_name__author_name')


class AuthorDetailsAPI(APIView):
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorUpdationApi(APIView):
    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def put(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        author = self.get_object(pk)
        author.delete()
        return Response("data deleted",status=status.HTTP_204_NO_CONTENT)
class BookDetailsAPI(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class BookUpdationApi(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def put(self, request, id):
        book = self.get_object(id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response("data deleted",status=status.HTTP_204_NO_CONTENT)
