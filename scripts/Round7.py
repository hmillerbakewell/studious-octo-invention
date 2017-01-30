"""
Apply the simple annealing algorith with:
Lazy scoring
Balanced type-generation
No fixed types
"""

import conceptual_spaces

# real time cost is roughly one secound per round on my machine

def print_results():
    "Anneals and then prints steps line by line"
    results = conceptual_spaces.simple_annealing_v1("POS_ONLY", 45, 10000)
    for result in results:
        print result

print_results()
