from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Osoba, Stanowisko
from .serializers import BookSerializer, OsobaSerializer, StanowiskoSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.http import Http404

# określamy dostępne metody żądania dla tego endpointu
@api_view(['GET', "POST"])  # dekorator zawsze przed funkcją
def book_list(request):
    """
    Lista wszystkich obiektów modelu Book.
    """
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):  # pk od primary key

    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Book
    :return: Response (with status and/or object/s data)
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Zwraca pojedynczy obiekt typu Book.
    """
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data, status = status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookListView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


@api_view(["GET","POST","DELETE"])
def osoba_detail(request, pk):
    try:
        osoba = Osoba.objects.get(pk=pk)
    except Osoba.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = OsobaSerializer(osoba)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        osoba.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET"])
def osoba_list(request):
    if request.method == "GET":
        return Response(OsobaSerializer(Osoba.objects.all(),
                                        many = True).data,
                        status = status.HTTP_200_OK)
        
@api_view(["GET"])
def osoba_name_filter_url(request, name):
    if request.method == "GET":
        return Response(OsobaSerializer(Osoba.objects.filter(nazwisko__icontains = name),
                                        many = True).data,
                        status = status.HTTP_200_OK)
        
@api_view(["GET"])
def osoba_name_filter_params(request):
    if request.method == "GET":
        # Pobranie parametru 'name' z query params
        name = request.query_params.get('name', None)
        if name is not None:
            return Response(OsobaSerializer(Osoba.objects.filter(nazwisko__icontains = name),
                                            many = True).data,
                            status = status.HTTP_200_OK)
        else:
            return Response({"error": "Parametr 'name' jest wymagany."}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(["GET","POST","DELETE"])
def stanowisko_detail(request, pk):
    try:
        stanowisko = Stanowisko.objects.get(pk=pk)
    except Stanowisko.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = StanowiskoSerializer(stanowisko)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = StanowiskoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        stanowisko.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET"])
def stanowisko_list(request):
    if request.method == "GET":
        return Response(StanowiskoSerializer(Stanowisko.objects.all(),
                                        many = True).data,
                        status = status.HTTP_200_OK)


# kod umieszczamy w pliku views.py wybranej aplikacji

from django.http import HttpResponse
import datetime


def welcome_view(request):
    now = datetime.datetime.now()
    html = f"""
        <html><body>
        Witaj użytkowniku! </br>
        Aktualna data i czas na serwerze: {now}.
        </body></html>"""
    return HttpResponse(html)


def osoba_list_html(request):
    # pobieramy wszystkie obiekty Osoba z bazy poprzez QuerySet
    osoby = Osoba.objects.all()
    return render(request,
                  "biblioteka/osoba/list.html",
                  {'osoby': osoby})

def osoba_detail_html(request, id):
    # pobieramy konkretny obiekt Osoba
    try:
        osoba = Osoba.objects.get(id=id)
    except Osoba.DoesNotExist:
        raise Http404("Obiekt Osoba o podanym id nie istnieje")

    return render(request,
                  "biblioteka/osoba/detail.html",
                  {'osoba': osoba})


def osoba_create_html(request):
    stanowiska = Stanowisko.objects.all()  # pobieramy listę stanowisk z bazy

    if request.method == "GET":
        return render(request, "biblioteka/osoba/create.html", {'stanowiska': stanowiska})
    elif request.method == "POST":
        imie = request.POST.get('imie')
        nazwisko = request.POST.get('nazwisko')
        plec = request.POST.get('plec')
        stanowisko_id = request.POST.get('stanowisko')

        if imie and nazwisko and plec and stanowisko_id:
            # pobieramy obiekt stanowiska
            try:
                stanowisko_obj = Stanowisko.objects.get(id=stanowisko_id)
            except Stanowisko.DoesNotExist:
                error = "Wybrane stanowisko nie istnieje."
                return render(request, "biblioteka/osoba/create.html", {'error': error, 'stanowiska': stanowiska})

            # tworzymy nową osobę
            Osoba.objects.create(
                imie=imie,
                nazwisko=nazwisko,
                plec=plec,
                stanowisko=stanowisko_obj
            )
            return redirect('osoba-list')
        else:
            error = "Wszystkie pola są wymagane."
            return render(request, "biblioteka/osoba/create.html", {'error': error, 'stanowiska': stanowiska})