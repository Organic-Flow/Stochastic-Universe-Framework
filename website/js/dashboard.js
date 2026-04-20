// ─── Content Map ────────────────────────────────────────────────────────────
const TOPICS = [
  {
    id: 'stochastic_universe',
    label: 'Stochastic Universe',
    tabs: [
      { id: 'book', label: 'Book', file: 'pages/stochastic_book.html' },
      { id: 'ch1',  label: 'Chapter 1',  file: 'pages/stochastic_ch1.html' },
      { id: 'ch1_1', label: '1.1', file: 'pages/stochastic_ch1_1.html' },
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
];

// ─── State ───────────────────────────────────────────────────────────────────
let currentTopic = TOPICS[0].id;
let currentTab   = TOPICS[0].tabs[0].id;
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
