from turtle import ht
from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.

@login_required
def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST) # creating a form from data in the request
        place = form.save(commit=False) # creating a model object from form
        place.user = request.user
        if form.is_valid(): # validation against DB constraints
            place.save() # saves place to database
            return redirect('place_list') # reloads front page

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

@login_required
def about(request):
    author = 'Wyatt'
    about = 'A website to create a list of places to visit' # creates basic information about the author and website
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True) # filters information to only include places that were visited
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

# this method saves places that are marked as visited
@login_required
def place_was_visited(request, place_pk): 
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden() # return forbidden message if user is not logged in
    return redirect('place_list') # reload place_list

@login_required
def place_details(request, place_pk):
    # displays 404 error page if a place cannot be found
    place = get_object_or_404(Place, pk=place_pk)

    # shows a forbidden message if the user is not logged in
    if place.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid(): # checks if all required fields by the databse are filled in, and are they the correct data types
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors) # temporary, refine later

        return redirect('place_details', place_pk=place_pk)

    else:
        # if GET request, show Place info and optional form
        # if place is visited, show form' if not, no form
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place':place, 'review_form':review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})

# allows a user to delete a place after they have properly logged in
@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')

    else:
        return HttpResponseForbidden()
