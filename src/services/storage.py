from src.models.task import Task
from uuid import uuid4, UUID

# Создаем хранилище, где TaskStorage.data = {uuid: task}
class TaskStorage:
    def __init__(self):
        self.data: dict = {}

    def add(self, task: Task) -> UUID:
        task_id = uuid4()
        self.data[task_id] = task
        return task_id

    def get(self, task_id: UUID) -> Task:
        return self.data[task_id]

# Создаем новое хранилище задач
new_storage = TaskStorage()