"""
TAS-5: Services - warstwa logiki biznesowej.
Zasada Single Responsibility: Services łączy dane z różnych DAO i przygotowuje dla widoków.
Zasada DRY: Każda funkcja get_*_data() jest wywoływana z wielu miejsc (views, API).
"""

from django.utils import timezone
from .dao import TaskDAO, PriorityDAO, AttachmentDAO


# ==================== TASK SERVICES ====================

def get_task_list_data() -> dict:
    """
    Pobierz dane dla widoku listy zadań.
    Używane w: task_list view, potencjalnie w API.
    """
    return {
        'uncompleted_tasks': TaskDAO.get_uncompleted(),
        'completed_tasks': TaskDAO.get_completed(),
    }


def get_task_detail_data(task_id: int) -> dict:
    """
    Pobierz dane dla widoku szczegółów zadania.
    Łączy task + jego załączniki.
    """
    return {
        'task': TaskDAO.get_by_id(task_id),
        'attachments': AttachmentDAO.get_for_task(task_id),
    }


def get_task_for_form(task_id: int) -> dict:
    """Pobierz task do formularza edycji."""
    return {'task': TaskDAO.get_by_id(task_id)}


def get_task_for_delete(task_id: int) -> dict:
    """Pobierz task do potwierdzenia usunięcia."""
    return {'task': TaskDAO.get_by_id(task_id)}


def get_task_for_complete(task_id: int) -> dict:
    """Pobierz task do potwierdzenia ukończenia."""
    return {'task': TaskDAO.get_for_completion(task_id)}


def get_task_for_restore(task_id: int) -> dict:
    """Pobierz task do potwierdzenia przywrócenia."""
    return {'task': TaskDAO.get_for_restore(task_id)}


def complete_task(task_id: int):
    """Ukończ zadanie."""
    task = TaskDAO.get_for_completion(task_id)
    TaskDAO.complete(task, timezone.now().date())


def restore_task(task_id: int):
    """Przywróć zadanie do nieukończonych."""
    task = TaskDAO.get_for_restore(task_id)
    TaskDAO.restore(task)


def delete_task(task_id: int):
    """Usuń zadanie (soft delete)."""
    task = TaskDAO.get_by_id(task_id)
    TaskDAO.soft_delete(task)


# ==================== PRIORITY SERVICES ====================

def get_priority_list_data() -> dict:
    """Pobierz dane dla widoku listy priorytetów."""
    return {'priorities': PriorityDAO.get_all()}


def get_priority_for_form(priority_id: int) -> dict:
    """Pobierz priorytet do formularza edycji."""
    return {'priority': PriorityDAO.get_by_id(priority_id)}


def get_priority_for_delete(priority_id: int) -> dict:
    """Pobierz priorytet do potwierdzenia usunięcia."""
    return {'priority': PriorityDAO.get_by_id(priority_id)}


def delete_priority(priority_id: int):
    """Usuń priorytet (soft delete)."""
    priority = PriorityDAO.get_by_id(priority_id)
    PriorityDAO.soft_delete(priority)


# ==================== ATTACHMENT SERVICES ====================

def get_attachment_form_data(task_id: int) -> dict:
    """Pobierz dane dla formularza załącznika."""
    return {'task': TaskDAO.get_by_id(task_id)}


def get_attachment_for_delete(attachment_id: int) -> dict:
    """Pobierz załącznik do potwierdzenia usunięcia."""
    return {'attachment': AttachmentDAO.get_by_id(attachment_id)}


def create_attachment(task_id: int, file, filename: str):
    """Dodaj załącznik do taska."""
    task = TaskDAO.get_by_id(task_id)
    AttachmentDAO.create(task, file, filename)


def delete_attachment(attachment_id: int) -> int:
    """Usuń załącznik. Zwraca task_id do przekierowania."""
    attachment = AttachmentDAO.get_by_id(attachment_id)
    task_id = attachment.task.pk
    AttachmentDAO.delete(attachment)
    return task_id


# ==================== API SERVICES (dla sortowania TAS-2) ====================

# Mapowanie pól do sortowania (DRY - zdefiniowane raz)
SORT_FIELD_MAP = {
    'id': 'id',
    'title': 'title',
    'date_added': 'date_added',
    'priority': 'priority__weight',
    'completion_date': 'completion_date',
}


def get_sorted_uncompleted_tasks(sort_by: str, sort_order: str) -> dict:
    """Pobierz nieukończone taski z sortowaniem dla API."""
    order_by = _build_order_by(sort_by, sort_order)
    return {
        'tasks': TaskDAO.get_uncompleted(order_by=order_by),
        'sort_by': sort_by,
        'sort_order': sort_order,
    }


def get_sorted_completed_tasks(sort_by: str, sort_order: str) -> dict:
    """Pobierz ukończone taski z sortowaniem dla API."""
    order_by = _build_order_by(sort_by, sort_order)
    return {
        'tasks': TaskDAO.get_completed(order_by=order_by),
        'sort_by': sort_by,
        'sort_order': sort_order,
    }


def _build_order_by(sort_by: str, sort_order: str) -> list:
    """Zbuduj listę order_by z parametrów. (DRY - używane przez oba endpointy)"""
    if sort_by not in SORT_FIELD_MAP:
        return None
    
    field = SORT_FIELD_MAP[sort_by]
    if sort_order == 'desc':
        field = f'-{field}'
    
    return [field]


def is_valid_sort_field(sort_by: str) -> bool:
    """Sprawdź czy pole sortowania jest prawidłowe."""
    return sort_by in SORT_FIELD_MAP


def get_allowed_sort_fields() -> list:
    """Pobierz listę dozwolonych pól sortowania."""
    return list(SORT_FIELD_MAP.keys())
