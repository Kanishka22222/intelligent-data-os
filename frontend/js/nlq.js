// DataOS Conversational NLQ & Multi-Lingual Voice Assistant
window.NLQModule = {
    isListening: false,
    recognition: null,

    init() {
        const input = document.getElementById('nlq-input-field');
        if (input) {
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') this.sendQuery();
            });
        }
        this.initSpeech();
    },

    initSpeech() {
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRec) {
            this.recognition = new SpeechRec();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';

            this.recognition.onstart = () => {
                this.isListening = true;
                const micBtn = document.getElementById('nlq-mic-btn');
                if (micBtn) micBtn.classList.add('text-rose-400', 'animate-pulse');
                showToast('Listening to your voice command...', 'info');
            };

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                const input = document.getElementById('nlq-input-field');
                if (input) {
                    input.value = transcript;
                    this.sendQuery();
                }
            };

            this.recognition.onend = () => {
                this.isListening = false;
                const micBtn = document.getElementById('nlq-mic-btn');
                if (micBtn) micBtn.classList.remove('text-rose-400', 'animate-pulse');
            };
        }
    },

    toggleVoice() {
        if (!this.recognition) {
            showToast('Voice input is supported in Chrome, Edge, and Safari. Please use text prompt.', 'error');
            return;
        }
        if (this.isListening) {
            this.recognition.stop();
        } else {
            const langSelect = document.getElementById('voice-lang-select');
            if (langSelect) this.recognition.lang = langSelect.value;
            this.recognition.start();
        }
    },

    speak(text) {
        if ('speechSynthesis' in window) {
            const clean = text.replace(/[*_#`]/g, '');
            const utterance = new SpeechSynthesisUtterance(clean);
            window.speechSynthesis.speak(utterance);
        }
    },

    setPrompt(promptText) {
        const input = document.getElementById('nlq-input-field');
        if (input) {
            input.value = promptText;
            this.sendQuery();
        }
    },

    async sendQuery() {
        const input = document.getElementById('nlq-input-field');
        const q = input.value.trim();
        if (!q) return;

        const chatBox = document.getElementById('nlq-chat-messages');
        if (!chatBox) return;

        // Append User Bubble
        chatBox.innerHTML += `
            <div class="flex justify-end mb-4">
                <div class="bg-indigo-600/40 border border-indigo-500/50 rounded-2xl rounded-tr-none px-4 py-3 max-w-lg text-xs md:text-sm text-white font-medium shadow-md">
                    ${q}
                </div>
            </div>
        `;
        input.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;

        const loadId = `load_${Date.now()}`;
        chatBox.innerHTML += `
            <div id="${loadId}" class="flex justify-start mb-4">
                <div class="bg-slate-800/80 border border-slate-700/60 rounded-2xl rounded-tl-none px-4 py-3 max-w-lg text-xs md:text-sm text-indigo-300 flex items-center gap-2">
                    <i data-lucide="loader" class="w-4 h-4 animate-spin"></i> Synthesizing SQL & computing intelligence...
                </div>
            </div>
        `;
        lucide.createIcons();
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            const res = await fetch('/api/nlp/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: q, dataset_name: state.currentDataset })
            });
            const data = await res.json();
            document.getElementById(loadId)?.remove();

            chatBox.innerHTML += `
                <div class="flex justify-start mb-4">
                    <div class="card border-indigo-500/30 rounded-2xl rounded-tl-none p-4 max-w-xl text-xs md:text-sm text-slate-200 shadow-xl">
                        <div class="flex items-center justify-between mb-2 pb-2 border-b border-white/5">
                            <span class="text-xs font-mono text-cyan-400 flex items-center gap-1.5 font-bold">
                                <i data-lucide="sparkles" class="w-3.5 h-3.5 text-indigo-400"></i> DataOS Cognitive Answer
                            </span>
                            <span class="text-[11px] font-mono text-slate-400 bg-slate-900 px-2 py-0.5 rounded">${data.execution_time_ms} ms</span>
                        </div>
                        <div class="mb-3 text-slate-100 leading-relaxed">${data.answer.replace(/\*\*(.*?)\*\*/g, '<strong class="text-cyan-300">$1</strong>')}</div>
                        ${data.generated_sql ? `
                            <div class="bg-black/50 rounded-lg p-2.5 font-mono text-[11px] text-emerald-400 border border-emerald-500/20 mb-2 overflow-x-auto">
                                ${data.generated_sql}
                            </div>
                        ` : ''}
                        <div class="flex items-center gap-3 mt-2">
                            <button onclick="window.NLQModule.speak('${data.answer.replace(/'/g, "\'")}')" class="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1">
                                <i data-lucide="volume-2" class="w-3.5 h-3.5"></i> Read aloud
                            </button>
                        </div>
                    </div>
                </div>
            `;
            lucide.createIcons();
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (e) {
            document.getElementById(loadId)?.remove();
            chatBox.innerHTML += `<div class="p-3 text-rose-400 text-xs">Error: ${e.message}</div>`;
        }
    }
};
