"""Turn a checked proof into a readable write-up in the usual olympiad style.

The renderer never decides anything: it replays the proof through the
checker and describes what each accepted move did, using the checker's log.
A proof the checker rejects is not rendered as a proof.
"""

from __future__ import annotations

from . import terms as T
from .algebra import Poly, equation_str, monic, poly_str
from .checker import CheckResult, LogEntry, Problem, check
from .solutions import make_family
from .moves import Cancel, Cauchy, Conclude, Divide, Inj, Onto, Pre, Quadratic, Split, SplitNZ, Subst, Surj

DOMAIN_WORD = {"R": "real", "Q": "rational"}
PROPERTY_SENTENCE = {
    "odd": "So f is odd: f(-t) = -f(t) for all t.",
    "even": "So f is even: f(-t) = f(t) for all t.",
    "additive": "So f is additive: f(s + t) = f(s) + f(t) for all s, t.",
    "involution": "So f is an involution: f(f(t)) = t for all t; in particular f is bijective.",
    "injective": "So f is injective.",
    "surjective": "So f is surjective.",
}


def _variables(problem: Problem) -> list[str]:
    return sorted(problem.poly.variables())


def _eq(poly: Poly) -> str:
    return equation_str(poly)


def _renamings(row: Poly) -> set:
    """The copies of a one-variable identity in the other variable names."""
    names = row.variables()
    if len(names) != 1:
        return set()
    (name,) = names
    return {row.subst({name: Poly.var(other)}) for other in "xyz" if other != name}


def _new_facts(entry: LogEntry, skip: Poly | None = None) -> list[str]:
    """Identities worth mentioning after a move: new ones, one copy per renaming,
    leaving out the identity the move itself just displayed."""
    hidden: set = set()
    if skip is not None and not skip.is_zero():
        shown = monic(skip)
        hidden = {shown} | _renamings(shown)
    out = []
    for row in entry.fresh_rows:
        if row in hidden:
            continue
        hidden |= _renamings(row)
        out.append(_eq(row))
    return out[:3]


def _props(entry: LogEntry) -> list[str]:
    names = list(entry.new_props)
    if isinstance(entry.move, Inj):
        names = [n for n in names if n != "injective"]
    if isinstance(entry.move, Surj):
        names = [n for n in names if n != "surjective"]
    if "involution" in names:
        names = [n for n in names if n not in ("injective", "surjective")]
    return [PROPERTY_SENTENCE[n] for n in names]


def _assertion_name(problem: Problem, move: Subst) -> str:
    bindings = dict(move.bindings)
    args = [T.show(bindings[v]) if v in bindings else v for v in _variables(problem)]
    return f"P({', '.join(args)})"


