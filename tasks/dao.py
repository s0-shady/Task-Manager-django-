"""
TAS-5: Data Access Object (DAO) - TYLKO dostęp do bazy danych.
Zasada DRY: 
  - Bazowe query zdefiniowane raz w _base_query()
  - Filtry aktywnych rekordów w _active()
  - Domyślne sortowanie w DEFAULT_ORDER
  - Metoda save() używana przez wszystkie modyfikacje
Zasada Single Responsibility: DAO odpowiada TYLKO za operacje na bazie.
"""

from django.db.models import QuerySet
from .models import Task, Priority, Attachment


class TaskDAO:
    """Data Access Object for Task model"""
    
    # Domyślne sortowanie (DRY - zdefiniowane raz)
    DEFAULT_ORDER_UNCOMPLETED = ['-priority__weight', 'date_added']
    DEFAULT_ORDER_COMPLETED = ['-completion_date']
    
    # ===== BAZOWE QUERY (DRY) =====
    
    @staticmethod
    def _base_query() -> QuerySet:
        """Bazowe query - select_related zdefiniowane RAZ."""
        return Task.objects.select_related('priority')
    
    @staticmethod
    def _active() -> QuerySet:
        """Aktywne (nieusunięte) rekordy."""
        return TaskDAO._base_query().filter(deleted=False)
    
    # ===== POBIERANIE DANYCH =====
    
    @staticmethod
    def get_uncompleted(order_by: list = None) -> QuerySet:
        """Pobierz nieukończone taski."""
        order_by = order_by or TaskDAO.DEFAULT_ORDER_UNCOMPLETED
        return TaskDAO._active().filter(completion_date__isnull=True).order_by(*order_by)
    
    @staticmethod
    def get_completed(order_by: list = None) -> QuerySet:
        """Pobierz ukończone taski."""
        order_by = order_by or TaskDAO.DEFAULT_ORDER_COMPLETED
        return TaskDAO._active().filter(completion_date__isnull=False).order_by(*order_by)
    
    @staticmethod
    def get_by_id(pk: int) -> Task:
        """Pobierz task po ID."""
        return TaskDAO._active().get(pk=pk)
    
    @staticmethod
    def get_for_completion(pk: int) -> Task:
        """Pobierz task do ukończenia (nieukończony)."""
        return TaskDAO._active().get(pk=pk, completion_date__isnull=True)
    
    @staticmethod
    def get_for_restore(pk: int) -> Task:
        """Pobierz task do przywrócenia (ukończony)."""
        return TaskDAO._active().get(pk=pk, completion_date__isnull=False)
    
    # ===== MODYFIKACJA DANYCH =====
    
    @staticmethod
    def _save(instance: Task) -> Task:
        """Zapisz task (DRY - używane przez wszystkie modyfikacje)."""
        instance.save()
        return instance
    
    @staticmethod
    def soft_delete(task: Task) -> Task:
        """Miękkie usunięcie."""
        task.deleted = True
        return TaskDAO._save(task)
    
    @staticmethod
    def complete(task: Task, completion_date) -> Task:
        """Oznacz jako ukończony."""
        task.completion_date = completion_date
        return TaskDAO._save(task)
    
    @staticmethod
    def restore(task: Task) -> Task:
        """Przywróć do nieukończonych."""
        task.completion_date = None
        return TaskDAO._save(task)


class PriorityDAO:
    """Data Access Object for Priority model"""
    
    # Domyślne sortowanie (DRY)
    DEFAULT_ORDER = ['-weight']
    
    # ===== BAZOWE QUERY (DRY) =====
    
    @staticmethod
    def _base_query() -> QuerySet:
        """Bazowe query."""
        return Priority.objects
    
    @staticmethod
    def _active() -> QuerySet:
        """Aktywne (nieusunięte) rekordy."""
        return PriorityDAO._base_query().filter(deleted=False)
    
    # ===== POBIERANIE DANYCH =====
    
    @staticmethod
    def get_all(order_by: list = None) -> QuerySet:
        """Pobierz wszystkie aktywne priorytety."""
        order_by = order_by or PriorityDAO.DEFAULT_ORDER
        return PriorityDAO._active().order_by(*order_by)
    
    @staticmethod
    def get_by_id(pk: int) -> Priority:
        """Pobierz priorytet po ID."""
        return PriorityDAO._active().get(pk=pk)
    
    # ===== MODYFIKACJA DANYCH =====
    
    @staticmethod
    def _save(instance: Priority) -> Priority:
        """Zapisz priorytet (DRY)."""
        instance.save()
        return instance
    
    @staticmethod
    def soft_delete(priority: Priority) -> Priority:
        """Miękkie usunięcie."""
        priority.deleted = True
        return PriorityDAO._save(priority)


class AttachmentDAO:
    """Data Access Object for Attachment model"""
    
    # Domyślne sortowanie (DRY)
    DEFAULT_ORDER = ['-uploaded_at']
    
    # ===== BAZOWE QUERY (DRY) =====
    
    @staticmethod
    def _base_query() -> QuerySet:
        """Bazowe query."""
        return Attachment.objects
    
    @staticmethod
    def _with_task() -> QuerySet:
        """Query z dołączonym taskiem."""
        return AttachmentDAO._base_query().select_related('task')
    
    # ===== POBIERANIE DANYCH =====
    
    @staticmethod
    def get_for_task(task_id: int) -> QuerySet:
        """Pobierz załączniki dla taska."""
        return AttachmentDAO._base_query().filter(task_id=task_id).order_by(*AttachmentDAO.DEFAULT_ORDER)
    
    @staticmethod
    def get_by_id(pk: int) -> Attachment:
        """Pobierz załącznik po ID."""
        return AttachmentDAO._with_task().get(pk=pk)
    
    # ===== MODYFIKACJA DANYCH =====
    
    @staticmethod
    def create(task: Task, file, filename: str) -> Attachment:
        """Utwórz załącznik."""
        return AttachmentDAO._base_query().create(task=task, file=file, filename=filename)
    
    @staticmethod
    def delete(attachment: Attachment) -> None:
        """Usuń załącznik (trwale)."""
        if attachment.file:
            attachment.file.delete(save=False)
        attachment.delete()
