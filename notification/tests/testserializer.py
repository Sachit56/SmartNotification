from rest_framework.test import APITestCase
from notification.serializers import *

class UserSerializerTest(APITestCase):
    
    def test_user_serializer(self):
        data = {
            'username':'NewUser',
            'email':'Newuser@gmail.com',
            'password':'admin'
        }

        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['username'],'NewUser')
        user = serializer.save()

        self.assertEqual(user.email,'Newuser@gmail.com')