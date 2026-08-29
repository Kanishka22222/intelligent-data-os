// DataOS Overview Dashboard & Interactive Hub
window.DashboardsModule = {
    chartInstances: {},
    currentRecords: [],
    filteredRecords: [],

    async load(datasetName) {
        const container = document.getElementById('dashboard-content');
        if (!container) return;
        
        container.innerHTML = `<div class="flex items-center justify-center p-12 text-indigo-300 animate-pulse font-mono text-sm">
            <i data-lucide="loader" class="w-5 h-5 animate-spin mr-2"></i> Loading analytics for ${datasetName}...
        </div>`;
        lucide.createIcons();

        try {
            const [dashRes, dataRes] = await Promise.all([
                fetch(`/api/analytics/dashboard/${datasetName}`).then(r => r.json()),
                fetch(`/api/datasets/${datasetName}`).then(r => r.json())
            ]);
            this.currentRecords = dataRes.sample || [];
            this.filteredRecords = [...this.currentRecords];
            this.render(dashRes, dataRes);
        } catch (e) {
            container.innerHTML = `<div class="p-8 text-rose-400">Failed to render dashboard: ${e.message}</div>`;
        }
    },

    render(data, rawData) {
        const container = document.getElementById('dashboard-content');
        if (!container) return;

        const kpisHtml = data.kpis.map(k => `
            <div class="card p-5 relative overflow-hidden group border border-white/5 hover:border-indigo-500/30">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">${k.label}</span>
                    <span class="text-[11px] font-mono px-2 py-0.5 rounded-md bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 font-medium">${k.badge}</span>
                </div>
                <div class="text-2xl font-bold text-white tracking-tight my-1">${k.value}</div>
                <div class="text-xs text-slate-400">${k.subtext}</div>
            </div>
        `).join('');

        const chartsHtml = data.charts.map((c, i) => `
            <div class="card p-5 ${i === 0 ? 'lg:col-span-2' : ''}">
                <div class="flex items-center justify-between mb-3">
                    <div>
                        <h3 class="text-sm font-bold text-white">${c.title}</h3>
                        <p class="text-[11px] text-slate-400">Auto-mapped by heuristic dimension engine</p>
                    </div>
                    <span class="text-[10px] font-mono text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20 uppercase font-semibold">${c.type}</span>
                </div>
                <div class="h-60 relative">
                    <canvas id="${c.id}"></canvas>
                </div>
            </div>
        `).join('');

        const cols = rawData.columns || [];
        const tableHeaders = cols.slice(0, 7).map(c => `<th class="p-2.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">${c}</th>`).join('');

        container.innerHTML = `
            <!-- Top Header & Live Status -->
            <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
                <div>
                    <div class="flex items-center gap-2 mb-1">
                        <h2 class="text-xl font-bold text-white tracking-tight">Analytics Workspace:</h2>
                        <span class="text-xl font-extrabold text-cyan-400">${data.dataset_name}</span>
                        <span class="live-badge ml-2"><span class="pulse-dot"></span> In-Memory Ready</span>
                    </div>
                    <p class="text-xs text-slate-400">Total Observations: <strong class="text-slate-200">${rawData.total_rows || 0} rows</strong> • Dimensions: <strong class="text-slate-200">${cols.length} columns</strong></p>
                </div>
                <div class="flex items-center gap-2.5">
                    <a href="/api/analytics/export-html/${data.dataset_name}" target="_blank" class="btn-secondary text-xs">
                        <i data-lucide="file-text" class="w-3.5 h-3.5 text-indigo-400"></i> Export Brief (PDF/HTML)
                    </a>
                    <button onclick="window.DashboardsModule.triggerAutoClean()" class="btn-primary text-xs">
                        <i data-lucide="sparkles" class="w-3.5 h-3.5 text-amber-300"></i> 1-Click Auto-Clean ETL
                    </button>
                </div>
            </div>

            <!-- Front Quick Action Operations Hub with Working switchTab -->
            <div class="card p-4 mb-6 border-indigo-500/20 bg-indigo-950/20">
                <div class="text-xs font-bold uppercase tracking-wider text-indigo-300 mb-3 flex items-center gap-1.5">
                    <i data-lucide="zap" class="w-3.5 h-3.5 text-amber-400"></i> Quick Operations for ${data.dataset_name}
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5">
                    <button onclick="window.DashboardsModule.triggerAutoClean()" class="card card-interactive p-3 text-left flex flex-col justify-between cursor-pointer">
                        <i data-lucide="sparkles" class="w-4 h-4 text-amber-400 mb-2"></i>
                        <div>
                            <div class="text-xs font-bold text-white">Auto-Clean</div>
                            <div class="text-[10px] text-slate-400">Fix nulls & outliers</div>
                        </div>
                    </button>

                    <button onclick="window.switchTab('nlq')" class="card card-interactive p-3 text-left flex flex-col justify-between cursor-pointer">
                        <i data-lucide="bot" class="w-4 h-4 text-cyan-400 mb-2"></i>
                        <div>
                            <div class="text-xs font-bold text-white">Ask AI Copilot</div>
                            <div class="text-[10px] text-slate-400">Voice & natural query</div>
                        </div>
                    </button>

                    <button onclick="window.switchTab('canvas')" class="card card-interactive p-3 text-left flex flex-col justify-between cursor-pointer">
                        <i data-lucide="workflow" class="w-4 h-4 text-indigo-400 mb-2"></i>
                        <div>
                            <div class="text-xs font-bold text-white">ETL Canvas</div>
                            <div class="text-[10px] text-slate-400">Visual DAG builder</div>
                        </div>
                    </button>

                    <button onclick="window.switchTab('brain')" class="card card-interactive p-3 text-left flex flex-col justify-between cursor-pointer">
                        <i data-lucide="trending-up" class="w-4 h-4 text-emerald-400 mb-2"></i>
                        <div>
                            <div class="text-xs font-bold text-white">AI Forecast</div>
                            <div class="text-[10px] text-slate-400">Predict demand/churn</div>
                        </div>
                    </button>

                    <button onclick="window.switchTab('security')" class="card card-interactive p-3 text-left flex flex-col justify-between cursor-pointer">
                        <i data-lucide="shield-check" class="w-4 h-4 text-rose-400 mb-2"></i>
                        <div>
                            <div class="text-xs font-bold text-white">PII & DPDP</div>
                            <div class="text-[10px] text-slate-400">Sanitize & verify</div>
                        </div>
                    </button>

                    <button onclick="window.switchTab('billing')" class="card card-interactive p-3 text-left flex flex-col justify-between cursor-pointer">
                        <i data-lucide="credit-card" class="w-4 h-4 text-purple-400 mb-2"></i>
                        <div>
                            <div class="text-xs font-bold text-white">Subscription</div>
                            <div class="text-[10px] text-slate-400">Razorpay / Stripe</div>
                        </div>
                    </button>
                </div>
            </div>

            <!-- KPI Metric Cards Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                ${kpisHtml}
            </div>

            <!-- Charts Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-6">
                ${chartsHtml}
            </div>

            <!-- Live Data Table Explorer -->
            <div class="card p-5">
                <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
                    <div>
                        <h3 class="text-sm font-bold text-white flex items-center gap-2">
                            <i data-lucide="table" class="w-4 h-4 text-cyan-400"></i> Live Data Inspector (Sample Preview)
                        </h3>
                        <p class="text-[11px] text-slate-400">Inspect raw records or search values inline</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <input type="text" id="table-search-input" onkeyup="window.DashboardsModule.filterTable()" placeholder="Search in records..." class="bg-slate-900 border border-white/10 text-xs rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-indigo-500 w-48">
                        <span class="text-xs font-mono text-slate-400" id="table-count-badge">Showing ${Math.min(15, this.filteredRecords.length)} of ${this.currentRecords.length}</span>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-white/10 bg-slate-900/40">
                                ${tableHeaders}
                            </tr>
                        </thead>
                        <tbody id="raw-data-table-body">
                            ${this.renderTableRows(cols.slice(0, 7))}
                        </tbody>
                    </table>
                </div>
            </div>
        `;

        lucide.createIcons();

        // Render Chart.js
        data.charts.forEach(c => {
            const ctx = document.getElementById(c.id);
            if (!ctx) return;
            if (this.chartInstances[c.id]) {
                this.chartInstances[c.id].destroy();
            }
            this.chartInstances[c.id] = new Chart(ctx, {
                type: c.type,
                data: {
                    labels: c.labels,
                    datasets: c.datasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 11 } } }
                    },
                    scales: c.type !== 'doughnut' && c.type !== 'pie' ? {
                        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#94a3b8', font: { size: 11 } } },
                        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#94a3b8', font: { size: 11 } } }
                    } : {}
                }
            });
        });
    },

    renderTableRows(visibleCols) {
        const rows = this.filteredRecords.slice(0, 15);
        if (rows.length === 0) {
            return `<tr><td colspan="${visibleCols.length}" class="p-6 text-center text-xs text-slate-500">No matching records found.</td></tr>`;
        }
        return rows.map(r => `
            <tr class="border-b border-white/5 hover:bg-white/[0.02] text-xs">
                ${visibleCols.map(c => `<td class="p-2.5 text-slate-300 font-mono">${r[c] !== undefined ? r[c] : '-'}</td>`).join('')}
            </tr>
        `).join('');
    },

    filterTable() {
        const q = (document.getElementById('table-search-input')?.value || '').toLowerCase();
        if (!q) {
            this.filteredRecords = [...this.currentRecords];
        } else {
            this.filteredRecords = this.currentRecords.filter(row => 
                Object.values(row).some(v => String(v).toLowerCase().includes(q))
            );
        }
        const tbody = document.getElementById('raw-data-table-body');
        const badge = document.getElementById('table-count-badge');
        if (tbody && this.currentRecords.length > 0) {
            const visibleCols = Object.keys(this.currentRecords[0]).slice(0, 7);
            tbody.innerHTML = this.renderTableRows(visibleCols);
        }
        if (badge) {
            badge.innerText = `Showing ${Math.min(15, this.filteredRecords.length)} of ${this.currentRecords.length}`;
        }
    },

    async triggerAutoClean() {
        showToast(`Executing Auto-Clean ETL on ${state.currentDataset}...`, 'info');
        try {
            const res = await fetch(`/api/etl/auto-clean?dataset_name=${state.currentDataset}`, { method: 'POST' });
            const data = await res.json();
            if (data.status === 'success') {
                showToast(`Cleaned! Score improved: ${data.initial_score}% ➔ ${data.final_score}% (+${data.improvement_pct}%)`, 'success');
                await loadDatasets();
                state.currentDataset = data.clean_dataset_name;
                updateDatasetDropdown();
                this.load(state.currentDataset);
            }
        } catch (e) {
            showToast(`Auto-clean failed: ${e.message}`, 'error');
        }
    }
};
