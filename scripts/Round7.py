"""
Apply the simple annealing algorith with:
Lazy scoring
Balanced type-generation
No fixed types
"""

import conceptual_spaces

# real time cost is roughly one secound per round on my machine

print conceptual_spaces.simple_annealing_v1("POS_ONLY", 20, 10000)
