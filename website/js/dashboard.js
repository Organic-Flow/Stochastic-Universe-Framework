// ─── Content Map ────────────────────────────────────────────────────────────
const TOPICS = [
  {
    id: 'stochastic_universe',
    label: 'Stochastic Universe',
    tabs: [
      {
            "id": "stochastic_ch1",
            "label": "Chapter 1",
            "file": "pages/stochastic_ch1.html"
      },
      {
            "id": "stochastic_ch1_1",
            "label": "1.1",
            "file": "pages/stochastic_ch1_1.html"
      },
      {
            "id": "stochastic_ch1_2",
            "label": "1.2",
            "file": "pages/stochastic_ch1_2.html"
      },
      {
            "id": "stochastic_ch1_3",
            "label": "1.3",
            "file": "pages/stochastic_ch1_3.html"
      },
      {
            "id": "stochastic_ch1_4",
            "label": "1.4",
            "file": "pages/stochastic_ch1_4.html"
      },
      {
            "id": "stochastic_ch1_5",
            "label": "1.5",
            "file": "pages/stochastic_ch1_5.html"
      },
      {
            "id": "stochastic_ch2",
            "label": "Chapter 2",
            "file": "pages/stochastic_ch2.html"
      },
      {
            "id": "stochastic_ch2_1",
            "label": "2.1",
            "file": "pages/stochastic_ch2_1.html"
      },
      {
            "id": "stochastic_ch2_2",
            "label": "2.2",
            "file": "pages/stochastic_ch2_2.html"
      },
      {
            "id": "stochastic_ch2_3",
            "label": "2.3",
            "file": "pages/stochastic_ch2_3.html"
      },
      {
            "id": "stochastic_ch2_4",
            "label": "2.4",
            "file": "pages/stochastic_ch2_4.html"
      },
      {
            "id": "stochastic_ch2_5",
            "label": "2.5",
            "file": "pages/stochastic_ch2_5.html"
      },
      {
            "id": "stochastic_ch2_6",
            "label": "2.6",
            "file": "pages/stochastic_ch2_6.html"
      },
      {
            "id": "stochastic_ch3",
            "label": "Chapter 3",
            "file": "pages/stochastic_ch3.html"
      },
      {
            "id": "stochastic_ch3_1",
            "label": "3.1",
            "file": "pages/stochastic_ch3_1.html"
      },
      {
            "id": "stochastic_ch3_2",
            "label": "3.2",
            "file": "pages/stochastic_ch3_2.html"
      },
      {
            "id": "stochastic_ch3_3",
            "label": "3.3",
            "file": "pages/stochastic_ch3_3.html"
      },
      {
            "id": "stochastic_ch3_4",
            "label": "3.4",
            "file": "pages/stochastic_ch3_4.html"
      },
      {
            "id": "stochastic_ch3_5",
            "label": "3.5",
            "file": "pages/stochastic_ch3_5.html"
      },
      {
            "id": "stochastic_ch3_6",
            "label": "3.6",
            "file": "pages/stochastic_ch3_6.html"
      },
      {
            "id": "stochastic_ch4",
            "label": "Chapter 4",
            "file": "pages/stochastic_ch4.html"
      },
      {
            "id": "stochastic_ch4_1",
            "label": "4.1",
            "file": "pages/stochastic_ch4_1.html"
      },
      {
            "id": "stochastic_ch4_2",
            "label": "4.2",
            "file": "pages/stochastic_ch4_2.html"
      },
      {
            "id": "stochastic_ch4_3",
            "label": "4.3",
            "file": "pages/stochastic_ch4_3.html"
      },
      {
            "id": "stochastic_ch4_4",
            "label": "4.4",
            "file": "pages/stochastic_ch4_4.html"
      },
      {
            "id": "stochastic_ch4_5",
            "label": "4.5",
            "file": "pages/stochastic_ch4_5.html"
      },
      {
            "id": "stochastic_ch4_6",
            "label": "4.6",
            "file": "pages/stochastic_ch4_6.html"
      },
      {
            "id": "stochastic_ch5",
            "label": "Chapter 5",
            "file": "pages/stochastic_ch5.html"
      },
      {
            "id": "stochastic_ch5_1",
            "label": "5.1",
            "file": "pages/stochastic_ch5_1.html"
      },
      {
            "id": "stochastic_ch5_2",
            "label": "5.2",
            "file": "pages/stochastic_ch5_2.html"
      },
      {
            "id": "stochastic_ch5_3",
            "label": "5.3",
            "file": "pages/stochastic_ch5_3.html"
      },
      {
            "id": "stochastic_ch5_4",
            "label": "5.4",
            "file": "pages/stochastic_ch5_4.html"
      },
      {
            "id": "stochastic_ch5_5",
            "label": "5.5",
            "file": "pages/stochastic_ch5_5.html"
      },
      {
            "id": "stochastic_ch5_6",
            "label": "5.6",
            "file": "pages/stochastic_ch5_6.html"
      },
      {
            "id": "stochastic_ch5_7",
            "label": "5.7",
            "file": "pages/stochastic_ch5_7.html"
      },
      {
            "id": "stochastic_ch5_8",
            "label": "5.8",
            "file": "pages/stochastic_ch5_8.html"
      },
      {
            "id": "stochastic_ch5_9",
            "label": "5.9",
            "file": "pages/stochastic_ch5_9.html"
      },
      {
            "id": "stochastic_ch6",
            "label": "Chapter 6",
            "file": "pages/stochastic_ch6.html"
      },
      {
            "id": "stochastic_ch6_1",
            "label": "6.1",
            "file": "pages/stochastic_ch6_1.html"
      },
      {
            "id": "stochastic_ch6_2",
            "label": "6.2",
            "file": "pages/stochastic_ch6_2.html"
      },
      {
            "id": "stochastic_ch6_3",
            "label": "6.3",
            "file": "pages/stochastic_ch6_3.html"
      },
      {
            "id": "stochastic_ch6_4",
            "label": "6.4",
            "file": "pages/stochastic_ch6_4.html"
      },
      {
            "id": "stochastic_ch6_5",
            "label": "6.5",
            "file": "pages/stochastic_ch6_5.html"
      },
      {
            "id": "stochastic_ch6_6",
            "label": "6.6",
            "file": "pages/stochastic_ch6_6.html"
      },
      {
            "id": "stochastic_ch6_7",
            "label": "6.7",
            "file": "pages/stochastic_ch6_7.html"
      },
      {
            "id": "stochastic_ch6_8",
            "label": "6.8",
            "file": "pages/stochastic_ch6_8.html"
      },
      {
            "id": "stochastic_ch7",
            "label": "Chapter 7",
            "file": "pages/stochastic_ch7.html"
      }
    ]
  },
  {
    id: 'fractal_invariance',
    label: 'Fractal Structural Invariance',
    tabs: [
      { id: 'code', label: 'Code Analysis', file: 'pages/fractal_code.html' },
      { id: 'coherence', label: 'Energy Coherence Analysis', file: 'pages/fractal_coherence.html' },
      { id: 'dynamic', label: 'First Dynamic Patterns Analysis', file: 'pages/fractal_dynamic.html' },
      { id: 'geometric', label: 'Geometric Shape Analysis', file: 'pages/fractal_geometric.html' },
    ]
  },
  {
    id: 'metaqubit_homeostasis',
    label: 'MetaQubit Dynamic Homeostasis',
    tabs: [
      { id: 'code', label: 'Code Analysis', file: 'pages/metaqubit_code.html' },
      { id: 'benchmarking', label: 'Quantum Benchmarking', file: 'pages/metaqubit_benchmarks.html' },
      { id: 'network', label: 'Network Self Organization', file: 'pages/metaqubit_network.html' },
      { id: 'dynamics', label: 'Internal Dynamics', file: 'pages/metaqubit_dynamics.html' },
    ]
  },
  {
    id: 'core_science',
    label: 'Core Science',
    tabs: [
      { id: 'presentation', label: 'Presentation', file: 'pages/core_science.html' },
    ]
  },
];

