from src.models.task import Task
from uuid import uuid4, UUID

# Создаем хранилище, где TaskStorage.data = {uuid: task}
class TaskStorage:
    def __init__(self):
        self._data: dict = {}

    def add(self, task: Task) -> UUID:
        task_id = uuid4()
        self._data[task_id] = task
        return task_id

    def get(self, task_id: UUID) -> Task:
        return self._data[task_id]

# Создаем новое хранилище задач
new_storage = TaskStorage()