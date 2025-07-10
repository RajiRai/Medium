import streamlit as st
import requests

# Ollama/LLM configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# Prompt templates for different diagram types
TEMPLATES = {
    "Flowchart": """
Convert the following description into a valid Mermaid flowchart.
Use 'graph LR' for left-to-right. Use edge labels as needed: A --|label|--> B.
Each node should be X[Label]. Only output code. No explanations, no backticks.

Description:
{description}
""",
    "Sequence Diagram": """
Convert the following description into a valid Mermaid sequence diagram.
Begin with:
sequenceDiagram
participant Alice
participant Bob
Alice->>Bob: Hello
Only output code. No explanations, no backticks.

Description:
{description}
""",
    "Class Diagram": """
Convert the following description into a valid Mermaid class diagram.
Begin with:
classDiagram
class Animal{{
  +String name
  +move()
}}
Only output code. No explanations, no backticks.

Description:
{description}
"""
}

def generate_mermaid(prompt):
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=data)
    r.raise_for_status()
    return r.json()["response"]

def extract_mermaid_code(response):
    import re
    blocks = re.findall(r'```(?:mermaid)?(.*?)```', response, re.DOTALL)
    if blocks:
        return blocks[0].strip()
    return response.strip()

st.title("AI Diagram Generator")

# Diagram type selector
diagram_type = st.selectbox(
    "Diagram type:",
    list(TEMPLATES.keys()),
    index=0
)

default_descriptions = {
    "Flowchart": "A developer pushes code. CI server runs tests. If tests pass, create build artifact and deploy to staging. If staging passes, deploy to production.",
    "Sequence Diagram": "A user logs in. The app checks credentials with the database. If valid, the app returns a welcome message.",
    "Class Diagram": "A Vehicle has a start() method. Car and Bike inherit from Vehicle. Car has a drive() method. Bike has a pedal() method."
}

description = st.text_area(
    "Describe your process or structure:",
    value=default_descriptions[diagram_type],
    height=150
)

theme_choice = st.selectbox("Diagram Theme:", ["default", "dark", "forest", "neutral"], index=0)

if st.button("Generate Diagram"):
    prompt = TEMPLATES[diagram_type].format(description=description)
    with st.spinner("Generating diagram..."):
        llm_response = generate_mermaid(prompt)
        mermaid_code = extract_mermaid_code(llm_response)
        mermaid_code = mermaid_code.strip()

    st.subheader("Rendered Diagram:")
    st.components.v1.html(f"""
        <div class="mermaid">
        {mermaid_code}
        </div>
        <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{startOnLoad:true, theme: '{theme_choice}'}});
        </script>
        <div>
          <button id="dl-svg" style="padding:8px 16px;font-size:1em;margin:10px 6px;">Export SVG</button>
          <button id="dl-png" style="padding:8px 16px;font-size:1em;margin:10px 6px;">Export PNG</button>
        </div>
        <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{startOnLoad:true, theme: '{theme_choice}'}});
        function download(filename, dataUrl) {{
           var a = document.createElement("a");
           a.href = dataUrl;
           a.download = filename;
           document.body.appendChild(a);
           a.click();
           document.body.removeChild(a);
        }}
        document.getElementById("dl-svg").onclick = function() {{
           let svg = document.querySelector(".mermaid svg");
           if(svg) {{
              let blob = new Blob([svg.outerHTML], {{type: "image/svg+xml"}});
              let url = URL.createObjectURL(blob);
              download("diagram.svg", url);
              setTimeout(()=>URL.revokeObjectURL(url), 5000);
           }}
        }}
        document.getElementById("dl-png").onclick = function() {{
           let svg = document.querySelector(".mermaid svg");
           if(svg) {{
             let image = new Image();
             let svgData = new XMLSerializer().serializeToString(svg);
             let svgBlob = new Blob([svgData], {{type: "image/svg+xml;charset=utf-8"}});
             let url = URL.createObjectURL(svgBlob);
             image.onload = function() {{
                let canvas = document.createElement('canvas');
                canvas.width = image.width * 2;
                canvas.height = image.height * 2;
                let ctx = canvas.getContext("2d");
                ctx.fillStyle = "#fff";
                ctx.fillRect(0,0,canvas.width,canvas.height);
                ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
                let pngFile = canvas.toDataURL("image/png");
                download("diagram.png", pngFile);
                setTimeout(()=>URL.revokeObjectURL(url), 5000);
             }}
             image.src = url;
           }}
        }}
        </script>
        """, height=700)
