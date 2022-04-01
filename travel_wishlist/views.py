from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.

def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST) # creating a form from data in the request
        place = form.save() # creating a model object from form
        if form.is_valid(): # validation against DB constraints
            place.save() # saves place to database
            return redirect('place_list') # reloads front page

    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

def about(request):
    author = 'Wyatt'
    about = 'A website to create a list of places to visit' # creates basic information about the author and website
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

def places_visited(request):
    visited = Place.objects.filter(visited=True) # filters information to only include places that were visited
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

def place_was_visited(request, place_pk): # this method saves place that are marked as visited
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    return redirect('place_list')
