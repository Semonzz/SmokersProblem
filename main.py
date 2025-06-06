"""
Solving Cigarette smokers problem
"""
import threading
import time
import random


tobacco_paper = threading.Semaphore(0)
tobacco_matches = threading.Semaphore(0)
paper_matches = threading.Semaphore(0)
agent_sem = threading.Semaphore(1)


def agent() -> None:
    """
    Agent function, that takes supplies, and give 1 to smoker's semaphore
    """
    combinations = [
        (tobacco_paper, "tobacco and paper"),
        (tobacco_matches, "tobacco and matches"),
        (paper_matches, "paper and matches")
    ]
    while True:
        agent_sem.acquire()
        comb_sem, comb_name = random.choice(combinations)
        print(f"\nAgent put: {comb_name}")
        comb_sem.release()


def smoker(name: str, needed_sem: threading.Semaphore) -> None:
    """
    Smoker function, that init time for smoke and give agent signal to continue pick supplies
    Args:
    :name: name of smoker
    :needed_sem: semaphore needed for follow smoker
    """
    while True:
        needed_sem.acquire()
        print(f"{name} taked supplies")
        agent_sem.release()
        print(f"{name} smoking...")
        time.sleep(5)
        print(f"{name} finished smoking.")


threads = [threading.Thread(target=agent),
           threading.Thread(target=smoker, args=("Smoker with tobacco", paper_matches)),
           threading.Thread(target=smoker, args=("Smoker with paper", tobacco_matches)),
           threading.Thread(target=smoker, args=("Smoker with matches", tobacco_paper))]

for thread in threads:
    thread.start()