def _describe(problem: Problem, entry: LogEntry) -> list[str]:
    """Sentences for one accepted move."""
    move = entry.move
    lines: list[str] = []
    if isinstance(move, Subst):
        if move.target == "P" or entry.source == problem.poly:
            lead = _assertion_name(problem, move)
        else:
            bindings = ", ".join(f"{name} = {T.show(term)}" for name, term in move.bindings)
            lead = f"Putting {bindings} in {_eq(entry.source)}"
        if entry.closed == "contradiction":
            lines.append(f"{lead} leads to {_absurd(entry.reason)}. So this case is impossible.")
            return lines
        shown = entry.instance
        if shown is not None and not shown.is_zero():
            lines.append(f"{lead} gives {_eq(shown)}.")
        else:
            lines.append(f"{lead}, simplified with what we already know, gives new information.")
        extra = _new_facts(entry, skip=shown)
        if extra:
            lines.append("Together with the earlier relations this yields " + "; ".join(extra) + ".")
    elif isinstance(move, (Split, SplitNZ)):
        labels = [label for label, _ in entry.children]
        fact = _eq(entry.source) if isinstance(move, Split) else None
        if isinstance(move, Split):
            lines.append(f"Since {fact}, we have " + " or ".join(labels) + ".")
        else:
            lines.append("Either " + " or ".join(labels) + ".")
        for label, reason in entry.children:
            if reason is not None:
                lines.append(f"The case {label} is impossible: with the relations above it leads to {_absurd(reason)}.")
    elif isinstance(move, Divide):
        lines.append(f"Since {poly_str(entry.extra)} is nonzero we may divide {_eq(entry.source)} by it.")
        lines.extend(_fact_line(entry))
    elif isinstance(move, Inj):
        lines.append(
            f"f is injective: in {_eq(entry.source)}, if f(a) = f(b) then comparing the identity at a and at b "
            "(same values of the other variables) forces a = b."
        )
    elif isinstance(move, Surj):
        lines.append(
            f"f is surjective: in {_eq(entry.source)}, fixing the other variables, one side is f of something "
            "while the other side takes every value."
        )
    elif isinstance(move, Cancel):
        lines.append(f"Since f is injective, {_eq(entry.source)} gives {_eq(entry.instance)}.")
        lines.extend(_fact_line(entry, skip=entry.instance))
    elif isinstance(move, Pre):
        lines.append(f"Since f is surjective, there is a constant {entry.witness} with f({entry.witness}) = {poly_str(entry.extra)}.")
    elif isinstance(move, Onto):
        v = move.var
        lines.append(
            f"In {_eq(entry.source)} the variable {v} occurs only inside f({v}). Since f is surjective, f({v}) takes "
            f"every value, so we may replace f({v}) by {v}: {_eq(entry.instance)}."
        )
        lines.extend(_fact_line(entry, skip=entry.instance))
    elif isinstance(move, Cauchy):
        if entry.source is not None:
            lines.append(f"The relation {_eq(entry.source)} says that f, minus a suitable polynomial, is additive.")
        lines.append(
            "An additive function on the rationals is linear (g(n) = n g(1) for integers n, then for fractions), "
            f"so {_eq(entry.instance)}."
        )
    elif isinstance(move, Quadratic):
        lines.append(
            f"The relation {_eq(entry.source)} is the quadratic functional equation. On the rationals it forces "
            "f(0) = 0, f even and f(nt) = n^2 f(t) for integers n (induction), hence "
            f"{_eq(entry.instance)}."
        )
    elif isinstance(move, Conclude):
        lines.append(f"Hence f(x) = {poly_str(entry.candidate)} for all x.")
        if not entry.solutions:
            lines.append("Substituting this into the original equation, no choice of the constants works, so this case gives no solutions.")
        else:
            found = "; ".join(make_family(s).describe() for s in entry.solutions)
            lines.append(
                "Substituting this into the original equation and comparing coefficients, it holds exactly for: "
                f"{found}."
            )
        return lines
    if entry.closed == "contradiction" and not isinstance(move, Subst):
        lines.append(f"This leads to {_absurd(entry.reason)}. So this case is impossible.")
        return lines
    if isinstance(move, (Cauchy, Quadratic)):
        lines.extend(_fact_line(entry, skip=entry.instance))
    elif not isinstance(move, (Subst, Divide, Cancel, Onto)):
        lines.extend(_fact_line(entry))
    lines.extend(_props(entry))
    return lines


def _absurd(reason: str) -> str:
    """Phrase a contradiction found by the checker."""
    if reason.endswith(" = 0") and reason[:-4].lstrip("-").replace("/", "").isdigit():
        return f"the absurd equation {reason}"
    return f"a contradiction ({reason})"


def _fact_line(entry: LogEntry, skip: Poly | None = None) -> list[str]:
    facts = _new_facts(entry, skip=skip)
    return ["We now know: " + "; ".join(facts) + "."] if facts else []


def render_result(problem: Problem, result: CheckResult) -> str:
    """Write up a check result (use ``render`` to check and render in one go)."""
    names = _variables(problem)
    quantifier = f"for all {DOMAIN_WORD[problem.domain]} {', '.join(names)}"
    out = [
        f"Problem. Find all functions f: {problem.domain} -> {problem.domain} such that "
        f"{problem.equation} {quantifier}.",
        "",
    ]
    if result.solved:
        out += [f"Answer. {result.solutions}.", ""]
    out.append(f"Solution. Let P({', '.join(names)}) denote the assertion {problem.equation}.")
    log = result.state.log if result.state is not None else ()
    current_case: tuple = ()
    for entry in log:
        if entry.move is None:
            if entry.closed:
                out.append(f"The equation is contradictory as it stands: {entry.reason}.")
            continue
        if entry.case != current_case:
            current_case = entry.case
            if current_case:
                out += ["", f"Case {' and '.join(current_case)}."]
        out.extend(_describe(problem, entry))
    out.append("")
    if result.solved:
        out.append(
            "All cases are closed. Every function listed in the answer was substituted into the original "
            "equation and satisfies it exactly, and the argument above shows there are no others."
        )
    elif not result.ok:
        out.append(f"THE PROOF WAS REJECTED by the checker at move {result.step + 1}: {result.error}")
    else:
        out.append(f"THE PROOF IS INCOMPLETE: {result.error}.")
    return "\n".join(out)


def render(problem: Problem, proof) -> str:
    """Check a proof and write it up. The text says clearly if the proof is not complete."""
    return render_result(problem, check(problem, proof))
