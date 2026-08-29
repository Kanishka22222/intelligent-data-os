// DataOS Security, DPDP Compliance & SHA-256 Audit Ledger
window.SecurityModule = {
    async load(datasetName) {
        this.loadPIIScan(datasetName);
        this.loadCompliance(datasetName);
        this.loadAuditLogs();
    },

    async loadPIIScan(datasetName) {
        try {
            const res = await fetch(`/api/security/scan-pii/${datasetName}`);
            const data = await res.json();
            const container = document.getElementById('pii-findings-container');
            if (!container) return;

            if (data.findings.length === 0) {
                container.innerHTML = `
                    <div class="p-6 text-center text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 rounded-xl">
                        <i data-lucide="shield-check" class="w-6 h-6 mx-auto mb-1"></i>
                        No unmasked Personally Identifiable Information (PII) found in this dataset.
                    </div>
                `;
            } else {
                const items = data.findings.map(f => `
                    <div class="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 mb-2.5 flex items-center justify-between">
                        <div>
                            <div class="text-xs font-bold text-white flex items-center gap-1.5">
                                <span class="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-400 font-mono text-[10px]">${f.severity}</span>
                                Column: <span class="text-cyan-300">${f.column}</span>
                            </div>
                            <div class="text-xs text-slate-400 mt-1">Detected ${f.matched_samples} instances of <strong>${f.pii_type}</strong></div>
                        </div>
                        <button onclick="window.SecurityModule.maskPII('${datasetName}')" class="btn-secondary text-xs">
                            <i data-lucide="lock" class="w-3 h-3 text-cyan-400"></i> Redact/Mask
                        </button>
                    </div>
                `).join('');
                container.innerHTML = items;
            }
            lucide.createIcons();
        } catch (e) {
            console.error('PII error', e);
        }
    },

    async maskPII(datasetName) {
        showToast(`Sanitizing sensitive PII in ${datasetName}...`, 'info');
        try {
            const res = await fetch('/api/security/mask-pii', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ dataset_name: datasetName, method: 'redact' })
            });
            const data = await res.json();
            if (data.status === 'success') {
                showToast(`Created PII-sanitized dataset: ${data.masked_dataset_name}`, 'success');
                await loadDatasets();
                state.currentDataset = data.masked_dataset_name;
                updateDatasetDropdown();
                this.load(state.currentDataset);
            }
        } catch (e) {
            showToast(`PII Masking failed: ${e.message}`, 'error');
        }
    },

    async loadCompliance(datasetName) {
        try {
            const res = await fetch(`/api/security/compliance-audit/${datasetName}`);
            const data = await res.json();
            const scoreEl = document.getElementById('compliance-score-val');
            if (scoreEl) scoreEl.innerText = `${data.overall_compliance_score}%`;

            const container = document.getElementById('compliance-checks-list');
            if (!container) return;

            const checksHtml = data.checks.map(c => `
                <div class="p-3 rounded-lg bg-slate-900/40 border border-slate-800/80 mb-2 flex items-start justify-between">
                    <div>
                        <div class="text-xs font-semibold text-slate-200">${c.standard}</div>
                        <div class="text-xs text-slate-400 mt-0.5">${c.requirement}</div>
                        <div class="text-[11px] text-cyan-400 mt-1">${c.detail}</div>
                    </div>
                    <span class="text-xs font-bold text-emerald-400 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">${c.status}</span>
                </div>
            `).join('');
            container.innerHTML = checksHtml;
        } catch (e) {
            console.error('Compliance error', e);
        }
    },

    async loadAuditLogs() {
        try {
            const res = await fetch('/api/security/audit-logs');
            const data = await res.json();
            const container = document.getElementById('audit-ledger-table-body');
            if (!container) return;

            container.innerHTML = data.logs.map(l => `
                <tr class="border-b border-slate-800/60 hover:bg-slate-800/20 text-xs">
                    <td class="p-2.5 font-mono text-indigo-300">#${l.block_index}</td>
                    <td class="p-2.5 text-slate-400">${l.timestamp}</td>
                    <td class="p-2.5 text-white font-medium">${l.user_email}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 font-mono text-[11px]">${l.action}</span></td>
                    <td class="p-2.5 text-slate-300">${l.resource}</td>
                    <td class="p-2.5 font-mono text-[10px] text-cyan-400">${l.block_hash.substring(0, 16)}...</td>
                </tr>
            `).join('');
        } catch (e) {
            console.error('Audit log error', e);
        }
    },

    async verifyChain() {
        showToast('Verifying SHA-256 cryptographic chain integrity...', 'info');
        try {
            const res = await fetch('/api/security/verify-chain');
            const data = await res.json();
            if (data.is_valid) {
                showToast(`Verified! ${data.message}`, 'success');
            } else {
                showToast(`Chain Breached: ${data.message}`, 'error');
            }
        } catch (e) {
            showToast(`Verification error: ${e.message}`, 'error');
        }
    }
};
