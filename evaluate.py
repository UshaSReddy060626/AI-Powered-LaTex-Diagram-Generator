"""Compare diagram generation WITHOUT and WITH retrieval (RAG) on a fixed set of prompts.

Run:  python evaluate.py
Outputs: results.csv, eval_out/*.png (diagram images to rate by eye), and a summary table.
"""
import csv, pathlib, sys, time

import tikz_agent
from tikz_agent import DiagramAgent, REPAIR_PROMPT, extract_tikz, compile_tikz

PROMPTS = [
    "Flowchart of an online shopping checkout: browse, add to cart, pay, confirm order.",
    "Flowchart with a decision: is the user logged in? If yes show the profile page, if no show the login page.",
    "Neural network with 2 inputs, 3 hidden neurons and 1 output, fully connected, left to right.",
    "Binary search tree with root 15, children 10 and 20, and leaves 5, 12 and 25.",
    "State machine for a traffic light with Red, Green and Yellow states and timer transitions.",
    "State machine for a door with Open, Closed and Locked states.",
    "UML class diagram with a class Vehicle and subclasses Car and Truck, with attributes and methods.",
    "UML class diagram of Student and Course classes with an association labelled enrolls in.",
    "Organisation chart of a university: Chancellor, two deans, and two departments under each dean.",
    "Three-layer web architecture: client, API server, database, with labelled arrows.",
    "Encoder-decoder model for translation: source sentence, encoder, context vector, decoder, target sentence.",
    "Machine learning pipeline: data collection, cleaning, feature engineering, training, evaluation, with a feedback arrow from evaluation back to training.",
    "Venn diagram with three overlapping circles labelled A, B and C.",
    "Layered network model with four stacked layers: Application, Transport, Network, Link.",
    "Software development lifecycle as a loop: Plan, Build, Test, Release, then back to Plan.",
    "Transformer decoder block with masked self-attention, cross-attention and feed-forward, stacked bottom to top.",
]


def run_one(agent, prompt):
    """Returns (first_try_ok, final_ok, repairs, png_bytes, error_text)."""
    examples = agent._examples_block(prompt)
    raw = agent._chat(f"{examples}Create a TikZ diagram for:\n{prompt}")
    code = extract_tikz(raw)
    res = compile_tikz(code)
    if res.ok:
        return True, True, 0, res.png, ""
    repairs = 0
    for _ in range(agent.max_repairs):
        code = extract_tikz(agent._chat(REPAIR_PROMPT.format(code=code, errors=res.errors)))
        res = compile_tikz(code)
        repairs += 1
        if res.ok:
            break
    return False, res.ok, repairs, res.png, ("" if res.ok else res.errors[:200])


def evaluate(agent, mode, out_dir):
    rows = []
    for i, prompt in enumerate(PROMPTS, 1):
        print(f"[{mode}] {i}/{len(PROMPTS)}  {prompt[:60]}...", flush=True)
        try:
            first, final, repairs, png, err = run_one(agent, prompt)
        except Exception as e:  # network/quota/etc.
            first, final, repairs, png, err = False, False, 0, None, f"EXCEPTION: {e}"[:200]
        if png:
            (out_dir / f"{mode}_{i:02d}.png").write_bytes(png)
        rows.append({"mode": mode, "id": i, "prompt": prompt, "first_try_ok": first,
                     "final_ok": final, "repairs": repairs, "error": err})
    return rows


def summarize(rows, mode):
    r = [x for x in rows if x["mode"] == mode]
    n = len(r)
    first = sum(x["first_try_ok"] for x in r)
    final = sum(x["final_ok"] for x in r)
    avg_rep = sum(x["repairs"] for x in r) / n
    return f"{mode:<8} first-try compile: {first}/{n} ({100*first/n:.0f}%)   after repair: {final}/{n} ({100*final/n:.0f}%)   avg repairs: {avg_rep:.2f}"


def main():
    real_retrieve = tikz_agent.retrieve
    if real_retrieve is None:
        print("Retrieval is not available (rag import failed). Fix that first.")
        sys.exit(1)
    out_dir = pathlib.Path("eval_out")
    out_dir.mkdir(exist_ok=True)
    agent = DiagramAgent()
    all_rows = []
    for mode in ("no_rag", "rag"):
        tikz_agent.retrieve = None if mode == "no_rag" else real_retrieve
        all_rows += evaluate(agent, mode, out_dir)
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        w.writeheader()
        w.writerows(all_rows)
    print("\n===== SUMMARY =====")
    print(summarize(all_rows, "no_rag"))
    print(summarize(all_rows, "rag"))
    print("\nSaved results.csv and eval_out/ (open the PNGs to rate how good each diagram looks).")


if __name__ == "__main__":
    main()
