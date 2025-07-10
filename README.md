# AI-Powered Diagram Generator

This is a simple Streamlit app that lets you generate **Mermaid.js diagrams** from natural language using a local LLM via [Ollama](https://ollama.com).

## Features
- Generate **Flowcharts**, **Sequence**, and **Class Diagrams**
- Powered by **LLaMA3** (or any Ollama-supported model)
- Choose from multiple **Mermaid themes**
- Export diagrams as **SVG** or **PNG**
- Fully **offline** and **private**

## Known Issues
The app relies on the LLM to generate syntactically correct Mermaid code. Occasionally, the model may return invalid syntax, especially for complex or ambiguous prompts. If the diagram doesn't render, try simplifying or rephrasing your input.

For some diagram types like Flowchart, the PNG export may fail due to how Mermaid renders certain SVG layouts. If that happens, try using the SVG export instead, which is more reliable across all themes.
