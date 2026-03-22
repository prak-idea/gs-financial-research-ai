"""
Goldman Sachs Financial Models
1. DCF  -- Discounted Cash Flow
2. LBO  -- Leveraged Buyout
3. Comps -- Trading Comparables
4. M&A  -- Accretion/Dilution
5. Monte Carlo -- GBM Simulation
"""
import numpy as np
import yfinance as yf


def run_dcf(free_cash_flow, total_debt, total_cash,
            shares_out, beta, revenue_growth, market_cap):
    risk_free = 0.043
    erp = 0.055
    coe = risk_free + beta * erp
    cod = 0.05
    tax = 0.21
    dr  = total_debt / (market_cap + total_debt) if (market_cap + total_debt) > 0 else 0.1
    wacc = coe * (1 - dr) + cod * (1 - tax) * dr
    tg   = 0.025
    rates = [revenue_growth * f for f in [1.1, 1.0, 0.85, 0.70, 0.55]]
    rates = [max(-0.1, min(0.5, g)) for g in rates]
    projs = []
    fcf = free_cash_flow
    for i, g in enumerate(rates):
        fcf = fcf * (1 + g)
        pv  = fcf / ((1 + wacc) ** (i + 1))
        projs.append({"year": i+1, "fcf_B": round(fcf/1e9,2), "pv_B": round(pv/1e9,2)})
    tv  = projs[-1]["fcf_B"] * 1e9 * (1 + tg) / (wacc - tg)
    pvt = tv / ((1 + wacc) ** 5)
    eq  = sum(p["pv_B"] for p in projs)*1e9 + pvt + total_cash - total_debt
    return {"dcf_price": round(eq / shares_out, 2), "wacc_pct": round(wacc*100,2)}


def run_monte_carlo(ticker, current_price, n_sim=10000, n_days=252):
    import numpy as np
    np.random.seed(42)
    hist  = yf.Ticker(ticker).history(period="1y")
    ret   = hist["Close"].pct_change().dropna()
    mu, sigma = float(ret.mean()), float(ret.std())
    Z     = np.random.standard_normal((n_sim, n_days))
    paths = current_price * np.exp(np.cumsum((mu - 0.5*sigma**2) + sigma*Z, axis=1))
    fins  = paths[:, -1]
    return {
        "p5":  round(float(np.percentile(fins, 5)), 2),
        "p50": round(float(np.median(fins)), 2),
        "p95": round(float(np.percentile(fins, 95)), 2),
        "prob_up": round(float(np.mean(fins > current_price)*100), 1),
        "var_95": round(current_price - float(np.percentile(fins, 5)), 2),
        "ann_vol": round(sigma * np.sqrt(252) * 100, 1),
    }