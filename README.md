# Goldman Sachs AI Financial Research System

AI-powered multi-model equity research pipeline for NVIDIA Corporation (NVDA)

Built with Python + Groq LLaMA + yFinance.

---

## Goldman Sachs Financial Models

| Model | Purpose |
|---|---|
| DCF | Discounted Cash Flow -- intrinsic value |
| LBO | Leveraged Buyout -- 5-year IRR |
| Comps | Trading Comparables -- peer multiples |
| M&A | Accretion/Dilution -- EPS impact |
| Monte Carlo | 10,000 GBM price simulations |

---

## Sample Output -- NVDA

| Metric | Value |
|---|---|
| Current Price | $172.7 |
| DCF Value | $80.92 |
| LBO IRR | 50.8% |
| Comps Implied | $137.25 |
| MC P50 Median | $252.83 |
| Price Target | $153.74 |
| Recommendation | SELL |
| Conviction | Medium |

---

## Tech Stack

- LLM: Groq API (llama-3.1-8b-instant)
- Financial data: yFinance (live)
- Sentiment NLP: VADER
- Web search: Serper API
- PDF export: fpdf2 + Liberation Sans
- Excel export: openpyxl
- Simulation: NumPy GBM
- Platform: Google Colab T4 GPU

---

## How to Run

### Prerequisites
```
GROQ_API_KEY   -- free at console.groq.com
SERPER_API_KEY -- free at serper.dev
```

### Steps
1. Open notebook/gs_financial_research.ipynb in Google Colab
2. Set Runtime to T4 GPU
3. Paste API keys in Cell 2
4. Run Cells 1 to 16 in order

---

## Project Structure

```
gs-financial-research-ai/
ss-- README.md
ss-- requirements.txt
ss-- .gitignore
ss-- src/
    ss-- data_tools.py
    ss-- groq_caller.py
    ss-- gs_models.py
    ss-- valuation_bridge.py
    ss-- pdf_exporter.py
ss-- outputs/
    ss-- dataset.xlsx
```

---

## Disclaimer

Educational purposes only. Not affiliated with Goldman Sachs Group Inc.
Not investment advice. AI-generated research using public data.

---

Generated: March 22, 2026
Model: groq/llama-3.1-8b-instant