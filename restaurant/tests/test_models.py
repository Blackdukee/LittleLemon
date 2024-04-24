from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from rest_framework.test import APIClient
import pytz
from ..models import Booking, Menu

class BookingTest(TestCase):
    def test_make_reservation_in_past(self):
        booking = Booking(name='John', no_of_guests=3, booking_date=timezone.now() - timezone.timedelta(days=1))
        self.assertTrue(booking.is_reservation_in_past())
    
    def test_make_reservation_in_future(self):
        booking = Booking(name='John', no_of_guests=3, booking_date=timezone.now() + timezone.timedelta(days=1))
        self.assertFalse(booking.is_reservation_in_past())
        
    def test_no_of_guests_greater_than_6(self):
        booking = Booking(name='John', no_of_guests=7, booking_date=timezone.now() + timezone.timedelta(days=1))
        with self.assertRaises(ValueError):
            booking.save()
            
    def test_no_of_guests_less_than_1(self):
        booking = Booking(name='John', no_of_guests=0, booking_date=timezone.now() + timezone.timedelta(days=1))
        with self.assertRaises(ValueError):
            booking.save()
    
    def test_no_of_guests_between_1_and_6(self):
        booking = Booking(name='John', no_of_guests=3, booking_date=timezone.now() + timezone.timedelta(days=1))
        booking.save()
        self.assertEqual(booking.no_of_guests, 3)


class BookingViewSetTest(TestCase):
    def test_get_all_bookings_without_token(self):
        client = APIClient()
        response = client.get(reverse('tables-list'))
        self.assertEqual(response.status_code, 401)
        
    def test_get_all_bookings_with_token(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='Rot@2112002Ma')
        token,_ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(reverse('tables-list'))
        self.assertEqual(response.status_code, 200)
        
    def test_create_booking_without_token(self):
        client = APIClient()
        response = client.post(reverse('tables-list'), {'name': 'John', 'no_of_guests': 3, 'booking_date': timezone.now() + timezone.timedelta(days=1)})
        self.assertEqual(response.status_code, 401)
    
    def test_create_booking_with_token(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='Rot@2112002Ma')
        token,_ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(reverse('tables-list'), {'name': 'John', 'no_of_guests': 3, 'booking_date': timezone.now() + timezone.timedelta(days=1)})
        self.assertEqual(response.status_code, 201)
        
class MenuTest(TestCase):
    def test_inventory_greater_than_5(self):
        menu = Menu(title='Pizza', price=12.99, inventory=6)
        with self.assertRaises(ValueError):
            menu.save()
            
    def test_inventory_less_than_1(self):
        menu = Menu(title='Pizza', price=12.99, inventory=0)
        with self.assertRaises(ValueError):
            menu.save()
            
        
class MenuViewTest(TestCase):
    def test_get_all_menu_items_without_token(self):
        client = APIClient()
        response = client.get(reverse('menu'))
        self.assertEqual(response.status_code, 401)
        
    def test_get_all_menu_items_with_token(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='Rot@2112002Ma')
        token,_ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        
    def test_create_menu_item_without_token(self):
        client = APIClient()
        response = client.post(reverse('menu'), {'title': 'Pizza', 'price': 12.99, 'inventory': 3})
        self.assertEqual(response.status_code, 401)
        
    def test_create_menu_item_with_token(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='Rot@2112002Ma')
        token,_ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(reverse('menu'), {'title': 'Pizza', 'price': 12.99, 'inventory': 3})
        self.assertEqual(response.status_code, 201)
        
    def test_get_single_menu_item_without_token(self):
        client = APIClient()
        menu = Menu.objects.create(title='Pizza', price=12.99, inventory=3)
        response = client.get(reverse('single_menu', args=[menu.id]))
        self.assertEqual(response.status_code, 401)
        
    def test_get_single_menu_item_with_token(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='Rot@2112002Ma')
        token,_ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        menu = Menu.objects.create(title='Pizza', price=12.99, inventory=3)
        response = client.get(reverse('single_menu', args=[menu.id]))
        self.assertEqual(response.status_code, 200)
        
    def test_update_single_menu_item_without_token(self):
        client = APIClient()
        menu = Menu.objects.create(title='Pizza', price=12.99, inventory=3)
        response = client.put(reverse('single_menu', args=[menu.id]), {'title': 'Pizza', 'price': 12.99, 'inventory': 4})
        self.assertEqual(response.status_code, 401)