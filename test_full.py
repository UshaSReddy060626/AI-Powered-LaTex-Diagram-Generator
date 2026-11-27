from tikz_agent import DiagramAgent

a = DiagramAgent()
v = a.generate("Flowchart: Data -> Preprocess -> Model -> Evaluate")
print("Compiled:", v.result.ok)
print(v.result.errors)
print(v.code)