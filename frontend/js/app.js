// DataOS Master State & Global Tab Controller
const state = {
    activeTab: 'dashboards',
    currentDataset: 'ecommerce_sales',
    datasets: [],
    currentUser: {
        email: 'analyst@enterprise.com',
        name: 'Senior BI Analyst',
        role: 'DataAnalyst'
    }
};

window.switchTab = function(tabName) {
    state.activeTab = tabName;
    
    // Update all navigation items (matching both .nav-item and .nav-tab)
    document.querySelectorAll('.nav-item, .nav-tab').forEach(el => {
        if (el.getAttribute('data-tab') === tabName) {
            el.classList.add('active');
        } else {
            el.classList.remove('active');
        }
    });

    // Toggle panes
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.add('hidden'));
    const target = document.getElementById(`pane-${tabName}`);
    if (target) {
        target.classList.remove('hidden');
    }

    loadCurrentTab();
    window.scrollTo({ top: 0, behavior: 'smooth' });
};

document.addEventListener('DOMContentLoaded', async () => {
    lucide.createIcons();
    initNavListeners();
    await loadDatasets();
    initDatasetSelector();
    loadCurrentTab();
    initWebSocketTelemetry();
    if (window.NLQModule) window.NLQModule.init();
});

function initNavListeners() {
    document.querySelectorAll('.nav-item, .nav-tab').forEach(item => {
        item.addEventListener('click', () => {
            const tab = item.getAttribute('data-tab');
            if (tab) window.switchTab(tab);
        });
    });
}

async function loadDatasets() {
    try {
        const res = await fetch('/api/datasets/list');
        const data = await res.json();
        state.datasets = data.datasets || [];
        updateDatasetDropdown();
    } catch (e) {
        console.error('Failed to load datasets', e);
    }
}

function updateDatasetDropdown() {
    const select = document.getElementById('global-dataset-select');
    if (!select) return;
    select.innerHTML = state.datasets.map(d => 
        `<option value="${d.name}" ${d.name === state.currentDataset ? 'selected' : ''}>
            ${d.name} (${d.row_count} rows, ${d.col_count} cols)
        </option>`
    ).join('');
}

function initDatasetSelector() {
    const select = document.getElementById('global-dataset-select');
    if (!select) return;
    select.addEventListener('change', (e) => {
        state.currentDataset = e.target.value;
        showToast(`Switched active dataset to: ${state.currentDataset}`, 'info');
        loadCurrentTab();
    });
}

function loadCurrentTab() {
    if (state.activeTab === 'dashboards' && window.DashboardsModule) {
        window.DashboardsModule.load(state.currentDataset);
    } else if (state.activeTab === 'brain' && window.BrainModule) {
        window.BrainModule.load(state.currentDataset);
    } else if (state.activeTab === 'security' && window.SecurityModule) {
        window.SecurityModule.load(state.currentDataset);
    } else if (state.activeTab === 'billing' && window.BillingModule) {
        window.BillingModule.load();
    } else if (state.activeTab === 'canvas' && window.CanvasModule) {
        window.CanvasModule.init(state.currentDataset);
    }
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    const bg = type === 'success' ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-300' : (type === 'error' ? 'bg-rose-500/20 border-rose-500/40 text-rose-300' : 'bg-indigo-500/20 border-indigo-500/40 text-indigo-300');
    toast.className = `flex items-center gap-3 px-4 py-3 rounded-xl border backdrop-blur-md shadow-2xl transition-all duration-300 pointer-events-auto ${bg}`;
    toast.innerHTML = `<span class="text-xs font-semibold">${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function initWebSocketTelemetry() {
    let mockTick = 0;
    const machines = ['CNC-ROBOT-01', 'SMT-LINE-04', 'HVAC-ZONE-02', 'PACKAGING-09'];
    setInterval(() => {
        mockTick++;
        const m = machines[mockTick % machines.length];
        const temp = (64.0 + (Math.sin(mockTick) * 5)).toFixed(1);
        const psi = (118.0 + (Math.cos(mockTick) * 4)).toFixed(1);
        const badge = document.getElementById('telemetry-stream-ticker');
        if (badge) {
            badge.innerHTML = `<span class="pulse-dot"></span> <span class="font-mono text-xs text-cyan-300">${m}: ${temp}°C | ${psi} PSI (OPTIMAL)</span>`;
        }
    }, 3000);
}

