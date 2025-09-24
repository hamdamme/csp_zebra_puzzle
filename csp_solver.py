# -*- coding: utf-8 -*-
"""
Zebra Puzzle (CSP) Solver
Backtracking + MRV with all 14 rules enforced.

Author: Hamdam Aynazarov
"""

from copy import deepcopy

# Categories and allowed values (must match app.py)
COLORS         = ["Red", "Blue", "Green", "Yellow", "White"]
NATIONALITIES  = ["American", "Indian", "Mexican", "Pakistani", "German"]
PETS           = ["Raccoon", "Monkey", "Parrot", "Dog", "Fish"]
DRINKS         = ["Water", "Tea", "Horchata", "Milk", "Beer"]
SPORTS         = ["Jogging", "Cricket", "Polo", "Soccer", "Swimming"]

CATS = ["Color", "Nationality", "Pet", "Drink", "Sport"]
HOUSE_INDEXES = list(range(5))


def initial_domains(partial=None):
    """
    Domains: dict[cat] -> list[5] of sets of possible values for each house.
    `partial` can be a dict like { "Color": ["", "Blue", "", "", ""], ... } from the UI.
    """
    domains = {
        "Color":       [set(COLORS)        for _ in HOUSE_INDEXES],
        "Nationality": [set(NATIONALITIES) for _ in HOUSE_INDEXES],
        "Pet":         [set(PETS)          for _ in HOUSE_INDEXES],
        "Drink":       [set(DRINKS)        for _ in HOUSE_INDEXES],
        "Sport":       [set(SPORTS)        for _ in HOUSE_INDEXES],
    }

    # Apply unary clues
    # 8. Tea is drunk in the third house (index 2)
    domains["Drink"][2] = {"Tea"}
    # 9. American lives in the first house (index 0)
    domains["Nationality"][0] = {"American"}

    # Apply any partial assignments from UI
    if partial:
        for cat, vals in partial.items():
            if cat not in domains:
                continue
            for i, v in enumerate(vals):
                if v and v.strip():
                    domains[cat][i] = {v}

    # Basic all-different forward checking for each category
    for cat in CATS:
        placed = [next(iter(s)) for s in domains[cat] if len(s) == 1]
        for i in HOUSE_INDEXES:
            if len(domains[cat][i]) > 1:
                domains[cat][i] -= set(placed)

    return domains


def is_complete(domains):
    return all(len(domains[cat][i]) == 1 for cat in CATS for i in HOUSE_INDEXES)


def get_assignment(domains):
    """Return a readable assignment dict[cat] -> list of chosen values (strings)"""
    result = {}
    for cat in CATS:
        result[cat] = [next(iter(domains[cat][i])) for i in HOUSE_INDEXES]
    return result


def index_of(value, cell_sets):
    """Given a value and a list[5] of sets, return index if uniquely placed, else None."""
    idxs = [i for i, s in enumerate(cell_sets) if value in s]
    if len(idxs) == 1 and len(cell_sets[idxs[0]]) == 1:
        return idxs[0]
    # If it's assigned somewhere, return that index
    assigned = [i for i, s in enumerate(cell_sets) if len(s) == 1 and next(iter(s)) == value]
    return assigned[0] if assigned else None


def maybe_pos(value, cell_sets):
    """Return all indices where 'value' is still possible (domain contains it)."""
    return [i for i, s in enumerate(cell_sets) if value in s]


def enforce_all_diff(domains, cat):
    """Simple all-different pruning: remove placed values from others."""
    placed = [next(iter(s)) for s in domains[cat] if len(s) == 1]
    changed = False
    for i in HOUSE_INDEXES:
        if len(domains[cat][i]) > 1:
            before = len(domains[cat][i])
            domains[cat][i] -= set(placed)
            if len(domains[cat][i]) == 0:
                return False  # contradiction
            changed = changed or (len(domains[cat][i]) != before)
    return True


