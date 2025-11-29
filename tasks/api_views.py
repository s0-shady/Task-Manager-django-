"""
TAS-2: REST API dla sortowania.
Używa services.py - nie ma bezpośredniego dostępu do bazy (DRY, Single Responsibility).
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import services as srs
from .serializers import TaskSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_tasks_uncompleted(request):
    """
    GET /api/tasks/uncompleted/
    Query params: sort_by, sort_order
    """
    sort_by = request.query_params.get('sort_by', 'priority')
    sort_order = request.query_params.get('sort_order', 'desc')
    
    # Walidacja
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    if not srs.is_valid_sort_field(sort_by):
        return Response(
            {'error': f'Invalid sort_by. Allowed: {srs.get_allowed_sort_fields()}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Pobierz dane przez services
    data = srs.get_sorted_uncompleted_tasks(sort_by, sort_order)
    serializer = TaskSerializer(data['tasks'], many=True)
    
    return Response({
        'tasks': serializer.data,
        'sort_by': data['sort_by'],
        'sort_order': data['sort_order'],
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_tasks_completed(request):
    """
    GET /api/tasks/completed/
    Query params: sort_by, sort_order
    """
    sort_by = request.query_params.get('sort_by', 'completion_date')
    sort_order = request.query_params.get('sort_order', 'desc')
    
    # Walidacja
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    if not srs.is_valid_sort_field(sort_by):
        return Response(
            {'error': f'Invalid sort_by. Allowed: {srs.get_allowed_sort_fields()}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Pobierz dane przez services
    data = srs.get_sorted_completed_tasks(sort_by, sort_order)
    serializer = TaskSerializer(data['tasks'], many=True)
    
    return Response({
        'tasks': serializer.data,
        'sort_by': data['sort_by'],
        'sort_order': data['sort_order'],
    })
