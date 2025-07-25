from rest_framework.permissions import BasePermission
from .models import Threads,ThreadSubscription

class IsSubcribed(BasePermission):

    message = 'Please Subscribe to the thread first.'

    def has_permission(self, request, view):
        thread_id = view.kwargs.get('thread_id')

        if not thread_id:
            self.message = 'Thread ID not provided'
            return False
        
        try:
            thread = Threads.objects.get(id=thread_id)
        except Threads.DoesNotExist:
            self.message = 'Thread Does not exist.'
            return False
        
        if not ThreadSubscription.objects.filter(threads=thread_id,user=request.user).exists():
            self.message = 'Please Subscribe to the thread first.'
            return False

        
        return True
