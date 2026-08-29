// DataOS Subscriptions, Razorpay/Stripe & Invoicing
window.BillingModule = {
    async load() {
        try {
            const res = await fetch('/api/billing/plans');
            const data = await res.json();
            this.render(data);
        } catch (e) {
            console.error('Billing load error', e);
        }
    },

    render(data) {
        const container = document.getElementById('billing-plans-grid');
        if (!container) return;

        const currentId = data.current_plan.id;
        const quotaEl = document.getElementById('billing-quota-indicator');
        if (quotaEl) {
            quotaEl.innerHTML = `
                <div class="text-xs text-slate-400">Monthly Query Quota: <strong class="text-white">${data.query_quota_used} / ${data.query_quota_limit}</strong></div>
                <div class="w-full bg-slate-800 rounded-full h-1.5 mt-1.5 overflow-hidden">
                    <div class="bg-indigo-500 h-1.5 rounded-full" style="width: ${(data.query_quota_used/data.query_quota_limit)*100}%;"></div>
                </div>
            `;
        }

        container.innerHTML = data.plans.map(p => {
            const isCurrent = p.id === currentId;
            return `
                <div class="card p-6 flex flex-col justify-between relative ${p.is_popular ? 'border-indigo-500/50 shadow-2xl shadow-indigo-500/10' : ''}">
                    ${p.badge ? `<div class="absolute -top-3 right-4 px-2.5 py-0.5 rounded-full text-[10px] font-bold tracking-wider uppercase bg-gradient-to-r from-indigo-500 to-cyan-500 text-white shadow">${p.badge}</div>` : ''}
                    <div>
                        <h3 class="text-base font-bold text-white mb-1">${p.name}</h3>
                        <div class="flex items-baseline gap-1 my-3">
                            <span class="text-3xl font-extrabold text-white">₹${p.price_inr.toLocaleString()}</span>
                            <span class="text-xs text-slate-400 font-mono">/ ${p.billing_cycle}</span>
                        </div>
                        <div class="text-xs font-mono text-slate-400 mb-5 pb-3 border-b border-white/5">
                            ($${p.price_usd} USD equivalent)
                        </div>
                        <ul class="space-y-2.5 mb-6">
                            ${p.features.map(f => `
                                <li class="text-xs text-slate-300 flex items-start gap-2">
                                    <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5"></i>
                                    <span>${f}</span>
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                    <div>
                        ${isCurrent ? `
                            <button disabled class="w-full py-2.5 rounded-xl bg-slate-800 text-slate-400 text-xs font-semibold cursor-not-allowed">
                                Current Active Plan
                            </button>
                        ` : `
                            <button onclick="window.BillingModule.openCheckoutModal('${p.id}')" class="w-full btn-primary justify-center text-xs">
                                Upgrade with Razorpay / Stripe
                            </button>
                        `}
                    </div>
                </div>
            `;
        }).join('');

        lucide.createIcons();
    },

    async openCheckoutModal(planId) {
        showToast(`Initializing secure payment session for ${planId}...`, 'info');
        try {
            const res = await fetch('/api/billing/create-checkout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ plan_id: planId, currency: 'INR' })
            });
            const data = await res.json();
            const session = data.session;

            const modal = document.getElementById('payment-checkout-modal');
            if (modal) {
                modal.classList.remove('hidden');
                document.getElementById('checkout-plan-name').innerText = planId === 'plan_pro' ? 'Pro Data Strategist' : 'Enterprise Autonomous Brain';
                document.getElementById('checkout-amount-display').innerText = session.display_amount;
                document.getElementById('checkout-order-id').innerText = session.order_id;
                document.getElementById('checkout-pay-btn').onclick = () => this.confirmPayment(session.order_id, planId);
            }
        } catch (e) {
            showToast(`Checkout initialization failed: ${e.message}`, 'error');
        }
    },

    closeCheckoutModal() {
        const modal = document.getElementById('payment-checkout-modal');
        if (modal) modal.classList.add('hidden');
    },

    fillDemoCard() {
        const num = document.getElementById('card-num-input');
        const exp = document.getElementById('card-exp-input');
        const cvv = document.getElementById('card-cvv-input');
        if (num) num.value = '4242 4242 4242 4242';
        if (exp) exp.value = '12/28';
        if (cvv) cvv.value = '888';
        showToast('Autofilled demo test card credentials', 'info');
    },

    async confirmPayment(orderId, planId) {
        showToast('Authorizing Razorpay / Stripe transaction...', 'info');
        try {
            const res = await fetch('/api/billing/verify-payment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ order_id: orderId, plan_id: planId, payment_id: `pay_${Date.now()}` })
            });
            const data = await res.json();
            if (data.status === 'success') {
                this.closeCheckoutModal();
                showToast('Payment successful! Subscription plan upgraded.', 'success');
                this.renderInvoiceModal(data.invoice);
                this.load();
            }
        } catch (e) {
            showToast(`Payment verification error: ${e.message}`, 'error');
        }
    },

    renderInvoiceModal(invoice) {
        const modal = document.getElementById('invoice-receipt-modal');
        if (!modal) return;
        modal.classList.remove('hidden');
        document.getElementById('invoice-no-display').innerText = invoice.invoice_number;
        document.getElementById('invoice-date-display').innerText = invoice.date;
        document.getElementById('invoice-total-display').innerText = invoice.total_paid;
    },

    closeInvoiceModal() {
        const modal = document.getElementById('invoice-receipt-modal');
        if (modal) modal.classList.add('hidden');
    }
};
