from collections import deque

# Erstelle eine Queue mit Maximalgröße 3
q = deque(maxlen=3)

q.append(1)
q.append(2)
q.append(3)
print(q)  # deque([1, 2, 3], maxlen=3)

q.append(4)
print(q)  # deque([2, 3, 4], maxlen=3) — das älteste Element (1) wurde automatisch entfernt

q.append(5)
print(q)  # deque([3, 4, 5], maxlen=3)