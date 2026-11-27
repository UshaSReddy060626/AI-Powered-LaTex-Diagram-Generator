"""Core agent: natural language / sketch -> compiled, refinable TikZ (IBM Granite on watsonx.ai)."""
import base64, os, re, shutil, subprocess, tempfile
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()
try:
       from rag import retrieve
except Exception:
       retrieve = None

SYSTEM_PROMPT = r"""You are an expert LaTeX/TikZ engineer producing publication-quality figures for academic papers.
Rules:
- Output ONLY one complete TikZ picture: \begin{tikzpicture} ... \end{tikzpicture}, inside a ```latex fence.
- Allowed libraries only: arrows.meta, positioning, shapes.geometric, shapes.multipart, calc, fit, backgrounds, decorations.pathreplacing, matrix, quotes.
- Use named nodes, relative positioning (right=of A), and node distance. Never hard-code fragile absolute coordinates unless drawing plots/geometry.
- Style for papers: black/grayscale by default, thin lines, font=\small, consistent node sizes, Stealth arrows.
- Define reusable styles with \tikzset inside the picture options.
- No \documentclass, no \usepackage, no commentary outside the code fence."""

REFINE_PROMPT = """Here is the current TikZ code:
```latex
{code}
```
Apply this change and return the FULL updated picture. Keep every existing node, edge and label unless the change asks you to remove it. Change nothing else: {instruction}"""

REPAIR_PROMPT = """This TikZ code failed to compile.
```latex
{code}
```
LaTeX errors:
{errors}
Fix the errors and return the full corrected picture."""

PREAMBLE = r"""\documentclass[tikz,border=4pt]{standalone}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,shapes.multipart,calc,fit,backgrounds,decorations.pathreplacing,matrix,quotes}
\begin{document}
%s
\end{document}
"""


def extract_tikz(text: str) -> str:
    m = re.search(r"```(?:latex|tex)?\s*(.*?)```", text, re.S)
    code = (m.group(1) if m else text).strip()
    m = re.search(r"\\begin\{tikzpicture\}.*\\end\{tikzpicture\}", code, re.S)
    return m.group(0) if m else code


@dataclass
class CompileResult:
    ok: bool
    errors: str = ""
    pdf: bytes | None = None
    png: bytes | None = None


def compile_tikz(code: str, timeout: int = 120) -> CompileResult:
    if not shutil.which("pdflatex"):
        return CompileResult(False, "pdflatex not found. Install MiKTeX (Windows) or TeX Live (Linux/Mac).")
    with tempfile.TemporaryDirectory() as d:
        tex = Path(d) / "fig.tex"
        tex.write_text(PREAMBLE % code, encoding="utf-8")
        try:
            p = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-no-shell-escape", "fig.tex"],
                cwd=d, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        except subprocess.TimeoutExpired:
            return CompileResult(False, "Compilation timed out.")
        pdf = Path(d) / "fig.pdf"
        if p.returncode != 0 or not pdf.exists():
            errs = [l for l in p.stdout.splitlines() if l.startswith("!") or l.startswith("l.")]
            return CompileResult(False, "\n".join(errs[:12]) or p.stdout[-800:])
        png = None
        try:
            try:
                import pymupdf as fitz  # PyMuPDF (current name)
            except ImportError:
                import fitz  # older PyMuPDF
            doc = fitz.open(str(pdf))
            png = doc[0].get_pixmap(dpi=200).tobytes("png")
            doc.close()
        except Exception:
            pass
        return CompileResult(True, "", pdf.read_bytes(), png)


@dataclass
class Version:
    instruction: str
    code: str
    result: CompileResult


@dataclass
class DiagramAgent:
    max_repairs: int = 3
    history: list[Version] = field(default_factory=list)

    def __post_init__(self):
        creds = Credentials(url=os.environ["WATSONX_URL"], api_key=os.environ["WATSONX_APIKEY"])
        self._creds = creds
        self._pid = os.environ["WATSONX_PROJECT_ID"]
        self.params = {"temperature": 0.1, "max_tokens": 2000}
        self.text_llm = ModelInference(model_id=os.getenv("TEXT_MODEL", "ibm/granite-4-h-small"),
                                       credentials=creds, project_id=self._pid, params=self.params)
        self._vision_llm = None  # created only when a sketch is uploaded

    # ---- LLM helpers -------------------------------------------------
    def _chat(self, user: str) -> str:
        msgs = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user}]
        return self.text_llm.chat(messages=msgs)["choices"][0]["message"]["content"]

    @property
    def vision_llm(self):
        if self._vision_llm is None:
            self._vision_llm = ModelInference(
                model_id=os.getenv("VISION_MODEL", "mistralai/mistral-small-3-1-24b-instruct-2503"),
                credentials=self._creds, project_id=self._pid, params=self.params)
        return self._vision_llm

    def describe_sketch(self, image_bytes: bytes, mime: str = "image/png") -> str:
        b64 = base64.b64encode(image_bytes).decode()
        msgs = [{"role": "user", "content": [
            {"type": "text", "text": "This is a hand-drawn diagram. List every node (with its label and shape), "
                                     "every edge (source -> target, direction, label), and the overall layout "
                                     "(left-to-right, grid, layers...). Be precise and exhaustive."},
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}]}]
        return self.vision_llm.chat(messages=msgs)["choices"][0]["message"]["content"]

    # ---- public API --------------------------------------------------
    def _examples_block(self, query: str) -> str:
        if retrieve is None:
            return ""
        try:
            hits = retrieve(query, k=1)
        except Exception:
            return ""
        parts = [f"Example for \"{h['description']}\":\n```latex\n{h['code']}\n```" for h in hits]
        return ("Here is a verified, compilable TikZ example of a similar diagram. "
                "Use it ONLY as a guide for style: node shapes, arrow style and spacing. "
                "The structure, labels and connections must follow the user's request, "
                "not the example.\n\n" + "\n\n".join(parts) + "\n\n")

    def generate(self, description: str, sketch: bytes | None = None, mime: str = "image/png") -> Version:
        prompt = description
        if sketch:
            prompt = f"Sketch analysis:\n{self.describe_sketch(sketch, mime)}\n\nUser request:\n{description or 'Recreate this sketch.'}"
        examples = self._examples_block(prompt)
        raw = self._chat(f"{examples}Create a TikZ diagram for:\n{prompt}")
        return self._compile_with_repair(prompt, raw, description)

    def refine(self, instruction: str) -> Version:
        if not self.history:
            raise ValueError("Nothing to refine yet; call generate() first.")
        raw = self._chat(REFINE_PROMPT.format(code=self.history[-1].code, instruction=instruction))
        return self._compile_with_repair(instruction, raw, instruction)

    def undo(self):
        if len(self.history) > 1:
            self.history.pop()
        return self.history[-1] if self.history else None

    def _compile_with_repair(self, _ctx, raw, label) -> Version:
        code = extract_tikz(raw)
        res = compile_tikz(code)
        for _ in range(self.max_repairs):
            if res.ok:
                break
            code = extract_tikz(self._chat(REPAIR_PROMPT.format(code=code, errors=res.errors)))
            res = compile_tikz(code)
        v = Version(label, code, res)
        self.history.append(v)
        return v