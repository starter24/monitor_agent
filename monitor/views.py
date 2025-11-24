from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .stream_handler import monitor_instance

def index(request):
    return render(request, 'index.html')

@api_view(['POST'])
def start_monitor(request):
    monitor_instance.start()
    return Response({"status": "started"})

@api_view(['POST'])
def stop_monitor(request):
    monitor_instance.stop()
    return Response({"status": "stopped"})

@api_view(['GET'])
def get_status(request):
    return Response({"running": monitor_instance.running})
