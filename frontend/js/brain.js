// DataOS AI Business Brain & Predictive Intelligence
window.BrainModule = {
    forecastChart: null,

    async load(datasetName) {
        this.loadModelStatus();
        this.loadForecast(datasetName);
        this.loadCustomerBrain(datasetName);
        this.loadAnomalies(datasetName);
        this.loadStrategy(datasetName);
    },

    async loadForecast(datasetName) {
        try {
            const res = await fetch(`/api/brain/forecast/${datasetName}`);
            const data = await res.json();
            const ctx = document.getElementById('forecast-chart-canvas');
            if (!ctx) return;
            if (this.forecastChart) this.forecastChart.destroy();

            this.forecastChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        { label: 'Historical Trend', data: data.historical, borderColor: '#3b82f6', backgroundColor: 'rgba(59, 130, 246, 0.1)', fill: false },
                        { label: 'AI Forecast', data: data.forecast, borderColor: '#10b981', borderDash: [5, 5], fill: false },
                        { label: 'Upper 95% Bound', data: data.upper_bound, borderColor: 'rgba(16, 185, 129, 0.3)', fill: '+1', backgroundColor: 'rgba(16, 185, 129, 0.08)' },
                        { label: 'Lower 95% Bound', data: data.lower_bound, borderColor: 'rgba(16, 185, 129, 0.3)', fill: false }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: '#94a3b8' } } },
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    }
                }
            });

            const badge = document.getElementById('forecast-growth-badge');
            if (badge) badge.innerText = `+${data.growth_rate_pct}% Expected Growth (${data.model_confidence} Confidence)`;
        } catch (e) {
            console.error('Forecast error', e);
        }
    },

    async loadCustomerBrain(datasetName) {
        try {
            const res = await fetch(`/api/brain/customer-insights/${datasetName}`);
            const data = await res.json();
            const container = document.getElementById('customer-segments-container');
            if (!container) return;

            const segHtml = data.segments.map(s => `
                <div class="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 mb-2.5">
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-xs font-bold" style="color: ${s.color};">${s.segment}</span>
                        <span class="text-xs font-mono text-white">${s.count} Users</span>
                    </div>
                    <div class="text-xs text-slate-400">${s.action}</div>
                </div>
            `).join('');

            const leversHtml = data.top_retention_levers.map(l => `<li class="text-xs text-slate-300 mb-1.5 flex items-start gap-2"><span class="text-indigo-400">❖</span> ${l}</li>`).join('');

            container.innerHTML = `
                <div class="flex items-center justify-between mb-4">
                    <span class="text-xs text-slate-400 font-medium">Cohort Intelligence: <strong class="text-white">${data.type}</strong></span>
                    <span class="text-xs font-mono px-2 py-0.5 rounded bg-rose-500/10 border border-rose-500/20 text-rose-400">Churn Rate: ${data.churn_rate_pct}%</span>
                </div>
                <div class="mb-4">${segHtml}</div>
                <div class="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Automated Retention Levers</div>
                <ul class="list-none">${leversHtml}</ul>
            `;
        } catch (e) {
            console.error('Customer brain error', e);
        }
    },

    async loadAnomalies(datasetName) {
        try {
            const res = await fetch(`/api/brain/anomalies/${datasetName}`);
            const data = await res.json();
            const container = document.getElementById('anomaly-alerts-container');
            if (!container) return;

            if (data.records.length === 0) {
                container.innerHTML = `<div class="p-6 text-center text-xs text-slate-400">Zero statistical anomalies detected. Operating within standard parameters.</div>`;
                return;
            }

            const itemsHtml = data.records.map(a => `
                <div class="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 mb-2">
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-xs font-bold text-rose-400 flex items-center gap-1">
                            <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i> ${a.severity} Spike in ${a.metric_column}
                        </span>
                        <span class="text-xs font-mono text-slate-400">${a.z_score}σ deviation</span>
                    </div>
                    <div class="text-xs text-slate-300">${a.reason}</div>
                </div>
            `).join('');

            container.innerHTML = itemsHtml;
            lucide.createIcons();
        } catch (e) {
            console.error('Anomaly error', e);
        }
    },

    async loadStrategy(datasetName) {
        try {
            const res = await fetch(`/api/brain/strategy/${datasetName}`);
            const data = await res.json();
            const container = document.getElementById('strategy-playbook-container');
            if (!container) return;

            const pillarsHtml = data.strategic_pillars.map(p => `
                <div class="p-4 rounded-xl bg-slate-900/50 border border-slate-800 mb-3">
                    <div class="flex items-center justify-between mb-1.5">
                        <h4 class="text-sm font-semibold text-white">${p.pillar}</h4>
                        <span class="text-xs font-mono text-cyan-300 px-2 py-0.5 rounded bg-cyan-500/10 border border-cyan-500/20">${p.impact}</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">${p.recommendation}</p>
                </div>
            `).join('');

            container.innerHTML = `
                <div class="mb-4">
                    <span class="text-xs text-slate-400 font-mono">Domain: ${data.sector} | Confidence: ${data.confidence_score}</span>
                    <p class="text-xs text-slate-300 mt-1 italic">${data.narrative}</p>
                </div>
                ${pillarsHtml}
            `;
        } catch (e) {
            console.error('Strategy error', e);
        }
    },

    async loadModelStatus() {
        try {
            const res = await fetch('/api/brain/model-status');
            const data = await res.json();
            
            const tag = document.getElementById('brain-version-tag');
            const score = document.getElementById('brain-autonomy-score');
            const acc = document.getElementById('brain-accuracy-val');
            const loss = document.getElementById('brain-loss-val');
            const datasets = document.getElementById('brain-datasets-count');
            const bar = document.getElementById('brain-autonomy-bar');
            
            if (tag) tag.innerText = data.model_version;
            if (score) score.innerText = `${data.autonomy_readiness_score}%`;
            if (acc) acc.innerText = `${data.current_accuracy_pct}%`;
            if (loss) loss.innerText = `${data.current_loss}`;
            if (datasets) datasets.innerText = `${data.total_datasets_learned} Datasets (${data.total_samples_digested.toLocaleString()} Samples)`;
            if (bar) bar.style.width = `${data.autonomy_readiness_score}%`;
        } catch (e) {
            console.error('Model status load error', e);
        }
    },

    async trainActiveDataset() {
        const btn = document.getElementById('train-brain-btn');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = `<i data-lucide="loader" class="w-3.5 h-3.5 animate-spin"></i> Ingesting & Fine-Tuning...`;
            lucide.createIcons();
        }
        showToast(`Running continuous gradient training on ${state.currentDataset}...`, 'info');
        
        try {
            const res = await fetch('/api/brain/train', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ dataset_name: state.currentDataset })
            });
            const data = await res.json();
            if (data.status === 'success') {
                showToast(`Training complete! Model evolved to ${data.model_version} (${data.autonomy_readiness_score}% Autonomy)`, 'success');
                await this.loadModelStatus();
                this.loadForecast(state.currentDataset);
            }
        } catch (e) {
            showToast(`Training failed: ${e.message}`, 'error');
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = `<i data-lucide="zap" class="w-3.5 h-3.5 text-amber-300"></i> ⚡ Train on Active Dataset`;
                lucide.createIcons();
            }
        }
    },

    exportStandaloneModel() {
        showToast('Packaging self-contained standalone AI model...', 'info');
        window.location.href = '/api/brain/export-standalone';
        setTimeout(() => {
            showToast('Standalone model downloaded: dataos_brain_standalone.py', 'success');
        }, 1200);
    },

    async testStandaloneInference() {
        showToast('Running zero-server standalone inference test...', 'info');
        try {
            const res = await fetch('/api/brain/standalone-inference', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    series: [1200.0, 1400.0, 1550.0, 1750.0, 2050.0],
                    query: 'What is our expected sales trajectory?'
                })
            });
            const data = await res.json();
            if (data.status === 'success') {
                showToast(`Standalone Test Passed: ${data.message} Forecast: [${data.sample_forecast.join(', ')}]`, 'success');
            }
        } catch (e) {
            showToast(`Standalone test failed: ${e.message}`, 'error');
        }
    }
};

