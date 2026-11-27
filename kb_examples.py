EXAMPLES = [
    {
        "description": "Linear flowchart pipeline: Data to Preprocess to Model, boxes connected left to right with arrows",
        "code": r"""\begin{tikzpicture}[node distance=1.6cm, box/.style={draw, rectangle, minimum width=2.2cm, minimum height=0.9cm, font=\small}, arrow/.style={-{Stealth}, thick}]
\node[box] (a) {Data};
\node[box, right=of a] (b) {Preprocess};
\node[box, right=of b] (c) {Model};
\draw[arrow] (a) -- (b);
\draw[arrow] (b) -- (c);
\end{tikzpicture}""",
    },
    {
        "description": "Flowchart with a decision diamond, Yes and No branches and a feedback loop back to the start",
        "code": r"""\begin{tikzpicture}[node distance=1.5cm and 2cm, box/.style={draw, rectangle, minimum width=2.2cm, minimum height=0.9cm, font=\small}, dec/.style={draw, diamond, aspect=2, inner sep=1pt, font=\small}, arrow/.style={-{Stealth}, thick}]
\node[box] (train) {Train};
\node[dec, right=of train] (check) {Accuracy $>$ 90\%?};
\node[box, right=of check] (deploy) {Deploy};
\node[box, below=of check] (tune) {Tune};
\draw[arrow] (train) -- (check);
\draw[arrow] (check) -- node[above, font=\scriptsize] {Yes} (deploy);
\draw[arrow] (check) -- node[right, font=\scriptsize] {No} (tune);
\draw[arrow] (tune) -| (train);
\end{tikzpicture}""",
    },
    {
        "description": "Fully connected neural network with input, hidden and output layers drawn as circles with labels",
        "code": r"""\begin{tikzpicture}[neuron/.style={circle, draw, minimum size=0.7cm}, arrow/.style={-{Stealth}, thin}]
\foreach \i in {1,2,3} \node[neuron] (in\i) at (0,-\i) {};
\foreach \j in {1,2,3,4} \node[neuron] (h\j) at (2.5,-\j+0.5) {};
\foreach \k in {1,2} \node[neuron] (out\k) at (5,-\k-0.5) {};
\foreach \i in {1,2,3} \foreach \j in {1,2,3,4} \draw[arrow] (in\i) -- (h\j);
\foreach \j in {1,2,3,4} \foreach \k in {1,2} \draw[arrow] (h\j) -- (out\k);
\node[above=0.3cm of in1, font=\small] {Input};
\node[above=0.3cm of h1, font=\small] {Hidden};
\node[above=0.3cm of out1, font=\small] {Output};
\end{tikzpicture}""",
    },
    {
        "description": "Binary tree with a root and two levels of children drawn as circles with numeric labels",
        "code": r"""\begin{tikzpicture}[vertex/.style={circle, draw, minimum size=0.8cm, font=\small}]
\node[vertex] (r) at (0,0) {8};
\node[vertex] (l) at (-2,-1.3) {3};
\node[vertex] (rr) at (2,-1.3) {10};
\node[vertex] (ll) at (-3,-2.6) {1};
\node[vertex] (lr) at (-1,-2.6) {6};
\node[vertex] (rrr) at (3,-2.6) {14};
\draw (r) -- (l);
\draw (r) -- (rr);
\draw (l) -- (ll);
\draw (l) -- (lr);
\draw (rr) -- (rrr);
\end{tikzpicture}""",
    },
    {
        "description": "State machine with three states Idle, Running and Stopped connected by labelled transition arrows",
        "code": r"""\begin{tikzpicture}[node distance=3cm, st/.style={draw, circle, minimum size=1.4cm, font=\small}, arrow/.style={-{Stealth}, thick}]
\node[st] (idle) {Idle};
\node[st, right=of idle] (run) {Running};
\node[st, right=of run] (stop) {Stopped};
\draw[arrow] (idle) -- node[above, font=\scriptsize] {start} (run);
\draw[arrow] (run) -- node[above, font=\scriptsize] {stop} (stop);
\end{tikzpicture}""",
    },
    {
        "description": "Three-tier architecture with browser, web server and database boxes and labelled arrows between them",
        "code": r"""\begin{tikzpicture}[node distance=2.2cm, box/.style={draw, rectangle, minimum width=2.4cm, minimum height=1cm, font=\small}, arrow/.style={-{Stealth}, thick}]
\node[box] (c) {Browser};
\node[box, right=of c] (s) {Web Server};
\node[box, right=of s] (d) {Database};
\draw[arrow] (c) -- node[above, font=\scriptsize] {request} (s);
\draw[arrow] (s) -- node[above, font=\scriptsize] {query} (d);
\end{tikzpicture}""",
    },

    {
        "description": "UML class diagram with a parent class Animal and two subclasses Dog and Cat, with attributes, methods and inheritance arrows",
        "code": r"""\begin{tikzpicture}[class/.style={draw, rectangle split, rectangle split parts=3, minimum width=3cm, font=\small, align=left}, inherit/.style={-{Triangle[open, length=4mm, width=4mm]}, thick}]
\node[class] (animal) {\textbf{Animal}\nodepart{second}+ name: String\nodepart{third}+ speak(): void};
\node[class, below=1.8cm of animal, xshift=-2.2cm] (dog) {\textbf{Dog}\nodepart{second}+ breed: String\nodepart{third}+ fetch(): void};
\node[class, below=1.8cm of animal, xshift=2.2cm] (cat) {\textbf{Cat}\nodepart{second}+ indoor: Boolean\nodepart{third}+ purr(): void};
\draw[inherit] (dog.north) -- (animal.south);
\draw[inherit] (cat.north) -- (animal.south);
\end{tikzpicture}""",
    },
    {
        "description": "Encoder-decoder architecture with input, encoder, latent vector, decoder and output connected left to right",
        "code": r"""\begin{tikzpicture}[node distance=1.4cm, box/.style={draw, rectangle, minimum width=2cm, minimum height=1cm, font=\small}, latent/.style={draw, ellipse, minimum width=1.8cm, minimum height=1cm, font=\small}, arrow/.style={-{Stealth}, thick}]
\node[box] (in) {Input};
\node[box, right=of in] (enc) {Encoder};
\node[latent, right=of enc] (z) {Latent $z$};
\node[box, right=of z] (dec) {Decoder};
\node[box, right=of dec] (out) {Output};
\draw[arrow] (in) -- (enc);
\draw[arrow] (enc) -- (z);
\draw[arrow] (z) -- (dec);
\draw[arrow] (dec) -- (out);
\end{tikzpicture}""",
    },
    {
        "description": "Organisation chart tree with a CEO at the top and three vice presidents below connected by elbow lines",
        "code": r"""\begin{tikzpicture}[box/.style={draw, rectangle, minimum width=2.4cm, minimum height=0.8cm, font=\small}, line/.style={thick}]
\node[box] (ceo) at (0,0) {CEO};
\node[box] (v1) at (-3.5,-1.8) {VP Engineering};
\node[box] (v2) at (0,-1.8) {VP Sales};
\node[box] (v3) at (3.5,-1.8) {VP Finance};
\draw[line] (ceo.south) -- ++(0,-0.7) -| (v1.north);
\draw[line] (ceo.south) -- ++(0,-0.7) -| (v2.north);
\draw[line] (ceo.south) -- ++(0,-0.7) -| (v3.north);
\end{tikzpicture}""",
    },
    {
        "description": "State machine with Idle, Running, Paused and Stopped states with start, stop, pause and resume transitions",
        "code": r"""\begin{tikzpicture}[node distance=3cm, st/.style={draw, circle, minimum size=1.5cm, font=\small}, arrow/.style={-{Stealth}, thick}]
\node[st] (idle) {Idle};
\node[st, right=of idle] (run) {Running};
\node[st, below=of run] (pause) {Paused};
\node[st, right=of run] (stop) {Stopped};
\draw[arrow] (idle) -- node[above, font=\scriptsize] {start} (run);
\draw[arrow] (run) -- node[above, font=\scriptsize] {stop} (stop);
\draw[arrow] (run) to[bend left=20] node[right, font=\scriptsize] {pause} (pause);
\draw[arrow] (pause) to[bend left=20] node[left, font=\scriptsize] {resume} (run);
\end{tikzpicture}""",
    },
    {
        "description": "Layered software architecture with three stacked layers Presentation, Business Logic and Data Access connected by downward arrows",
        "code": r"""\begin{tikzpicture}[node distance=1.1cm, layer/.style={draw, rectangle, minimum width=5cm, minimum height=0.9cm, font=\small}, arrow/.style={-{Stealth}, thick}]
\node[layer] (p) {Presentation Layer};
\node[layer, below=of p] (b) {Business Logic Layer};
\node[layer, below=of b] (d) {Data Access Layer};
\draw[arrow] (p) -- (b);
\draw[arrow] (b) -- (d);
\end{tikzpicture}""",
    },
    {
        "description": "Top to bottom flowchart with rounded Start and End terminators and process boxes in between",
        "code": r"""\begin{tikzpicture}[node distance=1.2cm, term/.style={draw, rounded corners=8pt, minimum width=2.4cm, minimum height=0.8cm, font=\small}, box/.style={draw, rectangle, minimum width=2.4cm, minimum height=0.8cm, font=\small}, arrow/.style={-{Stealth}, thick}]
\node[term] (s) {Start};
\node[box, below=of s] (i) {Read input};
\node[box, below=of i] (p) {Process data};
\node[term, below=of p] (e) {End};
\draw[arrow] (s) -- (i);
\draw[arrow] (i) -- (p);
\draw[arrow] (p) -- (e);
\end{tikzpicture}""",
    },
    {
        "description": "Venn diagram of two overlapping circles labelled Machine Learning and Statistics with Data Science in the overlap",
        "code": r"""\begin{tikzpicture}
\draw[thick, fill=gray!25, fill opacity=0.5] (0,0) circle (1.5cm);
\draw[thick, fill=gray!25, fill opacity=0.5] (1.6,0) circle (1.5cm);
\node[font=\small, align=center] at (-0.7,0) {ML};
\node[font=\small, align=center] at (2.3,0) {Statistics};
\node[font=\scriptsize, align=center] at (0.8,0) {Data\\Science};
\end{tikzpicture}""",
    },
    {
        "description": "Transformer encoder block stacked bottom to top with input embedding, multi-head attention, add and norm, feed-forward and output",
        "code": r"""\begin{tikzpicture}[node distance=0.9cm, box/.style={draw, rectangle, minimum width=3.6cm, minimum height=0.8cm, font=\small}, arrow/.style={-{Stealth}, thick}]
\node[box] (emb) {Input Embedding};
\node[box, above=of emb] (att) {Multi-Head Attention};
\node[box, above=of att] (n1) {Add \& Norm};
\node[box, above=of n1] (ff) {Feed-Forward};
\node[box, above=of ff] (n2) {Add \& Norm};
\node[box, above=of n2] (out) {Output};
\draw[arrow] (emb) -- (att);
\draw[arrow] (att) -- (n1);
\draw[arrow] (n1) -- (ff);
\draw[arrow] (ff) -- (n2);
\draw[arrow] (n2) -- (out);
\end{tikzpicture}""",
    },
]