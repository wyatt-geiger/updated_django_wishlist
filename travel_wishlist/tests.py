from django.test import TestCase
from django.urls import reverse

from .models import Place

class TestHomePage(TestCase):

    # this unit test checks to ensure that the homepage displays the proper message when the database is empty
    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list') # checks place_list
        response = self.client.get(home_page_url) # creates a response
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') # asserts that correct template is used
        self.assertContains(response, 'You have no places in your wishlist') # asserts that the response contains the correct message string

class TestWishList(TestCase):

    fixtures = ['test_places'] # loads preset data from test_places.json, which contains test data

    # this test ensures that the wishlist only contains place that have not been visited yet
    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list')) # checks place_list, creates response (identical to lines 10 and 11)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') # asserts that correct template is used
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')
        # these assert statements check to make sure that the response contains certain places and doesn't contain other places

class TestVisitedPage(TestCase):
    
    # this unit test checks to ensure that the visited page displays the proper message when the database is empty
    def test_visited_page_shows_empty_list_message_for_empty_database(self):
        response = self.client.get(reverse('places_visited')) # checks places_visited, creates response
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html') # asserts that correct template is used
        self.assertContains(response, 'You have not visited any places yet') # asserts that the response contains the correct message string

class VisitedList(TestCase):

    fixtures = ['test_places'] # loads preset data from test_places.json, which contains test data
    
    # this test checks to make sure that the visited list is showing visited places
    def test_visited_list_shows_visited_places(self):
        response = self.client.get(reverse('places_visited')) # checks places_visited, creates response
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html') # asserts that correct template is used
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')
        # these assert statements check to make sure that the response contains certain places and doesn't contain other places

class TestAddNewPlace(TestCase):

    # this test ensures that adding a new unvisited place works properly
    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list') # checks place_list
        new_place_data = {'name': 'Tokyo', 'visited': False} # add a new place, set visited to False

        response = self.client.post(add_place_url, new_place_data, follow=True) 
        # submit the data using POST method. follow ensures that redirect works properly (this is required)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') # asserts correct template is used

        # check data used to create template
        response_places = response.context['places'] # context is a dictionary, this is whatever views.py is combining with the template (line 19 in views.py)
        self.assertEquals(1, len(response_places)) # checks to make sure only 1 place is added
        tokyo_from_template = response_places[0] # retrieve first element in response_places, Tokyo

        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False) # retrieve object Tokyo

        self.assertEquals(tokyo_from_database, tokyo_from_template) # ensures that template and database values match

class TestVisitPlace(TestCase):

    fixtures = ['test_places'] # loads preset data from test_places.json, which contains test data

    # checks to make sure database is updated correctly when visiting a place
    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2, )) # checks place_was_visited, using 2 as the key
        response = self.client.post(visit_place_url, follow=True) # creates response, ensures redirect works with follow=True

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        # asserts correct template is used

        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')
        # asserts that response contains Tokyo but not New York

        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)
        # checks the database, ensures that New York is marked as visited using pk=2 to find it

    # checks to make sure that a 404 error is displayed when trying to find a pk key that does not exist
    def test_non_existent_place(self):
        visit_nonexistent_place_url = reverse('place_was_visited', args=(12312321, ))
        response = self.client.post(visit_nonexistent_place_url, follow=True)
        self.assertEqual(404, response.status_code)
