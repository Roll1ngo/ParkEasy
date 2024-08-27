from celery.result import AsyncResult

# Замініть 'your_task_id' на реальний ID вашого завдання
task_id = 'c1277f88-fa36-4b98-8e46-46d3b9bb5266'

result = AsyncResult(task_id)
print(result.info)
# print(f"Task Result: {result.result}")  # Для отримання результатів
