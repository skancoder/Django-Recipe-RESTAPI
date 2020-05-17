from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL=reverse('recipe:ingredient-list')

class PublicApiTests(TestCase):
    """Test the publicly available Ingredients API"""

    def setUp(self):
        self.client=APIClient()
    
    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res=self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsApiTests(TestCase):
    """Test the authorized user Ingredients API"""
    def setUp(self):
        self.user=get_user_model().objects.create_user(
            'testuser@gmail.com',
            'user1234'
        )
        self.client=APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of Ingredients"""
        Ingredient.objects.create(user=self.user,name='chilli')
        Ingredient.objects.create(user=self.user,name='salt')

        res=self.client.get(INGREDIENTS_URL)

        ingredients=Ingredient.objects.all().order_by('-name')# - means descending
        serializer=IngredientSerializer(ingredients,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)
    
    def test_Ingredients_limited_to_user(self):
        """Test that only Ingredients for the authenticated user are returned"""
        user2=get_user_model().objects.create_user(
            'testuser1@gmail.com',
            'user1234'
        )
        Ingredient.objects.create(user=user2,name='turmaric')
        ingredient=Ingredient.objects.create(user=self.user,name='cumin')

        res=self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],ingredient.name)
    
    ###############################################################
    def test_create_ingredient_successful(self):
        """Test creating a new ingredient"""
        payload={'name':'veniger'}
        self.client.post(INGREDIENTS_URL,payload)

        exists=Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)
    
    def test_create_Ingredient_invalid(self):
        """Test creating invalid ingredient fails"""
        payload={'name':''}
        res=self.client.post(INGREDIENTS_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST )