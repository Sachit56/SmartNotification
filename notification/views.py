from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count,Q
from django.utils.timezone import timedelta,now
from .utils import save_queue_notification,get_user_agent
from .tasks import notify_users
from .permissions import IsSubcribed


# Create your views here.

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)

            return Response({
                'message':'user created successfully',
            },status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(CreateAPIView):

    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh_token = RefreshToken.for_user(user)

            agent = get_user_agent(request)

            print('Agent:',agent)

            try:
                user_agent = get_user_agent(request)

                if not UserLoginRecord.objects.filter(user=user,user_agent=str(user_agent)).exists():
                    UserLoginRecord.objects.create(user=user,user_agent=str(user_agent))

                    notification = Notification.objects.create(
                        user = user,
                        message = f'User ({user}) has logged in using unrecognized device.',
                        event='login'
                    )
                    try:
                        preference = NotificationPreference.objects.get(user=user).preference
                    except NotificationPreference.DoesNotExist:
                        preference = 'app'

                    notify_users.delay(preference,notification.id)

            except Exception as e:
                print(f'[LoginView] Error detecting unrecognized device: {e}')


            return Response({
                'access': str(refresh_token.access_token)
            },status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ThreadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        threads = Threads.objects.all()
        serializer = ThreadSerializer(instance=threads, many=True)
        
        return Response({
            'threads': serializer.data
        },status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = ThreadSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                'message':'new thread created successfully.',
                'threads':serializer.data
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
class ThreadSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ThreadSubscriptionSerializer(data=request.data)

        if serializer.is_valid():
            thread = serializer.validated_data['threads']

            subscription,created = ThreadSubscription.objects.get_or_create(
                user=request.user,
                threads=thread
            )  
            if created:
                return Response({
                    'message':'Subcribed successfully'
                },status=status.HTTP_201_CREATED) 
            return Response({
                'message':'Already Subscribed to the thread.'
            },status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

            
class NotificationPreferenceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            preference = NotificationPreference.objects.get(user=request.user)
            serializers = NotificationPreferenceSerializer(preference)

            return Response({'preference':serializers.data},status=status.HTTP_200_OK)
        except NotificationPreference.DoesNotExist:
            return Response({'message':'Preference has not been set yet.'},status=status.HTTP_404_NOT_FOUND)

    
    def post(self,request):

        if NotificationPreference.objects.filter(user=request.user).exists():
            return Response({'message':'Prefence already exists'},status=status.HTTP_200_OK)

        serializer = NotificationPreferenceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user = request.user)

            return Response({
                'message':'Preference Added successfully'
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self,request):

        try:
            preference = NotificationPreference.objects.get(user=request.user)
        except NotificationPreference.DoesNotExist:
            return Response({'message':"Notification Preference doesn't exist"},status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationPreferenceSerializer(preference,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Preference Updated successfully',
                'preference':serializer.data
            },status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

def thread_websocket_view(request):
    return render(request,'notification/index.html')



class UnreadNotificationView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            unread_notification = Notification.objects.filter(is_read=False,user=request.user)
            serializer = NotificationSerializer(unread_notification,many=True)

            return Response({'unread_notification':serializer.data},status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


class NotificationHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            all_notification = Notification.objects.filter(user=request.user)
            serializer = NotificationSerializer(all_notification,many=True)

            return Response({'notification_history':serializer.data},status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
        
class ReadNotificationView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):
        notifications = Notification.objects.filter(user=request.user,is_read=False)

        if not notifications:
            return Response({
                'message':'Unread Notification not available.'
            },status=status.HTTP_404_NOT_FOUND)
        
        notifications.update(is_read=True)

        return Response({
            'message':'Read all the notification.'
        },status=status.HTTP_200_OK)
    

class CommentView(APIView):

    permission_classes = [IsAuthenticated,IsSubcribed]

    def get(self,request,thread_id):
        
        comments = Comment.objects.filter(thread=thread_id)

        if not comments:
            return Response({
                'message':'No comments posted yet.'
            },status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comments,many=True)

        return Response({
            'comments':serializer.data,
        },status=status.HTTP_200_OK)
    
    def post(self,request,thread_id):
        
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            print('Hello',request.user)
            thread = Threads.objects.get(id=thread_id)
            serializer.save(user=request.user,thread=thread)

            return Response({
                'message':'Comment posted successfully.',
                'data': serializer.data
            },status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class WeeklyReportView(APIView):

    permission_classes = [IsAuthenticated,IsSubcribed]

    def get(self,request,thread_id):

        time_threshold = now().date() - timedelta(days=7)

        query = Threads.objects.filter(id=thread_id)

        thread_comments = query.annotate(total_comments=Count('comments', filter=Q(comments__created_at__gte=time_threshold))).first()
        thread_subscriptions = query.annotate(total_subscriptions=Count('subscriptions', filter=Q(subscriptions__subscribed_at__gte=time_threshold))).first()

        data = {
            'thread':thread_comments.title,
            'total_comments':thread_comments.total_comments,
            'total_subscriptions':thread_subscriptions.total_subscriptions
        }
        other_subscribers = ThreadSubscription.objects.filter(threads=thread_id).exclude(user=request.user)

        message = f'User({(request.user)}) requested to generate weekly report of thread({thread_comments.title})'

        if data:
            for subscriber in other_subscribers:
                save_queue_notification(subscriber,message,'report')

        return Response({
            'data':data
        },status=status.HTTP_200_OK)