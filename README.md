# AI-Powered LaTeX Diagram Generator

An AI-powered application that converts natural-language descriptions into LaTeX/TikZ diagrams using **IBM watsonx.ai and IBM Granite models**.

Instead of writing complex TikZ code manually, users can simply describe the diagram they want in plain English. The application generates the TikZ code, compiles it into a PDF, checks for errors, and automatically attempts to fix compilation issues.

The generated diagrams can also be modified using simple English instructions.

## Project Overview

Creating diagrams using LaTeX and TikZ can be difficult, especially for beginners. Writing the code manually requires knowledge of TikZ commands, node positioning, shapes, and connections.

This project simplifies the process by using Generative AI and Retrieval-Augmented Generation (RAG) to create diagrams from text descriptions.

The application retrieves a relevant verified TikZ example, uses it as a style reference, and generates new diagram code based on the user's instructions.

The project was initially started during an **IBM SkillsBuild AI & Cloud Virtual Internship** with Edunet Foundation and AICTE. It was later extended into a complete application with additional features.

## Example Outputs

### 1. Vague Prompt vs Detailed Prompt

The quality of the generated diagram depends on how clearly the user describes it.

- A vague prompt such as "Draw an apple" may produce a basic or unexpected result.
- A detailed prompt describing the leaf, stem, shapes, and their positions produces a more accurate result.

### 2. Diagram Refinement

Users can improve an existing diagram through follow-up instructions.

For example:
- Initial version: A compiled tree diagram with an unattached node.
- Improved version: The node is correctly connected after providing a follow-up instruction.

**Note:** A successfully compiled diagram is not always structurally correct. Always check the generated preview.

## Key Features

- **Text-to-Diagram Generation:** Converts plain-English descriptions into flowcharts, binary trees, UML diagrams, neural networks, state machines, and architecture diagrams.
- **RAG-Based Retrieval:** Retrieves the closest matching example from a collection of 14 verified TikZ examples.
- **AI Code Generation:** Uses IBM Granite 4 H Small to generate LaTeX/TikZ code.
- **Automatic Compilation:** Compiles generated code using `pdflatex` and checks for errors.
- **Automatic Error Repair:** Sends compilation errors back to the AI model for correction, with up to three repair attempts.
- **Diagram Refinement:** Allows users to modify existing diagrams using simple English instructions.
- **Version History and Undo:** Keeps track of changes and allows users to undo the last modification.
- **Live Preview:** Displays the generated diagram through the Streamlit interface.
- **Download Options:** Allows users to download diagrams as PDF files or TikZ code.
- **Sketch-to-Diagram (Experimental):** Includes an experimental feature that uses a vision model to understand uploaded sketches and generate diagrams.

## Technologies Used

| Component | Technology |
|---|---|
| Programming Language | Python 3.11 |
| Frontend | Streamlit |
| AI Platform | IBM watsonx.ai |
| Text Generation Model | IBM Granite 4 H Small |
| Embedding Model | IBM Granite Embedding 278M Multilingual |
| Vision Model (Experimental) | Mistral Small 3.1 |
| RAG | Embeddings and Cosine Similarity |
| Diagram Generation | LaTeX / TikZ |
| Compilation | pdflatex |
| PDF Preview | PyMuPDF |

## How Does It Work?

The application follows these steps:

1. **User Input:** The user describes the required diagram in plain English. An image or sketch can also be uploaded experimentally.
2. **Text Embedding:** The description is converted into a numerical representation using IBM Granite Embedding.
3. **Example Retrieval:** Cosine similarity is used to find the closest matching example from 14 verified TikZ examples.
4. **Prompt Construction:** The retrieved example is provided to the AI model as a style reference. The actual diagram structure follows the user's description.
5. **Code Generation:** IBM Granite 4 H Small generates the LaTeX/TikZ code.
6. **Compilation:** The generated code is compiled using `pdflatex`.
7. **Error Correction:** If compilation fails, the error messages are sent back to the AI model for automatic correction, up to three attempts.
8. **Preview Generation:** The compiled PDF is converted into a PNG image using PyMuPDF.
9. **Refinement and Export:** Users can modify the diagram, undo changes, and download the final PDF or `.tex` code.

