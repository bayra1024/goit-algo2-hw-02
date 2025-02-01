from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

    def __init__(self, job: Dict):
        self.id = job["id"]
        self.volume = job["volume"]
        self.priority = job["priority"]
        self.print_time = job["print_time"]


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

    def __init__(self, constraint: Dict):
        self.max_volume = constraint["max_volume"]
        self.max_items = constraint["max_items"]


@dataclass
class PrintOrder:
    volume: float
    max_items: int
    time: int
    items: List

    def __init__(self, pc: PrinterConstraints):
        self.volume = pc.max_volume
        self.max_items = pc.max_items
        self.time = 0
        self.items = list()


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Тут повинен бути ваш код
    pc = PrinterConstraints(constraints)
    job_list = [PrintJob(job) for job in print_jobs]
    exec_jobs = []

    print_step = PrintOrder(pc)
    print_order = []

    for i in range(1, 3 + 1):  # тому що цикл буде виконуватися 3 рази
        for j in job_list:  # проходимо по списку
            if j.priority == i:
                # print(f"TEST JOB: {j}")
                if print_step.volume > j.volume and print_step.max_items > 0:
                    print_step.items.append(j)
                    # print_jobs.remove(j)
                    print_step.volume -= j.volume
                    print_step.max_items -= 1
                    print_step.time = max(print_step.time, j.print_time)
                    print_order.append(j.id)
                else:
                    exec_jobs.append(print_step)
                    print_step = PrintOrder(pc)
                    print_step.items.append(j)
                    # print_jobs.remove(job)
                    print_step.volume -= j.volume
                    print_step.max_items -= 1
                    print_step.time = max(print_step.time, j.print_time)
                    print_order.append(j.id)

    exec_jobs.append(print_step)

    print(exec_jobs)
    exec_time = 0
    for ep in exec_jobs:
        exec_time += ep.time

    return {"print_order": print_order, "total_time": exec_time}

    # {
    #     "print_order": ["M1", "M2", "M3"],  # порядок друку завдань
    #     "total_time": 360,  # загальний час у хвилинах
    # }

    # return {"print_order": None, "total_time": None}


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {
            "id": "M3",
            "volume": 120,
            "priority": 3,
            "print_time": 150,
        },  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]

    constraints = {"max_volume": 300, "max_items": 2}

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
