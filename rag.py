"""Vector-indexed knowledge base of verified TikZ examples (IBM watsonx.ai Slate embeddings).

Usage:
    python rag.py build                      # embed all examples and save kb_index.json
    python rag.py test "decision flowchart"  # show the closest examples for a query
"""
import json, os, sys
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Embeddings

from kb_examples import EXAMPLES

load_dotenv()

INDEX_PATH = Path(__file__).with_name("kb_index.json")
EMBED_MODEL = os.getenv("EMBED_MODEL", "ibm/granite-embedding-278m-multilingual")

_embedder = None
_index = None


def _get_embedder():
    global _embedder
    if _embedder is None:
        creds = Credentials(url=os.environ["WATSONX_URL"], api_key=os.environ["WATSONX_APIKEY"])
        _embedder = Embeddings(model_id=EMBED_MODEL, credentials=creds,
                               project_id=os.environ["WATSONX_PROJECT_ID"])
    return _embedder


def _embed(texts):
    return _get_embedder().embed_documents(texts=texts)


def build_index():
    vectors = _embed([e["description"] for e in EXAMPLES])
    items = [{"description": e["description"], "code": e["code"], "vector": v}
             for e, v in zip(EXAMPLES, vectors)]
    INDEX_PATH.write_text(json.dumps({"model": EMBED_MODEL, "items": items}), encoding="utf-8")
    print(f"Indexed {len(items)} examples with {EMBED_MODEL} -> {INDEX_PATH.name}")


def _load_index():
    global _index
    if _index is None:
        if not INDEX_PATH.exists():
            build_index()
        _index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return _index


def retrieve(query: str, k: int = 2):
    """Return the k most similar examples as a list of {description, code, score}."""
    idx = _load_index()
    q = np.array(_embed([query])[0], dtype=float)
    q /= np.linalg.norm(q) + 1e-12
    scored = []
    for item in idx["items"]:
        v = np.array(item["vector"], dtype=float)
        v /= np.linalg.norm(v) + 1e-12
        scored.append((float(q @ v), item))
    scored.sort(key=lambda t: t[0], reverse=True)
    return [{"description": it["description"], "code": it["code"], "score": s} for s, it in scored[:k]]


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "build":
        build_index()
    elif len(sys.argv) >= 3 and sys.argv[1] == "test":
        for r in retrieve(" ".join(sys.argv[2:]), k=3):
            print(f"{r['score']:.3f}  {r['description']}")
    else:
        print(__doc__)