// ─── State ───────────────────────────────────────────────────────────────────
let currentTopic = TOPICS[0].id;
let currentTab   = 'stochastic_ch1';
const cache = {};

// ─── Render ──────────────────────────────────────────────────────────────────
async function loadContent(file) {
  if (cache[file]) return cache[file];
  try {
    const res = await fetch(file);
    if (!res.ok) throw new Error(res.status);
    const text = await res.text();
    cache[file] = text;
    return cache[file];
  } catch (e) {
    return `<p style="color:#ba1a1a;font-family:monospace;padding:2rem;">Could not load: ${file}</p>`;
  }
}

async function renderContent() {
  const topic = TOPICS.find(t => t.id === currentTopic);
  const tab   = topic.tabs.find(t => t.id === currentTab);
  if (!tab) return;

  const contentEl = document.getElementById('content-body');
  contentEl.innerHTML = '<div class="loading-pulse">Retrieving encrypted data...</div>';
  const html = await loadContent(tab.file);

  const wrapper = document.createElement('div');
  wrapper.className = 'content-inner';
  wrapper.innerHTML = html;

  // Re-execute scripts
  wrapper.querySelectorAll('script').forEach(oldScript => {
    const newScript = document.createElement('script');
    Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
    newScript.textContent = oldScript.textContent;
    oldScript.replaceWith(newScript);
  });

  contentEl.innerHTML = '';
  contentEl.appendChild(wrapper);
  contentEl.scrollTop = 0;

  // Typeset math
  if (window.MathJax) {
    MathJax.typesetPromise([contentEl]).catch((err) => console.log('MathJax error:', err));
  }
}