## System Workflow

```text
       User Description
              |
              v
    Text Embedding (Granite)
              |
              v
      Cosine Similarity
              |
              v
   Retrieve Closest Example
       (14 Examples)
              |
              v
      Prompt Construction
              |
              v
   IBM Granite 4 H Small
              |
              v
       TikZ Code
              |
              v
      pdflatex Compilation
              |
         +----+----+
         |         |
      Success    Failure
         |         |
         |    Error Correction
         |    (Up to 3 Attempts)
         |         |
         |      Recompile
         |         |
         +----+----+
              |
              v
        PDF Generation
              |
              v
       PNG Preview
              |
              v
    Refine / Undo / Download
```

## Project Structure

```text
AI-Powered-LaTeX-Diagram-Generator/
│
├── app.py               # Streamlit application
├── tikz_agent.py        # Diagram generation, compilation and repair
├── rag.py               # Embedding generation and example retrieval
├── kb_examples.py       # Collection of 14 verified TikZ examples
├── evaluate.py          # Evaluates generation with and without RAG
├── compare.py           # Compares generated diagram outputs
├── test_connection.py   # Tests IBM watsonx.ai connection
├── test_full.py         # Tests complete generation and compilation
│
├── requirements.txt     # Required Python packages
├── .env.example         # Environment variable template
├── .gitignore           # Files excluded from Git
├── .dockerignore        # Files excluded from Docker builds
├── Dockerfile           # Optional Docker configuration
├── deploy_ibmcloud.sh   # Optional IBM Cloud deployment script
│
├── docs/                # Example screenshots
├── LICENSE              # MIT License
│
└── kb_index.json        # Generated embedding index (not committed)
```

## Installation and Setup

### Prerequisites

Before running the application, make sure you have:

- Python 3.11 or later.
- An IBM Cloud account.
- A watsonx.ai project.
- A watsonx.ai Runtime service linked to your project.
- An IBM Cloud API key.
- A LaTeX distribution that includes `pdflatex`.

**LaTeX installation options:**
- Windows: MiKTeX
- Linux/macOS: TeX Live

For Windows, allow MiKTeX to install missing packages automatically.

### Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username>/AI-Powered-LaTeX-Diagram-Generator.git

cd AI-Powered-LaTeX-Diagram-Generator
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure IBM watsonx.ai

Create your environment configuration file.

**Windows PowerShell:**
```powershell
Copy-Item .env.example .env
```

**Linux/macOS:**
```bash
cp .env.example .env
```

Open the `.env` file and add your IBM watsonx.ai credentials.

| Variable | Description |
|---|---|
| `WATSONX_URL` | Regional watsonx.ai endpoint |
| `WATSONX_APIKEY` | Your IBM Cloud API key |
| `WATSONX_PROJECT_ID` | Your watsonx.ai project ID |
| `TEXT_MODEL` | Text generation model ID |
| `VISION_MODEL` | Vision model ID |
| `EMBED_MODEL` | Embedding model ID |

Default model IDs:

```text
TEXT_MODEL=ibm/granite-4-h-small
VISION_MODEL=mistralai/mistral-small-3-1-24b-instruct-2503
EMBED_MODEL=ibm/granite-embedding-278m-multilingual
```

**Important:** Model availability depends on your IBM Cloud region. Check the available models in watsonx.ai Prompt Lab and use the appropriate regional endpoint.

**Security:** Never upload your `.env` file, API keys, or private credentials to GitHub. The `.env` file should remain excluded through `.gitignore`.

### Step 5: Build the Knowledge Base (Optional)

```bash
python rag.py build
```

This generates the embedding index used for retrieving relevant TikZ examples.

If the index does not exist, the application automatically builds it when required.

### Step 6: Test the Connection

Check whether the IBM watsonx.ai connection is working:

```bash
python test_connection.py
```

Test the retrieval system:

```bash
python rag.py test "flowchart with a yes no decision"
```

### Step 7: Run the Application

