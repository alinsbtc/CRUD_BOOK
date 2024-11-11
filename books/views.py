from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q


# Create a new book
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book
from .serializers import BookSerializer

def create_book(request):
    if request.method == 'POST':
        # Get data from the POST request
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        isbn = request.POST.get('isbn')
        price = request.POST.get('price')

        # Create a dictionary to pass to the serializer
        book_data = {
            'title': title,
            'author': author,
            'published_date': published_date,
            'isbn': isbn,
            'price': price
        }

        # Create a serializer instance with the data
        serializer = BookSerializer(data=book_data)

        # Check if the data is valid
        if serializer.is_valid():
            # Save the book data to the database
            serializer.save()
            messages.success(request, "Book added successfully!")
            return redirect('/')  # Redirect to the book list page after successful creation
        else:
            # If validation fails, display error messages
            for error in serializer.errors.values():
                messages.error(request, error)
    
    return render(request, 'create_book.html')  # Render the form for creating a book



def list_books(request):
    query = request.GET.get('q')  # Get the search term from the request
    if query:
        books = Book.objects.filter(
            Q(id__icontains=query) | Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()  # If no query, show all books

    return render(request, 'list_books.html', {'books': books})
def update_book(request, book_id): 
    book = get_object_or_404(Book, id=book_id)  
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.published_date = request.POST.get('published_date')
        book.isbn = request.POST.get('isbn')
        book.price = request.POST.get('price')

        book.save()
        messages.success(request, "Book updated successfully!")
        return redirect('/')  

    return render(request, 'update_book.html', {'book': book}) 

def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete() 
        
        return redirect('/')  

    return render(request, 'confirm_delete.html', {'book': book})
def detail_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'detail_book.html', {'book': book})