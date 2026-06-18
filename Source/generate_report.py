"""Generate the project report PDF from code and experiment artifacts."""

import csv
from collections import defaultdict
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


BASE = Path(__file__).resolve().parent
OUT = BASE / "Report.pdf"


def para(text, style):
    return Paragraph(text.replace("\n", "<br/>"), style)


def table(data, widths=None):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#172033")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#9aa6b2")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f9fb")]),
            ]
        )
    )
    return t


def read_experiments():
    path = BASE / "Outputs" / "experiment_results.csv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def count_constraints():
    rows = []
    for path in sorted((BASE / "Inputs").glob("input-*.txt")):
        lines = [line.split("#", 1)[0].strip() for line in path.read_text(encoding="utf-8").splitlines()]
        lines = [line for line in lines if line]
        n = int(lines[0])
        grid = lines[1 : 1 + n]
        h = lines[1 + n : 1 + n + n]
        v = lines[1 + n + n : 1 + n + n + n - 1]
        clues = sum(1 for line in grid for item in line.split(",") if int(item.strip()) != 0)
        cons = sum(1 for line in h + v for item in line.split(",") if int(item.strip()) != 0)
        rows.append([path.name, n, clues, cons])
    return rows


def build():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8, leading=10))
    if "CodeSmall" not in styles:
        styles.add(ParagraphStyle(name="CodeSmall", parent=styles["BodyText"], fontName="Courier", fontSize=8, leading=10))

    story = []
    story.append(Paragraph("Project 2. Logic - Futoshiki Puzzles", styles["Title"]))
    story.append(Paragraph("Report", styles["Heading2"]))
    story.append(para("Team members: StudentID1, StudentID2. Contribution: StudentID1 50%, StudentID2 50%.", styles["BodyText"]))
    story.append(para("Video URLs: add YouTube or Google Drive links after recording the required demonstrations.", styles["BodyText"]))
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("Self-Evaluation", styles["Heading1"]))
    story.append(
        table(
            [
                ["Criterion", "Status"],
                ["FOL formalization", "Included below with complete rules and three CNF derivations."],
                ["Automatic KB/CNF generation", "Implemented in kb_generator.py and cnf_generator.py."],
                ["Forward chaining", "Implemented with Horn facts/rules plus deterministic propagation."],
                ["Backward chaining", "Implemented with unification-based Horn query helper and SLD-style DFS search."],
                ["A* search", "Implemented with admissible remaining-cells heuristic and metrics."],
                ["Brute force and backtracking", "Implemented and compared on all ten inputs."],
                ["Experiments", "Runtime, memory, nodes, assignments, inferences, and frontier are reported."],
                ["GUI", "Optional Tkinter GUI implemented in gui.py."],
            ],
            [2.0 * inch, 4.6 * inch],
        )
    )

    story.append(Paragraph("Formal FOL Axioms", styles["Heading1"]))
    axioms = [
        "Domain: row, column, and value variables range over {1,...,N}.",
        "A1: For all i,j, exists v such that Val(i,j,v).",
        "A2: For all i,j,v1,v2, Val(i,j,v1) and Val(i,j,v2) implies v1 = v2.",
        "A3: For all i,j1,j2,v, Val(i,j1,v) and Val(i,j2,v) and j1 != j2 implies contradiction.",
        "A4: For all j,i1,i2,v, Val(i1,j,v) and Val(i2,j,v) and i1 != i2 implies contradiction.",
        "A5: For all i,j,v, Given(i,j,v) implies Val(i,j,v).",
        "A6: For all i,j,v1,v2, LessH(i,j) and Val(i,j,v1) and Val(i,j+1,v2) implies Less(v1,v2).",
        "A7: For all i,j,v1,v2, GreaterH(i,j) and Val(i,j,v1) and Val(i,j+1,v2) implies Less(v2,v1).",
        "A8: For all i,j,v1,v2, LessV(i,j) and Val(i,j,v1) and Val(i+1,j,v2) implies Less(v1,v2).",
        "A9: For all i,j,v1,v2, GreaterV(i,j) and Val(i,j,v1) and Val(i+1,j,v2) implies Less(v2,v1).",
        "A10: For every value v in the finite domain, each row and each column contains v at least once.",
    ]
    for item in axioms:
        story.append(para(item, styles["BodyText"]))

    story.append(Paragraph("CNF Derivations", styles["Heading1"]))
    derivations = [
        "Given enforcement: Given(i,j,v) -> Val(i,j,v). Eliminate implication: not Given(i,j,v) or Val(i,j,v). Clause: {~Given(i,j,v), Val(i,j,v)}.",
        "At most one value: Val(i,j,v1) and Val(i,j,v2) -> false for v1 != v2. Eliminate implication: not (Val(i,j,v1) and Val(i,j,v2)). Distribute: {~Val(i,j,v1), ~Val(i,j,v2)}.",
        "Horizontal less: LessH(i,j) and Val(i,j,v1) and Val(i,j+1,v2) -> Less(v1,v2). For violating pairs v1 >= v2, replace consequent by false, giving clause {~LessH(i,j), ~Val(i,j,v1), ~Val(i,j+1,v2)}.",
        "Row uniqueness: Val(i,j1,v) and Val(i,j2,v) and j1 != j2 -> false. Since j1 != j2 is fixed after grounding, each pair j1 < j2 creates {~Val(i,j1,v), ~Val(i,j2,v)}.",
    ]
    for item in derivations:
        story.append(para(item, styles["BodyText"]))

    story.append(Paragraph("Algorithm Summaries", styles["Heading1"]))
    story.append(para("Forward chaining: initialize Given and constraint facts, apply Horn rules until fixed point, update singleton domains and hidden singles, and detect empty domains as contradictions. If propagation stalls, branch on the smallest domain.", styles["BodyText"]))
    story.append(para("Backward chaining: query Val(i,j,v) goals with a unification-based Horn helper, choose the unassigned cell with the smallest provable domain, and use depth-first SLD-style search.", styles["BodyText"]))
    story.append(para("A*: a state is a partial assignment. g(s) is the number of assignments added after the initial state. h(s) is the number of unassigned cells. Each action fills one cell, so h never overestimates the minimum remaining assignments and is admissible.", styles["BodyText"]))
    story.append(para("Backtracking uses MRV for variable selection. Brute force fills cells in row-major order with only local consistency pruning, so it is a weaker baseline.", styles["BodyText"]))

    story.append(PageBreak())
    story.append(Paragraph("Input Coverage", styles["Heading1"]))
    story.append(table([["Input", "N", "Clues", "Inequality constraints"]] + count_constraints(), [1.4 * inch, 0.6 * inch, 0.8 * inch, 1.8 * inch]))

    experiments = read_experiments()
    story.append(Paragraph("Experiment Results", styles["Heading1"]))
    if experiments:
        compact = [["Input", "N", "Method", "Solved", "Time(s)", "Peak KB", "Nodes", "Assign", "Infer", "Frontier"]]
        for row in experiments:
            compact.append(
                [
                    row["input"],
                    row["N"],
                    row["method"],
                    row["solved"],
                    row["runtime_seconds"],
                    row["peak_kb"],
                    row["nodes_expanded"],
                    row["assignments_tried"],
                    row["inferences"],
                    row["max_frontier"],
                ]
            )
        story.append(table(compact, [0.82 * inch, 0.32 * inch, 0.75 * inch, 0.48 * inch, 0.62 * inch, 0.55 * inch, 0.45 * inch, 0.48 * inch, 0.48 * inch, 0.48 * inch]))

        by_method = defaultdict(list)
        for row in experiments:
            by_method[row["method"]].append(float(row["runtime_seconds"]))
        summary = [["Method", "Average runtime (s)", "Solved cases"]]
        for method, values in sorted(by_method.items()):
            solved = sum(1 for row in experiments if row["method"] == method and row["solved"] == "True")
            summary.append([method, f"{sum(values) / len(values):.6f}", solved])
        story.append(Spacer(1, 0.15 * inch))
        story.append(table(summary, [1.4 * inch, 1.5 * inch, 1.0 * inch]))
    else:
        story.append(para("Run python run_experiments.py to generate experiment_results.csv.", styles["BodyText"]))

    story.append(Paragraph("Comparative Analysis", styles["Heading1"]))
    story.append(para("The generated cases contain many clues, so all algorithms solve them quickly. Forward chaining often expands one search node because propagation derives enough singleton domains. A* and backtracking expand similar numbers of states because both use small-domain choices; A* additionally tracks a priority frontier. Brute force is slower in less constrained cases because it uses row-major order instead of MRV.", styles["BodyText"]))

    story.append(Paragraph("References", styles["Heading1"]))
    story.append(para("Course assignment handout: Project 2. Logic - Futoshiki Puzzles.", styles["BodyText"]))

    doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
