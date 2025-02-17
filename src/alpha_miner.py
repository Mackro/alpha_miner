import re
import itertools

def construct_arcs(tuples, initials, outputs):
    Fl = []
    for i in initials:
        Fl.append(("Pi", i))
    for tup in tuples:
        A, B = tup
        for a in A:
            Fl.append((a,f"P{tup}"))
        for b in B:
            Fl.append((f"P{tup}", b))
    for o in outputs:
        Fl.append((o, "Po"))
    print(f"Fl = {Fl}")
    return Fl

def construct_places(tuples):
    Pl = ["Pi", "Po"]
    for tup in tuples:
        Pl.append(f"P{tup}")
    print(f"Pl = {Pl}")
    return Pl

def remove_sets(tuples):
    Yl = []
    for t1 in tuples:
        issub = False
        for t2 in tuples:
            if t1 == t2:
                continue
            s11, s12 = t1
            s21, s22 = t2
#            print(f"T1: {s11}, {s12} = {t1}")
#            print(f"T2: {s21}, {s22} = {t2}")
            if s11.issubset(s21) and s12.issubset(s22):
                issub = True
                break
        if not issub:
            Yl.append(t1)
    print(f"Yl = {Yl}")
    return Yl

def construct_sets(transes, footprint):
    transitions = list(transes)
    transitions.sort()
    Xs = []
    for trans1 in transitions:
        friends = [t for t in transitions if f"{trans1}#{t}" in footprint]
        partners = [t for t in transitions if f"{trans1}->{t}" in footprint]
        if not partners:
            continue

        As = [{trans1}]
        for i in range(2,len(friends)+1):
            for subset in itertools.combinations(friends, i):
                include = True
                for t1 in subset:
                    for t2 in subset:
                        if not f"{t1}#{t2}" in footprint:
                            include = False
                if include and trans1 in subset:
                    As.append(set(subset))

        for i in range(1, len(partners)+1):
            for subset in itertools.combinations(partners, i):
                for A in As:
                    match = True
                    for a in A:
                        for b in subset:
                            if not f"{a}->{b}" in footprint:
                                match = False
                            for b2 in subset:
                                if not f"{b}#{b2}" in footprint:
                                    match = False
                    if not match:
                        continue
                    Xs.append((A, set(subset)))

    Xl = []
    for tup in Xs:
        if tup not in Xl:
            Xl.append(tup)
    print(f"Xl = {Xl}")
    return Xl

def get_outputs(log):
    To = set()
    for trace in log:
        To.add(trace[-1])

    print(f"To = {To}")
    return To

def calculate_footprint(log, transitions):
    df_relation = set()
    for trace in log:
        ts = trace.split(",")
        for a, b in itertools.pairwise(ts):
            df_relation.add(f"{a}>{b}")

    print(df_relation)
    relation = set()
    for trans1 in transitions:
        for trans2 in transitions:
            forward = f"{trans1}>{trans2}" in df_relation
            backward = f"{trans2}>{trans1}" in df_relation
            if forward and not backward:
                relation.add(f"{trans1}->{trans2}")
            elif forward and backward:
                relation.add(f"{trans1}||{trans2}")
            elif not forward and not backward:
                relation.add(f"{trans1}#{trans2}")

    print(relation)
    return relation


def get_initials(log):
    Ti = set()
    for trace in log:
        Ti.add(trace[0])

    print(f"Ti = {Ti}")
    return Ti

def get_transitions(log):
    Tl = set()
    for trace in log:
        transitions = set(trace.split(","))
        Tl.update(transitions)

    print(f"Tl = {Tl}")
    return Tl

def get_log():
    log_text = input("enter event log:\n")
    raw_traces = re.split("<|>", log_text.replace(" ", ""))
    traces = [t for t in raw_traces if t.strip()]
    return traces


def main():
    L = get_log()
    Tl = get_transitions(L)
    Ti = get_initials(L)
    To = get_outputs(L)
    footprint = calculate_footprint(L, Tl)
    Xl = construct_sets(Tl, footprint)
    Yl = remove_sets(Xl)
    Pl = construct_places(Yl)
    Fl = construct_arcs(Yl, Ti, To)


if __name__ == '__main__':
    main()