def consistent_with_rules(domains):
    """
    Check all rules that can be checked with current domains.
    If something is impossible, return False.
    """
    C = domains["Color"]
    N = domains["Nationality"]
    P = domains["Pet"]
    D = domains["Drink"]
    S = domains["Sport"]

    # Helper: if X <-> Y (biconditional), enforce consistency when assigned
    def biconditional(lhs_sets, lhs_val, rhs_sets, rhs_val):
        # If a house is assigned lhs_val, that same house must be rhs_val
        for i in HOUSE_INDEXES:
            if lhs_val in lhs_sets[i]:
                # if this cell i is exactly lhs_val, then rhs must allow rhs_val
                if len(lhs_sets[i]) == 1 and lhs_val in lhs_sets[i]:
                    if rhs_val not in rhs_sets[i]:
                        return False
                # If rhs is assigned and is different, conflict
                if len(rhs_sets[i]) == 1 and rhs_val not in rhs_sets[i] and lhs_val in lhs_sets[i] and len(lhs_sets[i]) == 1:
                    return False
        return True

    # 1. Indian ↔ Blue
    if not biconditional(N, "Indian", C, "Blue"): return False
    if not biconditional(C, "Blue", N, "Indian"): return False

    # 2. Pakistani ↔ Parrot
    if not biconditional(N, "Pakistani", P, "Parrot"): return False
    if not biconditional(P, "Parrot", N, "Pakistani"): return False

    # 3. Green ↔ Beer
    if not biconditional(C, "Green", D, "Beer"): return False
    if not biconditional(D, "Beer", C, "Green"): return False

    # 4. Mexican ↔ Horchata
    if not biconditional(N, "Mexican", D, "Horchata"): return False
    if not biconditional(D, "Horchata", N, "Mexican"): return False

    # 6. Cricket ↔ Monkey
    if not biconditional(S, "Cricket", P, "Monkey"): return False
    if not biconditional(P, "Monkey", S, "Cricket"): return False

    # 7. Red ↔ Jogging
    if not biconditional(C, "Red", S, "Jogging"): return False
    if not biconditional(S, "Jogging", C, "Red"): return False

    # 12. Polo ↔ Milk
    if not biconditional(S, "Polo", D, "Milk"): return False
    if not biconditional(D, "Milk", S, "Polo"): return False

    # 13. German ↔ Soccer
    if not biconditional(N, "German", S, "Soccer"): return False
    if not biconditional(S, "Soccer", N, "German"): return False

    # 5. Green is immediately to the right of Yellow (Yellow at i, Green at i+1)
    # If Yellow fixed at i, Green must be i+1; if Green fixed at j, Yellow must be j-1
    yellow_idxs = maybe_pos("Yellow", C)
    green_idxs  = maybe_pos("Green", C)
    # If either color cannot be placed anywhere, fail:
    if not yellow_idxs or not green_idxs:
        return False
    # If either is assigned, check consistency
    y = [i for i in HOUSE_INDEXES if len(C[i]) == 1 and next(iter(C[i])) == "Yellow"]
    g = [i for i in HOUSE_INDEXES if len(C[i]) == 1 and next(iter(C[i])) == "Green"]
    if y and g:
        if g[0] != y[0] + 1:
            return False

    # 8. Tea is in house 3 is already unary applied.
    # 9. American is in house 1 already unary applied.

    # 10. Raccoon next to Swimmer
    # If Raccoon assigned at i, at least one neighbor must be Swimming-possible
    for i in HOUSE_INDEXES:
        if len(P[i]) == 1 and next(iter(P[i])) == "Raccoon":
            neighbors = []
            if i > 0: neighbors.append(i-1)
            if i < 4: neighbors.append(i+1)
            if not any("Swimming" in S[j] for j in neighbors):
                return False

    # 11. Jogger next to Dog
    for i in HOUSE_INDEXES:
        if len(S[i]) == 1 and next(iter(S[i])) == "Jogging":
            neighbors = []
            if i > 0: neighbors.append(i-1)
            if i < 4: neighbors.append(i+1)
            if not any("Dog" in P[j] for j in neighbors):
                return False

    # 14. American next to White
    # If American at i, at least one neighbor must be White-possible
    for i in HOUSE_INDEXES:
        if len(N[i]) == 1 and next(iter(N[i])) == "American":
            neighbors = []
            if i > 0: neighbors.append(i-1)
            if i < 4: neighbors.append(i+1)
            if not any("White" in C[j] for j in neighbors):
                return False

    # All-different feasibility checks: each value must be possible somewhere
    for cat, values in [("Color", COLORS), ("Nationality", NATIONALITIES),
                        ("Pet", PETS), ("Drink", DRINKS), ("Sport", SPORTS)]:
        cell_sets = domains[cat]
        for v in values:
            if not any(v in s for s in cell_sets):
                return False

    return True


def select_unassigned_variable(domains):
    """
    MRV: pick the (cat, index) with the smallest domain size > 1.
    """
    best = None
    best_size = 10**9
    for cat in CATS:
        for i in HOUSE_INDEXES:
            size = len(domains[cat][i])
            if size > 1 and size < best_size:
                best = (cat, i)
                best_size = size
    return best  # None if all assigned


def assign_and_propagate(domains, cat, idx, val):
    """
    Assign value to (cat, idx), clone domains, propagate all-different, check rules.
    Return new_domains or None if contradiction.
    """
    new_domains = deepcopy(domains)

    # Assign
    new_domains[cat][idx] = {val}

    # All-different for this category
    if not enforce_all_diff(new_domains, cat):
        return None

    # Quick prune: remove val from other houses in same category already done by enforce_all_diff.
    # Check rule consistency
    if not consistent_with_rules(new_domains):
        return None

    return new_domains


def backtrack(domains):
    if is_complete(domains):
        return domains

    var = select_unassigned_variable(domains)
    if var is None:
        return None
    cat, idx = var

    # Try values in current domain (heuristic could be improved with LCV)
    for val in sorted(domains[cat][idx]):
        nd = assign_and_propagate(domains, cat, idx, val)
        if nd is not None:
            result = backtrack(nd)
            if result is not None:
                return result

    return None


def solve(partial=None):
    """
    Solve the puzzle. `partial` is an optional dict from the UI:
      { "Color": [...], "Nationality": [...], ... } with "" for unfilled cells.
    Returns: assignment dict[cat]->list[str] or None if no solution.
    """
    dom = initial_domains(partial)
    if not consistent_with_rules(dom):
        return None
    res = backtrack(dom)
    if res is None:
        return None
    return get_assignment(res)