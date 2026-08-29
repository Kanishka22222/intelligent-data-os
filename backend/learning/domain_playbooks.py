class DomainPlaybooks:
    @staticmethod
    def get_playbook(domain_name):
        playbooks = {
            "gst_compliance": {
                "name": "Indian GST Statutory Intelligence",
                "statutes": ["CGST Act 2017", "IGST Act 2017", "Rule 36(4) ITC Cap"],
                "rules": [
                    "HSN Codes: 6-digit mandatory for turnover > ₹5 Crore, 4-digit for B2B <= ₹5 Crore.",
                    "Input Tax Credit (ITC): Restricted to invoices matching supplier GSTR-1 in GSTR-2B.",
                    "E-Way Bill: Mandatory for inter-state consignment values exceeding ₹50,000.",
                    "E-Invoicing: Mandatory for all B2B businesses with turnover > ₹5 Crore."
                ]
            },
            "rbi_banking": {
                "name": "Reserve Bank of India (RBI) Prudential Norms",
                "statutes": ["Banking Regulation Act 1949", "Master Direction on Data Localization 2018"],
                "rules": [
                    "Data Localization: 100% of end-to-end payment transaction data must reside in domestic Indian servers.",
                    "Capital Adequacy Ratio (CAR): Minimum Tier 1 capital must be maintained above 9%.",
                    "NPA Classification: Overdue payments past 90 days must be tagged as Sub-Standard."
                ]
            },
            "sebi_governance": {
                "name": "SEBI Listing Obligations & Disclosure Requirements (LODR)",
                "statutes": ["SEBI LODR Regulations 2015", "Insider Trading Prohibition (PIT 2015)"],
                "rules": [
                    "Quarterly Financial Results: Mandatory disclosure within 45 days of quarter close.",
                    "Related Party Transactions: Audit committee prior approval mandatory.",
                    "Debt-to-Equity Covenant: Monitored on trailing 12-month EBITDA basis."
                ]
            }
        }
        return playbooks.get(domain_name, playbooks["gst_compliance"])