// ─── Utilities ──────────────────────────────────────────────────────────────
function toggleBenchCollapse(btn) {
  const body = btn.nextElementSibling;
  const icon = btn.querySelector('.bench-collapse-icon');
  const open = body.style.display !== 'none';
  body.style.display = open ? 'none' : 'block';
  icon.textContent   = open ? '▶' : '▼';
}

// ─── Navigation ──────────────────────────────────────────────────────────────
function selectTopic(topicId) {
  currentTopic = topicId;
  const topic  = TOPICS.find(t => t.id === topicId);
  currentTab   = topic.tabs[0].id;

  document.querySelectorAll('.sidebar-item').forEach(el => {
    el.classList.toggle('active', el.dataset.topic === topicId);
  });

  renderTabBar();
  renderContent();
}

function selectTab(tabId) {
  currentTab = tabId;
  document.querySelectorAll('.tab-item').forEach(el => {
    el.classList.toggle('active', el.dataset.tab === tabId);
  });
  renderContent();
}

function renderTabBar() {
  const topic  = TOPICS.find(t => t.id === currentTopic);
  const tabBar = document.getElementById('tab-bar');

  tabBar.innerHTML = topic.tabs.map(tab => {
    const isActive = tab.id === currentTab;
    return `<button class="tab-item ${isActive ? 'active' : ''}" 
                   data-tab="${tab.id}" 
                   onclick="selectTab('${tab.id}')">${tab.label}</button>`;
  }).join('');
}

function buildSidebar() {
  const sidebar = document.getElementById('sidebar-nav');
  sidebar.innerHTML = TOPICS.map(topic => `
    <button class="sidebar-item ${topic.id === currentTopic ? 'active' : ''}"
            data-topic="${topic.id}"
            onclick="selectTopic('${topic.id}')">
      <span class="sidebar-dot"></span>
      <span>${topic.label}</span>
    </button>
  `).join('');
}

// ─── Init ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const topicParam = urlParams.get('topic');
  const tabParam = urlParams.get('tab');
  
  if (topicParam && TOPICS.find(t => t.id === topicParam)) {
    currentTopic = topicParam;
    const topic = TOPICS.find(t => t.id === topicParam);
    if (tabParam && topic.tabs.find(t => t.id === tabParam)) {
      currentTab = tabParam;
    } else {
      currentTab = topic.tabs[0].id;
    }
  }

  buildSidebar();
  renderTabBar();
  renderContent();
});
