from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.endpoints import analysis
from app.services.risk_service import risk_service

app = FastAPI(title="Credit Risk RAG System", version="2.0")

# Enable CORS for direct frontend access (bypassing Next.js proxy timeout)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(analysis.router)

@app.on_event("startup")
async def startup_event():
    await risk_service.initialize()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Credit Risk Analyst</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background-color: #f4f4f9; color: #333; }
                .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
                .header { text-align: center; margin-bottom: 30px; }
                h1 { color: #2c3e50; margin-bottom: 5px; }
                .subtitle { color: #7f8c8d; font-size: 0.9em; }
                
                .input-group { display: flex; gap: 10px; justify-content: center; align-items: center; margin-bottom: 20px; }
                input[type="text"] { padding: 12px; border: 1px solid #ddd; border-radius: 6px; width: 200px; font-size: 16px; }
                button { padding: 12px 25px; background: #3498db; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; transition: background 0.3s; }
                button:hover { background: #2980b9; }

                .risk-badge { font-size: 1.5em; font-weight: bold; padding: 10px 20px; border-radius: 50px; display: inline-block; }
                .risk-low { background-color: #e8f8f5; color: #27ae60; border: 2px solid #27ae60; }
                .risk-high { background-color: #fdedec; color: #c0392b; border: 2px solid #c0392b; }

                .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px; }
                .metric-box { background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }
                .metric-label { font-size: 0.85em; color: #7f8c8d; }
                .metric-value { font-size: 1.1em; font-weight: 600; color: #2c3e50; }

                .drivers-list { list-style: none; padding: 0; }
                .driver-item { padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
                .driver-bad { color: #c0392b; font-weight: 500; }
                .driver-good { color: #27ae60; font-weight: 500; }

                #resultArea { display: none; }
                .loading { text-align: center; display: none; margin: 20px; color: #666; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Credit Risk Analyst</h1>
                <div class="subtitle">AI-Powered Financial Health & Default Prediction</div>
            </div>

            <div class="card">
                <div class="input-group">
                    <input type="text" id="ticker" placeholder="Enter Ticker (e.g. AAPL)" value="AAPL" />
                    <button onclick="analyze()">Analyze Risk</button>
                </div>
                <div style="text-align: center;">
                    <label style="color: #666;"><input type="checkbox" id="liveData" checked /> Fetch Live Market Data</label>
                </div>
            </div>

            <div id="loading" class="loading">Analyzing market data & news... (First time analysis may take up to 20s)... please wait...</div>

            <div id="resultArea">
                <!-- Summary Card -->
                <div class="card" style="text-align: center;">
                    <h2 id="companyName">Company Analysis</h2>
                    <div id="riskBadge" class="risk-badge">Analyzing...</div>
                    <p id="riskDesc" style="margin-top: 15px; font-size: 1.1em; line-height: 1.5;"></p>
                </div>

                <!-- Key Drivers Card -->
                <div class="card">
                    <h3>💡 Key Risk Drivers</h3>
                    <p style="color: #666; font-size: 0.9em;">What factors are contributing most to this logic?</p>
                    <ul id="driversList" class="drivers-list"></ul>
                </div>

                <!-- Financial Health Card -->
                <div class="card">
                    <h3>📊 Financial Health</h3>
                    <div class="metric-grid" id="metricsGrid"></div>
                </div>

                <!-- AI Insights Card -->
                <div class="card">
                    <h3>🧠 AI Readings (RAG)</h3>
                    <div id="ragEvidence" style="color: #555; background: #fff; line-height: 1.6; font-style: italic;"></div>
                </div>
            </div>

            <script>
                async function analyze() {
                    const ticker = document.getElementById('ticker').value.toUpperCase();
                    const liveData = document.getElementById('liveData').checked;
                    
                    document.getElementById('loading').style.display = 'block';
                    document.getElementById('resultArea').style.display = 'none';
                    
                    try {
                        // Increase timeout for on-demand downloading (can take 15-20s)
                        const controller = new AbortController();
                        const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 seconds

                        const response = await fetch('/analyze', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ ticker: ticker, use_live_data: liveData }),
                            signal: controller.signal
                        });
                        clearTimeout(timeoutId);
                        const data = await response.json();
                        
                        renderDashboard(data);
                    } catch (e) {
                        alert("Error: " + e.message);
                    } finally {
                        document.getElementById('loading').style.display = 'none';
                    }
                }

                function renderDashboard(data) {
                    document.getElementById('resultArea').style.display = 'block';
                    document.getElementById('companyName').innerText = `Analysis for ${data.ticker}`;

                    // 1. Risk Badge
                    const badge = document.getElementById('riskBadge');
                    const pd = data.probability_of_default;
                    const percent = (pd * 100).toFixed(2);
                    
                    if (pd > 0.5) {
                        badge.className = 'risk-badge risk-high';
                        badge.innerText = `HIGH RISK (${percent}% PD)`;
                        document.getElementById('riskDesc').innerText = `This company shows significant signs of financial distress based on our AI models. Caution is advised.`;
                    } else {
                        badge.className = 'risk-badge risk-low';
                        badge.innerText = `LOW RISK (${percent}% PD)`;
                        document.getElementById('riskDesc').innerText = `This company appears financially stable with healthy indicators.`;
                    }

                    // 2. Key Drivers (SHAP)
                    const driversList = document.getElementById('driversList');
                    driversList.innerHTML = '';
                    const factors = data.risk_factors || {};
                    const sortedFactors = Object.entries(factors).sort((a,b) => Math.abs(b[1]) - Math.abs(a[1]));
                    
                    sortedFactors.slice(0, 4).forEach(([key, val]) => {
                        const li = document.createElement('li');
                        li.className = 'driver-item';
                        
                        // Human readable text
                        let impact = val > 0 ? "Increasing Risk" : "Lowering Risk";
                        let colorClass = val > 0 ? "driver-bad" : "driver-good";
                        let name = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                        
                        // Contextual explanation
                        let reason = "";
                        if (key === 'debt_to_equity' && val > 0) reason = "(High Debt Load)";
                        if (key === 'quick_ratio' && val > 0) reason = "(Liquidity Issues)";
                        if (key === 'sentiment_risk_score' && val > 0) reason = "(Negative News/Filings)";
                        
                        li.innerHTML = `<span><b>${name}</b> <small>${reason}</small></span> <span class="${colorClass}">${impact}</span>`;
                        driversList.appendChild(li);
                    });

                    // 3. Financial Metrics
                    const grid = document.getElementById('metricsGrid');
                    grid.innerHTML = '';
                    const metrics = data.financial_metrics;
                    const displayMetrics = {
                        "debt_to_equity": "Debt/Equity",
                        "current_ratio": "Current Ratio",
                        "return_on_equity": "ROE",
                        "beta": "Volatility (Beta)"
                    };
                    
                    for (const [k, label] of Object.entries(displayMetrics)) {
                        let val = metrics[k];
                        if (typeof val === 'number') val = val.toFixed(2);
                        
                        grid.innerHTML += `
                            <div class="metric-box">
                                <div class="metric-label">${label}</div>
                                <div class="metric-value">${val || 'N/A'}</div>
                            </div>
                        `;
                    }

                    // 4. RAG Evidence
                    const evidences = data.rag_evidences || [];
                    document.getElementById('ragEvidence').innerHTML = evidences.length > 0 ?
                        evidences.map(e => `<p>related excerpt: "${e.substring(0, 150)}..."</p>`).join('') :
                        "No specific textual risk factors found in recent filings.";
                }
            </script>
        </body>
    </html>
    """
