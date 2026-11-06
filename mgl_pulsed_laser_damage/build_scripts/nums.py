import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
def L(n): return json.load(open(os.path.join(HERE, n)))
V = L("part_valid.json"); OM = L("part_opt_models.json"); OP = L("part_opt_pareto.json")
OF = L("part_opt_frontier.json"); OS = L("part_opt_sens.json"); C = L("part_compare.json")
