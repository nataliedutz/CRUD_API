from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Task
from .serializers import TaskSerializer

class TaskListApi(APIView):
    permission_classes=[permissions.IsAuthenticated]  # authenticated user can see only their own entries, no other entries

    def get(self, request):
        tasks=Task.objects.filter(user=request.user.id)
        serializer=TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request, *args,**kwargs):
        data={
            'task_name': request.data.get("task_name"),
            'completed': request.data.get('completed'),
            'user': request.user.id,
            }
        serializer=TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("Data Saved", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailApi(APIView):

    permission_classes=[permissions.IsAuthenticated]

    def get_object(self, task_id, user_id):
        try:
            return Task.objects.get(user=user_id, id=task_id)
        except Task.DoesNotExist:
            return None
        
    
    def get(self, request, task_id):
        task_instance=self.get_object(task_id,request.user.id)
        if task_instance==None:
            return Response(
                {"result":"Task with this specified task_id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer=TaskSerializer(task_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, task_id, *args, **kwargs):
        '''
        Updates the task item with given task_id if exists
        '''
        task_instance = self.get_object(task_id, request.user.id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task_name': request.data.get('task_name'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        serializer = TaskSerializer(instance = task_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response("Saved updated information", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # 5. Delete
    def delete(self, request, task_id):
        '''
        Deletes the task item with given task_id if exists
        '''
        task_instance = self.get_object(task_id, request.user.id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        task_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
