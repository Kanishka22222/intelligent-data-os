// DataOS Visual Drag & Drop ETL Pipeline Canvas
window.CanvasModule = {
    nodes: [],

    init(datasetName) {
        this.loadTemplate('ecommerce');
    },

    loadTemplate(templateName) {
        if (templateName === 'ecommerce') {
            this.nodes = [
                { id: 1, type: 'source', title: 'Data Source', params: { dataset: state.currentDataset }, x: 30, y: 50 },
                { id: 2, type: 'auto_clean', title: 'Auto-Clean & Deduplicate', params: {}, x: 260, y: 50 },
                { id: 3, type: 'filter', title: 'Filter High Value', params: { column: 'Sales', operator: '>', value: '200' }, x: 490, y: 50 },
                { id: 4, type: 'aggregate', title: 'Group by Category', params: { group_by: ['Category'], agg_column: 'Sales', func: 'sum' }, x: 720, y: 50 }
            ];
            showToast('Loaded template: E-Commerce Margin Maximizer', 'info');
        } else if (templateName === 'gst') {
            this.nodes = [
                { id: 1, type: 'source', title: 'GST B2B Invoices', params: { dataset: 'indian_financial_gst' }, x: 30, y: 50 },
                { id: 2, type: 'filter', title: 'Filter Taxable Supply', params: { column: 'Taxable_Value', operator: '>', value: '100000' }, x: 260, y: 50 },
                { id: 3, type: 'aggregate', title: 'Sum Tax Liability', params: { group_by: ['Place_Of_Supply'], agg_column: 'Total_Invoice_Value', func: 'sum' }, x: 490, y: 50 }
            ];
            showToast('Loaded template: GST Compliance & ITC Audit Flow', 'info');
        } else if (templateName === 'churn') {
            this.nodes = [
                { id: 1, type: 'source', title: 'Subscribers Feed', params: { dataset: 'customer_churn' }, x: 30, y: 50 },
                { id: 2, type: 'filter', title: 'Filter Churn Risk', params: { column: 'ChurnRiskScore', operator: '>', value: '0.6' }, x: 260, y: 50 },
                { id: 3, type: 'aggregate', title: 'Loss by Contract', params: { group_by: ['ContractType'], agg_column: 'MonthlyCharges', func: 'sum' }, x: 490, y: 50 }
            ];
            showToast('Loaded template: SaaS Churn Prevention Funnel', 'info');
        }
        this.renderCanvas();
    },

    renderCanvas() {
        const container = document.getElementById('pipeline-canvas-area');
        if (!container) return;

        const nodesHtml = this.nodes.map(n => `
            <div class="canvas-node" style="left: ${n.x}px; top: ${n.y}px;" data-id="${n.id}">
                <div class="flex items-center justify-between mb-1.5">
                    <span class="text-xs font-bold text-indigo-300 uppercase tracking-wider">${n.title}</span>
                    <button onclick="window.CanvasModule.removeNode(${n.id})" class="text-slate-500 hover:text-rose-400 p-0.5">
                        <i data-lucide="x" class="w-3.5 h-3.5"></i>
                    </button>
                </div>
                <div class="text-[11px] text-slate-400 font-mono bg-black/40 p-2 rounded border border-white/5 overflow-hidden text-ellipsis">
                    ${JSON.stringify(n.params)}
                </div>
            </div>
        `).join('');

        container.innerHTML = nodesHtml;
        lucide.createIcons();
    },

    addNode(type) {
        const id = this.nodes.length + 1;
        const titles = {
            'filter': 'Filter Condition',
            'select': 'Select Columns',
            'sort': 'Sort Order',
            'aggregate': 'Group & Aggregate',
            'auto_clean': 'Auto-Clean ETL',
            'mutate': 'Calculated Field'
        };
        const defaultParams = {
            'filter': { column: 'Sales', operator: '>', value: '100' },
            'select': { columns: ['Order_ID', 'Category', 'Sales', 'Profit'] },
            'sort': { column: 'Sales', ascending: false },
            'aggregate': { group_by: ['Region'], agg_column: 'Sales', func: 'sum' },
            'auto_clean': {},
            'mutate': { new_column: 'Margin_Pct', formula: 'Profit / Sales * 100' }
        };
        this.nodes.push({
            id: id,
            type: type,
            title: titles[type] || type,
            params: defaultParams[type] || {},
            x: 40 + (this.nodes.length * 30) % 500,
            y: 160
        });
        this.renderCanvas();
        showToast(`Added ${titles[type]} node to DAG`, 'info');
    },

    removeNode(id) {
        this.nodes = this.nodes.filter(n => n.id !== id);
        this.renderCanvas();
    },

    async runPipeline() {
        showToast('Running transformation graph...', 'info');
        const traceBox = document.getElementById('pipeline-trace-box');
        if (traceBox) traceBox.innerHTML = '<div class="text-indigo-400 p-5 animate-pulse text-xs">Executing multi-step DAG pipeline...</div>';

        try {
            const res = await fetch('/api/etl/run-pipeline', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    dataset_name: state.currentDataset,
                    nodes: this.nodes.map(n => ({ type: n.type, params: n.params }))
                })
            });
            const data = await res.json();
            if (traceBox) {
                const stepsHtml = data.execution_trace.map(s => `
                    <div class="flex items-center justify-between p-3 rounded-lg bg-slate-900/70 border border-slate-800 text-xs mb-2">
                        <div class="flex items-center gap-2.5">
                            <span class="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 font-bold flex items-center justify-center text-[10px]">✓</span>
                            <span class="text-white font-medium">${s.description}</span>
                        </div>
                        <span class="font-mono text-slate-400 text-[11px]">${s.rows_before} ➔ ${s.rows_after} rows</span>
                    </div>
                `).join('');
                traceBox.innerHTML = `
                    <div class="p-4">
                        <div class="flex items-center justify-between mb-3 pb-2 border-b border-white/5">
                            <span class="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                                <i data-lucide="check-circle" class="w-4 h-4"></i> Pipeline Complete (${data.execution_time_ms} ms)
                            </span>
                            <span class="text-xs font-mono text-cyan-400 font-semibold">Created Dataset: ${data.output_dataset_name}</span>
                        </div>
                        ${stepsHtml}
                    </div>
                `;
                lucide.createIcons();
                await loadDatasets();
                showToast(`New dataset generated: ${data.output_dataset_name}`, 'success');
            }
        } catch (e) {
            if (traceBox) traceBox.innerHTML = `<div class="p-4 text-rose-400 text-xs">Execution Error: ${e.message}</div>`;
        }
    }
};