```bash
streamlit run app.py
```

Open the following address in your browser:

```text
http://localhost:8501
```

## How to Use the Application

1. Open the application in your browser.
2. Enter a description of the diagram you want to generate.
3. Click the **Generate** button.
4. Wait for the AI model to generate and compile the TikZ code.
5. Check the generated diagram in the preview.
6. If needed, enter additional instructions to modify the diagram.
7. Use the Undo option to reverse the last modification.
8. Download the final diagram as a PDF or `.tex` file.

**Example prompt:**

```text
Create a login flowchart with a decision:
Is the user logged in?

If yes, display the profile page.
If no, display the login page.
```

**Example refinement instructions:**

```text
Make all arrows dashed.
```

```text
Add node 17 as the left child of node 20.
```

## Using the Exported TikZ Code

The downloaded `.tex` file contains only the `tikzpicture` code.

To use it in another LaTeX document, add the following packages to your document preamble:

```latex
\usepackage{tikz}

\usetikzlibrary{
    arrows.meta,
    positioning,
    shapes.geometric,
    shapes.multipart,
    calc,
    fit,
    backgrounds,
    decorations.pathreplacing,
    matrix,
    quotes
}
```

After adding these packages, paste the downloaded TikZ code into your document.

The exact libraries required may vary depending on the generated diagram.

## Evaluation

The project includes two evaluation scripts:

- `evaluate.py`: Tests 16 different prompts with and without RAG.
- `compare.py`: Creates side-by-side comparisons of the generated diagrams.

The evaluation covers:

- Flowcharts
- Binary trees
- State machines
- Neural networks
- UML diagrams
- Architecture diagrams
- Other diagram types

The evaluation records:

- First-attempt compilation success.
- Compilation success after automatic repair.
- Number of repair attempts.
- Generated diagram images.

Run the evaluation:

```bash
python evaluate.py
```

Generate the comparison images:

```bash
python compare.py
```

**Note:** Running the evaluation makes multiple IBM watsonx.ai API calls and uses your available API quota.

## Observations and Learnings

During development and testing, the following observations were made:

1. **RAG improves consistency:** Retrieved examples helped produce cleaner spacing and more consistent arrow styles in flowcharts and tree diagrams.
2. **Retrieval is not always beneficial:** A weakly related example sometimes influenced the diagram structure instead of only its visual style.
3. **Compilation does not guarantee correctness:** Some diagrams compiled successfully but still contained missing connections or overlapping nodes.
4. **Prompt quality matters:** Detailed descriptions generally produced better results than vague instructions.
5. **Refinement needs clear instructions:** Follow-up prompts should specify which parts to change and which existing nodes and connections must remain.
6. **Automatic repair is useful:** Sending LaTeX compilation errors back to the model helped correct many syntax-related problems.

## Current Limitations

- The knowledge base currently contains only 14 verified TikZ examples.
- Some diagrams may still fail after three repair attempts.
- Successful compilation does not guarantee a visually or structurally correct diagram.
- Diagram layouts may vary between generations.
- `pgfplots` and `tikz-cd` are currently not supported.
- The sketch-to-diagram feature is experimental and has not yet been tested.
- Docker and IBM Cloud Code Engine deployment configurations are included but have not been tested.

## Future Improvements

- Expand the knowledge base with more verified TikZ examples.
- Introduce a similarity threshold to avoid retrieving weakly related examples.
- Add structural validation to check whether generated nodes and connections match the user's description.
- Improve diagram layout and positioning.
- Add support for `pgfplots` and more diagram types.
- Test and improve the sketch-to-diagram feature.
- Complete Docker and IBM Cloud Code Engine deployment testing.

## Acknowledgements

Special thanks to the following platforms and organizations:

- IBM watsonx.ai and IBM Granite.
- IBM SkillsBuild.
- Edunet Foundation.
- AICTE.
- Streamlit.
- LaTeX and TikZ/PGF.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more information.

---

**Developed as part of an IBM SkillsBuild AI & Cloud Virtual Internship and further extended into a complete AI-powered diagram generation application.**