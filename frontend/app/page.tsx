"use client";

import Link from "next/link";
import {
  Activity,
  ShieldCheck,
  BarChart3,
  BrainCircuit,
  ArrowRight,
  CheckCircle,
  Check,
  Search,
  TrendingUp,
  FileText
} from "lucide-react";
import { motion } from "framer-motion";
import { ThemeToggle } from "@/components/theme-toggle";

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2
    }
  }
};

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-950 overflow-hidden transition-colors duration-300">
      {/* Navigation */}
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ type: "spring", stiffness: 100 }}
        className="fixed w-full bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-100 dark:border-gray-800 z-50 transition-colors duration-300"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <div className="bg-blue-600 p-1.5 rounded-lg">
                <Activity className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white tracking-tight">CreditRisk.AI</span>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition font-medium">Features</a>
              <a href="#demo" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition font-medium">Live Demo</a>
              <a href="#about" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition font-medium">How it works</a>
              <a href="#pricing" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition font-medium">Pricing</a>
            </div>
            <div className="flex items-center gap-4">
              <ThemeToggle />
              <Link href="/login" className="text-gray-900 dark:text-white font-medium hover:text-blue-600 dark:hover:text-blue-400 transition">
                Log in
              </Link>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Link
                  href="/login"
                  className="bg-gray-900 dark:bg-white text-white dark:text-gray-900 px-5 py-2.5 rounded-lg font-medium hover:bg-gray-800 dark:hover:bg-gray-100 transition shadow-lg shadow-gray-200 dark:shadow-none block"
                >
                  Get Started
                </Link>
              </motion.div>
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <motion.div
            initial="hidden"
            animate="visible"
            variants={staggerContainer}
            className="text-center max-w-4xl mx-auto"
          >
            <motion.div variants={fadeInUp} className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-sm font-medium mb-8 border border-blue-100 dark:border-blue-800">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500 dark:bg-blue-400"></span>
              </span>
              v2.0 is now live with Advanced RAG Support
            </motion.div>

            <motion.h1 variants={fadeInUp} className="text-5xl md:text-7xl font-extrabold text-gray-900 dark:text-white tracking-tight mb-8 leading-tight">
              Master Credit Risk with <br className="hidden md:block" />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400">AI-Powered Precision</span>
            </motion.h1>

            <motion.p variants={fadeInUp} className="text-xl text-gray-600 dark:text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed">
              Analyze corporate financial health in seconds. Combine quantitative metrics with qualitative insights using our advanced RAG engine.
            </motion.p>

            <motion.div variants={fadeInUp} className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Link
                  href="/login"
                  className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-blue-600 rounded-xl hover:bg-blue-700 transition shadow-xl shadow-blue-200/50 dark:shadow-blue-900/20 group"
                >
                  Start Analyzing Now
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Link>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <a
                  href="#demo"
                  className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 border-2 border-gray-100 dark:border-gray-700 rounded-xl hover:border-gray-300 dark:hover:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-750 transition"
                >
                  View Live Demo
                </a>
              </motion.div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-24 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeInUp}
            className="text-center mb-16"
          >
            <h2 className="text-base text-blue-600 dark:text-blue-400 font-semibold tracking-wide uppercase">Core Capabilities</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              Everything you need for credit assessment
            </p>
          </motion.div>

          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={staggerContainer}
            className="grid grid-cols-1 md:grid-cols-3 gap-12"
          >
            {[
              {
                icon: <BrainCircuit className="h-8 w-8 text-white" />,
                title: "RAG Intelligence",
                desc: "Retrieves and synthesizes data from 10-K filings and news to provide context implementation to the numbers.",
                color: "bg-indigo-600"
              },
              {
                icon: <ShieldCheck className="h-8 w-8 text-white" />,
                title: "Default Prediction",
                desc: "Proprietary ML models trained on historical default data to estimate Probability of Default (PD) with high accuracy.",
                color: "bg-emerald-500"
              },
              {
                icon: <BarChart3 className="h-8 w-8 text-white" />,
                title: "SHAP Explainability",
                desc: "Transparent AI. Understand exactly which factors—debt load, liquidity, or sentiment—drove the risk score.",
                color: "bg-blue-500"
              }
            ].map((feature, i) => (
              <motion.div
                key={i}
                variants={fadeInUp}
                whileHover={{ y: -10, transition: { duration: 0.3 } }}
                className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-xl transition-all duration-300"
              >
                <div className={`h-14 w-14 rounded-xl flex items-center justify-center mb-6 shadow-lg shadow-gray-200 dark:shadow-none ${feature.color}`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">{feature.title}</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  {feature.desc}
                </p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Interactive Demo Preview */}
      <section id="demo" className="py-24 bg-white dark:bg-gray-950 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeInUp}
            className="text-center mb-16"
          >
            <h2 className="text-base text-blue-600 dark:text-blue-400 font-semibold tracking-wide uppercase">Live Demo</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              See the platform in action
            </p>
            <p className="mt-4 text-xl text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
              Experience the power of our analysis engine. This is a preview of the dashboard you'll access after logging in.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="relative rounded-2xl bg-gray-900 p-2 sm:p-4 shadow-2xl ring-1 ring-gray-900/10"
          >
            <div className="absolute top-0 left-1/2 -ml-[40rem] -mt-[30rem] w-[80rem] h-[60rem] rounded-full bg-blue-600/20 blur-3xl opacity-20 pointer-events-none"></div>

            <div className="relative rounded-xl bg-gray-50 overflow-hidden border border-gray-200">
              {/* Mock Browser Header */}
              <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-2">
                <div className="flex gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-red-400"></div>
                  <div className="w-3 h-3 rounded-full bg-amber-400"></div>
                  <div className="w-3 h-3 rounded-full bg-green-400"></div>
                </div>
                <div className="flex-1 text-center text-xs text-gray-400 font-mono">dashboard.creditrisk.ai/analyze/AAPL</div>
              </div>

              {/* Mock Dashboard Content */}
              <div className="p-6 md:p-10 pointer-events-none select-none opacity-90 grayscale-[10%] hover:grayscale-0 transition duration-700">
                <div className="flex justify-between items-start mb-8">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-800">Apple Inc. (AAPL)</h3>
                    <p className="text-gray-500">NasdaqGS - Real Time Price • USD</p>
                  </div>
                  <div className="bg-green-50 text-green-700 border border-green-200 px-4 py-2 rounded-full font-bold">
                    LOW RISK (0.42%)
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  {/* Mock Graph */}
                  <div className="bg-white p-5 rounded-lg border border-gray-100 shadow-sm md:col-span-2">
                    <div className="flex items-center gap-2 mb-4">
                      <TrendingUp className="w-4 h-4 text-gray-400" />
                      <span className="font-semibold text-gray-700">Risk Factor Contribution</span>
                    </div>
                    <div className="h-48 flex items-end justify-between gap-2 px-4">
                      {[60, 45, 30, 20, 10, -15, -30].map((h, i) => (
                        <div key={i} className={`w-full rounded-t-sm ${h > 0 ? 'bg-red-400' : 'bg-green-400'}`} style={{ height: `${Math.abs(h)}%` }}></div>
                      ))}
                    </div>
                  </div>

                  {/* Mock Metrics */}
                  <div className="bg-white p-5 rounded-lg border border-gray-100 shadow-sm space-y-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Activity className="w-4 h-4 text-gray-400" />
                      <span className="font-semibold text-gray-700">Key Metrics</span>
                    </div>
                    {[
                      { l: "Debt to Equity", v: "1.45" },
                      { l: "Current Ratio", v: "0.94" },
                      { l: "ROE", v: "28.5%" },
                      { l: "Altman Z", v: "4.2" }
                    ].map((m, i) => (
                      <div key={i} className="flex justify-between text-sm">
                        <span className="text-gray-500">{m.l}</span>
                        <span className="font-mono font-medium">{m.v}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-100 p-5 rounded-lg flex gap-4">
                  <FileText className="w-5 h-5 text-blue-600 flex-shrink-0" />
                  <div className="space-y-2">
                    <div className="h-2 bg-blue-200 rounded w-3/4"></div>
                    <div className="h-2 bg-blue-200 rounded w-full"></div>
                    <div className="h-2 bg-blue-200 rounded w-5/6"></div>
                  </div>
                </div>
              </div>

              {/* Overlay CTA */}
              <div className="absolute inset-0 flex items-center justify-center bg-white/30 backdrop-blur-[2px]">
                <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }}>
                  <Link href="/login" className="bg-blue-600 text-white px-8 py-4 rounded-xl font-bold text-lg shadow-xl hover:bg-blue-700 transition">
                    Try Interactive Demo
                  </Link>
                </motion.div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* How it Works */}
      <section id="about" className="py-24 bg-gray-50 dark:bg-gray-900 border-y border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeInUp}
            className="text-center mb-16"
          >
            <h2 className="text-base text-blue-600 dark:text-blue-400 font-semibold tracking-wide uppercase">Workflow</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              From Ticker to Insight in Seconds
            </p>
          </motion.div>

          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={staggerContainer}
            className="grid md:grid-cols-3 gap-8"
          >
            {[
              {
                title: "1. Enter Stock Ticker",
                desc: "Input any US publicly traded company symbol (e.g., TSLA, NVDA). We fetch live market data immediately.",
                icon: <Search className="w-6 h-6 text-white" />
              },
              {
                title: "2. AI Processing",
                desc: "Our engine retrieves 10-K filings, digests financial statements, and runs cross-encoder RAG models.",
                icon: <BrainCircuit className="w-6 h-6 text-white" />
              },
              {
                title: "3. Actionable Risk Score",
                desc: "Receive a comprehensive risk profile, default probability, and cited evidence for your report.",
                icon: <CheckCircle className="w-6 h-6 text-white" />
              }
            ].map((step, i) => (
              <motion.div
                key={i}
                variants={fadeInUp}
                className="relative bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700"
              >
                <div className="absolute -top-6 left-8 bg-gray-900 dark:bg-blue-600 p-3 rounded-xl shadow-lg">
                  {step.icon}
                </div>
                <h3 className="mt-8 text-xl font-bold text-gray-900 dark:text-white mb-4">{step.title}</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{step.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-24 bg-white dark:bg-gray-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeInUp}
            className="text-center mb-16"
          >
            <h2 className="text-base text-blue-600 dark:text-blue-400 font-semibold tracking-wide uppercase">Pricing</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              Plans for every scale
            </p>
          </motion.div>

          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={staggerContainer}
            className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto"
          >
            {/* Starter */}
            <motion.div
              variants={fadeInUp}
              whileHover={{ y: -5 }}
              className="bg-white dark:bg-gray-800 rounded-2xl p-8 border border-gray-200 dark:border-gray-700 hover:border-blue-200 dark:hover:border-blue-500 transition relative"
            >
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Starter</h3>
              <div className="my-4 flex items-baseline">
                <span className="text-4xl font-extrabold text-gray-900 dark:text-white">$0</span>
                <span className="ml-1 text-gray-500 dark:text-gray-400">/mo</span>
              </div>
              <p className="text-gray-500 dark:text-gray-400 mb-6">Perfect for individual analysts trying out the platform.</p>
              <ul className="space-y-4 mb-8">
                {["5 Lookups / Day", "Basic Financial Metrics", "Standard RAG Usage", "Community Support"].map((f, i) => (
                  <li key={i} className="flex items-center text-gray-600 dark:text-gray-300">
                    <Check className="w-5 h-5 text-green-500 mr-2" /> {f}
                  </li>
                ))}
              </ul>
              <Link href="/login" className="block w-full text-center py-3 px-4 border border-blue-600 text-blue-600 dark:text-blue-400 dark:border-blue-400 rounded-lg font-medium hover:bg-blue-50 dark:hover:bg-blue-900/20 transition">
                Start for Free
              </Link>
            </motion.div>

            {/* Pro */}
            <motion.div
              variants={fadeInUp}
              whileHover={{ y: -5 }}
              className="bg-gray-900 dark:bg-blue-900 rounded-2xl p-8 border border-gray-900 dark:border-blue-800 text-white shadow-xl transform md:-translate-y-4 relative"
            >
              <div className="absolute top-0 right-0 bg-blue-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg rounded-tr-lg">POPULAR</div>
              <h3 className="text-lg font-medium text-white">Pro Analyst</h3>
              <div className="my-4 flex items-baseline">
                <span className="text-4xl font-extrabold text-white">$49</span>
                <span className="ml-1 text-gray-400 dark:text-blue-200">/mo</span>
              </div>
              <p className="text-gray-300 dark:text-blue-100 mb-6">For professional credit risk assessment and deep dives.</p>
              <ul className="space-y-4 mb-8">
                {["Unlimited Lookups", "Advanced SHAP Explanations", "Full 10-K RAG Access", "Export to PDF", "Priority Support"].map((f, i) => (
                  <li key={i} className="flex items-center text-gray-300 dark:text-blue-100">
                    <Check className="w-5 h-5 text-blue-400 mr-2" /> {f}
                  </li>
                ))}
              </ul>
              <Link href="/login" className="block w-full text-center py-3 px-4 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition">
                Get Pro Access
              </Link>
            </motion.div>

            {/* Enterprise */}
            <motion.div
              variants={fadeInUp}
              whileHover={{ y: -5 }}
              className="bg-white dark:bg-gray-800 rounded-2xl p-8 border border-gray-200 dark:border-gray-700 hover:border-blue-200 dark:hover:border-blue-500 transition"
            >
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Enterprise</h3>
              <div className="my-4 flex items-baseline">
                <span className="text-4xl font-extrabold text-gray-900 dark:text-white">Custom</span>
              </div>
              <p className="text-gray-500 dark:text-gray-400 mb-6">For banks and institutions requiring API access and SLAs.</p>
              <ul className="space-y-4 mb-8">
                {["API Access", "Custom Model Fine-tuning", "On-Prem Deployment", "SSO Integration", "Dedicated Account Manager"].map((f, i) => (
                  <li key={i} className="flex items-center text-gray-600 dark:text-gray-300">
                    <Check className="w-5 h-5 text-green-500 mr-2" /> {f}
                  </li>
                ))}
              </ul>
              <Link href="/login" className="block w-full text-center py-3 px-4 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg font-medium hover:bg-gray-50 dark:hover:bg-gray-750 transition">
                Contact Sales
              </Link>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-24 bg-gray-900 overflow-hidden">
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center z-10">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeInUp}
          >
            <h2 className="text-3xl font-extrabold text-white sm:text-4xl mb-8">
              Ready to upgrade your risk analysis?
            </h2>
            <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
              Join top financial institutions using CreditRisk.AI to make faster, smarter lending decisions.
            </p>
            <div className="flex justify-center gap-4">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Link
                  href="/login"
                  className="bg-white text-gray-900 px-8 py-4 rounded-xl font-bold text-lg hover:bg-gray-100 transition"
                >
                  Get Started for Free
                </Link>
              </motion.div>
            </div>
          </motion.div>
        </div>

        {/* Background Decorative Elements */}
        <div className="absolute top-0 left-0 -ml-20 -mt-20 w-80 h-80 rounded-full bg-blue-900/20 blur-3xl"></div>
        <div className="absolute bottom-0 right-0 -mr-20 -mb-20 w-80 h-80 rounded-full bg-indigo-900/20 blur-3xl"></div>
      </section>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-950 py-12 border-t border-gray-100 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <Activity className="h-5 w-5 text-blue-600" />
            <span className="font-bold text-gray-900 dark:text-white">CreditRisk.AI</span>
          </div>
          <div className="text-gray-500 dark:text-gray-400 text-sm">
            &copy; 2026 Credit Risk Systems. All rights reserved.
          </div>
          <div className="flex gap-6">
            <a href="#" className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">Privacy</a>
            <a href="#" className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">Terms</a>
            <a href="#" className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">Support</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
