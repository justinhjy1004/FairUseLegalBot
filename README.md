# Copyright Fair Use Legal Bot

This module implements a prototype Retrieval-Augmented Generation (RAG) system customized for legal analysis under the **Fair Use Doctrine** in U.S. copyright law. It supports granular legal reasoning by integrating semantic search with citation networks, court hierarchy, and structured factor-based analysis.

Developed for the paper [_Incorporating Legal Structure in Retrieval-Augmented Generation: A Case Study on Copyright Fair Use_](TODO ), this tool aims to improve the retrieval and evaluation of case law for use in real-world copyright disputes.

---

##  Folder Structure Overview

1. **Main Prototype (RetrievalTesting/)**: Core Streamlit app, legal retrieval, LLM evaluation, and citation logic.

1. **Analysis Tools (RetrievalTesting/Analysis/)**: Scripts and plots comparing standard vs. structured RAG performance.

1. **LaTeX Source (ConferencePaper/)**: Paper text and figures for the ASAIL 2025 submission.

1. **Graph Construction (BuildingDB/)**: Scripts to process legal cases and construct the Neo4j knowledge graph.

---

##  Key Features

- **Hybrid RAG Retrieval**: Combines text embeddings with PageRank citation scores and court hierarchy.
- **Interactive Tuning**: Users can control the weighting of semantic similarity, citation authority, and court prestige.
- **Four-Factor Legal Evaluation**: Breaks down retrieved cases and disputes into structured Chain-of-Thought reasoning under the four Fair Use factors.
- **LLM Integration**: Uses Google Gemini for embeddings and LLM-based reasoning.
- **Cited Case Expansion**: Automatically retrieves influential precedents cited by top cases.
- **Streamlit Interface**: Clean, interactive UI for dispute input, analysis, and downloading results.

## Running the App

### 1. **Install Dependencies**

```bash
pip install streamlit polars neo4j PyMuPDF langchain-google-genai
```

### 2. **Set Required Environment Variables**

You’ll need access to:

* A Neo4j AuraDB instance
* Google Gemini API

Set these environment variables (e.g., in `.env` or shell):

```bash
AURA_URI=bolt://...
AURA_user=...
AURA_password=...
GEMINI_API=...
```

### 3. **Start the Streamlit App**

```bash
cd RetrievalTesting
streamlit run RAG_Streamlit.py
```

---

## Notes

* **Neo4j DB Required**: This repository does not include the graph database dump. If you'd like to use the full retrieval system with case law and citation data, please contact the project authors to request access.
* The current prototype is designed for internal evaluation and academic demonstration. Production-grade legal use would require rigorous validation and safeguards.

---

## Related Links

* [Paper (PDF)](./main.pdf)
* [Live App Demo](https://fairuselegalbot-main.streamlit.app)
* [GitHub Project](https://github.com/justinhjy1004/FairUseLegalBot)