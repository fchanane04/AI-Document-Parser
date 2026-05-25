# Document Extractor

A standalone AI-powered tool that extracts customer data from business documents (CSV, Excel, PDF) and converts it into structured JSON.

Built as a companion tool for the [SaaS Metrics Dashboard](https://github.com/fchanane04/saas-metrics-dashboard) project.

---

## What It Does

Business owners store customer data in different formats — spreadsheets, invoices, contracts. This tool reads those files and automatically extracts customer information using AI, ready to be imported into the SaaS Metrics Dashboard.

---

## How It Works

Upload a file (CSV, Excel, PDF)
↓
Tool detects the file type
↓
Extracts raw content
↓
AI understands and structures the data
↓
Returns clean JSON with customer fields

---

## Tech Stack

- **LangChain** — AI orchestration framework
- **Groq + LLaMA 3.3** — Fast, free LLM for development
- **pandas** — CSV and Excel processing
- **pdfplumber** — PDF text extraction
- **Python** — Core language

---

## Supported File Types

| Format | Method | AI Needed |
|--------|--------|-----------|
| CSV    | pandas | No |
| Excel  | pandas | No |
| PDF    | pdfplumber + LangChain | Yes |

---
