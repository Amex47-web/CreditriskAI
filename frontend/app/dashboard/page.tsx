"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import {
    Search,
    TrendingUp,
    AlertTriangle,
    CheckCircle,
    DollarSign,
    Activity,
    FileText,
    Loader2,
    LogOut
} from "lucide-react";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Cell
} from 'recharts';

// Types matching the backend response
interface FinancialMetrics {
    debt_to_equity: number;
    quick_ratio: number;
    current_ratio: number;
    return_on_equity: number;
    beta: number;
    [key: string]: number;
}

interface AnalysisResponse {
    ticker: string;
    probability_of_default: number;
    risk_level: string;
    financial_metrics: FinancialMetrics;
    rag_evidences: string[];
    risk_factors: { [key: string]: number };
}

export default function Dashboard() {
    const router = useRouter();
    const { user, loading: authLoading, logout } = useAuth();
    const [ticker, setTicker] = useState("AAPL");
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState<AnalysisResponse | null>(null);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!authLoading && !user) {
            router.push("/login");
        }
    }, [user, authLoading, router]);

    const handleLogout = async () => {
        await logout();
    };

    const analyze = async () => {
        setLoading(true);
        setError("");
        setData(null);

        try {
            console.log(`Analyzing ${ticker}... calling backend directly...`);
            // Use direct backend URL to bypass Next.js proxy timeout
            const res = await fetch("http://127.0.0.1:8000/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ticker, use_live_data: true }),
            });

            if (!res.ok) {
                const errorText = await res.text();
                console.error("Backend Error:", res.status, errorText);
                throw new Error(`Analysis failed: ${res.status} ${res.statusText}`);
            }

            const result = await res.json();
            setData(result);
        } catch (err: any) {
            console.error("Fetch Error:", err);
            setError(err.message || "Something went wrong. Ensure backend is running on port 8000.");
        } finally {
            setLoading(false);
        }
    };

    // Prepare data for the Drivers Chart
    const driverData = data
        ? Object.entries(data.risk_factors || {})
            .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
            .slice(0, 5)
            .map(([key, value]) => ({
                name: key.replace(/_/g, " "),
                value: value,
                impact: value > 0 ? "Increasing Risk" : "Decreasing Risk"
            }))
        : [];

    if (authLoading || !user) {
        return <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950"><Loader2 className="animate-spin h-8 w-8 text-blue-600" /></div>;
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 font-sans pb-20 transition-colors duration-300">
            {/* Header */}
            <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-10 transition-colors duration-300">
                <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Activity className="text-blue-600 dark:text-blue-500 w-6 h-6" />
                        <h1 className="text-xl font-bold text-gray-800 dark:text-white">Credit Risk Analyst</h1>
                    </div>
                    <div className="flex items-center gap-4">
                        <span className="text-sm text-gray-500 dark:text-gray-400 hidden md:inline">AI-Powered Default Prediction</span>
                        <button onClick={handleLogout} className="flex items-center gap-1 text-sm text-gray-600 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 transition">
                            <LogOut className="w-4 h-4" /> Logout
                        </button>
                    </div>
                </div>
            </header>

            <main className="max-w-6xl mx-auto px-6 py-10">
                {/* Search Area */}
                <div className="flex flex-col items-center justify-center mb-12">
                    <div className="flex w-full max-w-md gap-2">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-3 text-gray-400 dark:text-gray-500 w-5 h-5" />
                            <input
                                type="text"
                                placeholder="Enter Ticker (e.g., AAPL, TSLA)"
                                className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
                                value={ticker}
                                onChange={(e) => setTicker(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && analyze()}
                            />
                        </div>
                        <button
                            onClick={analyze}
                            disabled={loading}
                            className="bg-blue-600 dark:bg-blue-600 hover:bg-blue-700 dark:hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition flex items-center gap-2 disabled:opacity-70 shadow-sm"
                        >
                            {loading ? <Loader2 className="animate-spin w-5 h-5" /> : "Analyze"}
                        </button>
                    </div>
                    {error && <p className="text-red-500 dark:text-red-400 mt-4 text-sm bg-red-50 dark:bg-red-900/20 px-4 py-2 rounded-md border border-red-100 dark:border-red-900/30">{error}</p>}
                    {loading && <p className="text-blue-500 mt-2 text-sm text-center">First-time analysis for a new company may take up to 20-30 seconds to download filings.</p>}
                </div>

                {data && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        {/* Risk Score Card */}
                        <div className="bg-white dark:bg-gray-900 p-8 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 md:col-span-2 flex flex-col md:flex-row items-center justify-between gap-8 transition-colors duration-300">
                            <div className="flex-1">
                                <h2 className="text-lg font-medium text-gray-500 dark:text-gray-400 mb-1">Risk Assessment</h2>
                                <div className="flex items-center gap-4">
                                    <div
                                        className={`text-4xl font-bold px-6 py-2 rounded-full border-2 ${data.risk_level === "High"
                                            ? "bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 border-red-200 dark:border-red-900/30"
                                            : "bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 border-green-200 dark:border-green-900/30"
                                            }`}
                                    >
                                        {data.risk_level} Risk
                                    </div>
                                    <div className="text-gray-400 dark:text-gray-500 font-mono text-sm">
                                        PD: {(data.probability_of_default * 100).toFixed(4)}%
                                    </div>
                                </div>
                                <p className="mt-4 text-gray-600 dark:text-gray-300 max-w-xl leading-relaxed">
                                    {data.risk_level === "High"
                                        ? "Our models detect significant financial distress signals. Caution is advised for credit exposure."
                                        : "The company demonstrates strong financial health with stable indicators and positive market sentiment."}
                                </p>
                            </div>

                            {/* Simple Visual Gauge Mockup */}
                            <div className="w-full md:w-1/3 h-4 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden relative">
                                <div
                                    className={`h-full transition-all duration-1000 ${data.risk_level === "High" ? "bg-red-500" : "bg-green-500"}`}
                                    style={{ width: `${Math.max(10, data.probability_of_default * 100)}%` }}
                                />
                            </div>
                        </div>

                        {/* Key Drivers Chart */}
                        <div className="bg-white dark:bg-gray-900 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 transition-colors duration-300">
                            <div className="flex items-center gap-2 mb-6">
                                <TrendingUp className="text-gray-400 dark:text-gray-500 w-5 h-5" />
                                <h3 className="font-semibold text-gray-800 dark:text-white">Top Risk Drivers (SHAP)</h3>
                            </div>
                            <div className="h-64">
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={driverData} layout="vertical" margin={{ left: 0 }}>
                                        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="var(--color-grid)" className="dark:opacity-20" />
                                        <XAxis type="number" hide />
                                        <YAxis
                                            dataKey="name"
                                            type="category"
                                            width={100}
                                            tick={{ fontSize: 12, fill: '#6B7280' }}
                                        />
                                        <Tooltip
                                            cursor={{ fill: 'transparent' }}
                                            contentStyle={{
                                                borderRadius: '8px',
                                                border: 'none',
                                                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                                                backgroundColor: 'var(--tooltip-bg)',
                                                color: 'var(--tooltip-text)'
                                            }}
                                            itemStyle={{ color: 'var(--tooltip-text)' }}
                                            wrapperClassName="dark:!bg-gray-800 dark:!text-white dark:ring-1 dark:ring-gray-700"
                                        />
                                        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                                            {driverData.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={entry.value > 0 ? "#EF4444" : "#10B981"} />
                                            ))}
                                        </Bar>
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* Financial Metrics */}
                        <div className="bg-white dark:bg-gray-900 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 transition-colors duration-300">
                            <div className="flex items-center gap-2 mb-6">
                                <DollarSign className="text-gray-400 dark:text-gray-500 w-5 h-5" />
                                <h3 className="font-semibold text-gray-800 dark:text-white">Financial Health</h3>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                {Object.entries(data.financial_metrics || {})
                                    .filter(([key]) => key !== 'ticker')
                                    .slice(0, 6)
                                    .map(([key, val]) => (
                                        <div key={key} className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg transition-colors duration-300">
                                            <div className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">
                                                {key.replace(/_/g, " ")}
                                            </div>
                                            <div className="text-lg font-semibold text-gray-900 dark:text-white">
                                                {typeof val === 'number' ? val.toFixed(2) : val}
                                            </div>
                                        </div>
                                    ))}
                            </div>
                        </div>

                        {/* AI Analysis / RAG */}
                        <div className="bg-white dark:bg-gray-900 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 md:col-span-2 transition-colors duration-300">
                            <div className="flex items-center gap-2 mb-4">
                                <FileText className="text-gray-400 dark:text-gray-500 w-5 h-5" />
                                <h3 className="font-semibold text-gray-800 dark:text-white">AI Analysis & Evidence</h3>
                            </div>
                            <div className="space-y-4">
                                {(data.rag_evidences && data.rag_evidences.length > 0) ? (
                                    data.rag_evidences.map((text, i) => (
                                        <div key={i} className="flex gap-4 p-4 bg-blue-50/50 dark:bg-blue-900/20 rounded-lg border border-blue-100 dark:border-blue-900/30 hover:bg-blue-50 dark:hover:bg-blue-900/30 transition">
                                            <CheckCircle className="text-blue-500 dark:text-blue-400 w-5 h-5 flex-shrink-0 mt-1" />
                                            <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed italic">
                                                "...{text}"
                                            </p>
                                        </div>
                                    ))
                                ) : (
                                    <p className="text-gray-500 dark:text-gray-400 italic">No specific filings found to cite.</p>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}
