import streamlit as st
from tikz_agent import DiagramAgent

st.set_page_config(page_title="TikZ Diagram Agent", layout="wide")
st.title("AI LaTeX Diagram Generator")
st.caption("IBM Granite on watsonx.ai · describe or sketch → compile-checked TikZ → refine in plain English")

if "agent" not in st.session_state:
    st.session_state.agent = DiagramAgent()
agent: DiagramAgent = st.session_state.agent

left, right = st.columns(2)
with left:
    desc = st.text_area("Describe your diagram", height=130,
                        placeholder="Three-layer neural network: 3 inputs, 4 hidden nodes, 2 outputs, fully connected, left to right.")
    up = st.file_uploader("…or upload a sketch (optional)", type=["png", "jpg", "jpeg"])
    if st.button("Generate", type="primary", disabled=not (desc or up)):
        with st.spinner("Granite is drawing, compiling and self-correcting…"):
            agent.history.clear()
            agent.generate(desc, up.getvalue() if up else None, up.type if up else "image/png")
    if agent.history:
        cmd = st.chat_input("Refine: e.g. 'make arrows dashed', 'add a label Softmax under the output layer'")
        if cmd:
            with st.spinner("Applying change…"):
                agent.refine(cmd)
        if st.button("↩ Undo last change"):
            agent.undo()

if agent.history:
    v = agent.history[-1]
    with right:
        if v.result.ok:
            st.success(f"Compiled · version {len(agent.history)}")
            if v.result.png:
                st.image(v.result.png)
            st.download_button("Download PDF", v.result.pdf, "figure.pdf")
        else:
            st.error("Could not produce compilable code after automatic repair attempts.")
            st.code(v.result.errors)
        st.code(v.code, language="latex")
        st.download_button("Download .tex snippet", v.code, "figure.tex")
        with st.expander("History"):
            for i, h in enumerate(agent.history, 1):
                st.write(f"{i}. {h.instruction[:100]}  {'✅' if h.result.ok else '❌'}")
