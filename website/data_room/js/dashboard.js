/* ── Data Room Logic ── */

const TOPICS = [
  {
    id: 'theory',
    label: 'I. The Theory',
    tabs: [
      { id: 'summary', label: 'Framework Overview', file: '../theory/pillar1_summary.html' },
      { id: 'intro', label: 'From Chaos to Order', file: '../theory/c1_intro.html' },
    ]
  },
  {
    id: 'engine',
    label: 'II. Quantum Engine',
    tabs: [
      { id: 'benchmarks', label: 'MetaQubit Benchmarks', file: '../analysis/pillar2_benchmarks.html' },
      { id: 'dynamics', label: 'Internal Dynamics', file: '../analysis/pillar2_dynamics.html' },
    ]
  },
  {
    id: 'evidence',
    label: 'III. The Evidence',
    tabs: [
      { id: 'geometric', label: 'Geometric Analysis', file: '../analysis/pillar3_geometric.html' },
      { id: 'coherence', label: 'Information Identity', file: '../analysis/pillar3_coherence.html' },
    ]
  }
];

let currentTopicId = TOPICS[0].id;
let currentTabId = TOPICS[0].tabs[0].id;
const cache = {};

async function loadContent(file) {
  if (cache[file]) return cache[file];
  try {
    const res = await fetch(file);
    if (!res.ok) throw new Error(res.status);
    const text = await res.text();
    cache[file] = text;
    return text;
  } catch (e) {
    console.error(e);
    return `<div style="color:var(--error); padding: 2rem;">Error loading content: ${file}</div>`;
  }
}

async function renderContent() {
  const topic = TOPICS.find(t => t.id === currentTopicId);
  const tab = topic.tabs.find(t => t.id === currentTabId);
  const container = document.getElementById('content-body');
  
  container.innerHTML = '<div class="loading-pulse">Retrieving encrypted data...</div>';
  
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
  
  container.innerHTML = '';
  container.appendChild(wrapper);
  container.scrollTop = 0;
}

function selectTopic(topicId) {
  currentTopicId = topicId;
  currentTabId = TOPICS.find(t => t.id === topicId).tabs[0].id;
  
  document.querySelectorAll('.sidebar-item').forEach(el => {
    el.classList.toggle('active', el.dataset.topic === topicId);
  });
  
  renderTabBar();
  renderContent();
}

function selectTab(tabId) {
  currentTabId = tabId;
  document.querySelectorAll('.tab-item').forEach(el => {
    el.classList.toggle('active', el.dataset.tab === tabId);
  });
  renderContent();
}

function renderTabBar() {
  const topic = TOPICS.find(t => t.id === currentTopicId);
  const tabBar = document.getElementById('tab-bar');
  
  tabBar.innerHTML = topic.tabs.map(tab => `
    <button class="tab-item ${tab.id === currentTabId ? 'active' : ''}" 
            data-tab="${tab.id}" 
            onclick="selectTab('${tab.id}')">
      ${tab.label}
    </button>
  `).join('');
}

function buildSidebar() {
  const nav = document.getElementById('sidebar-nav');
  nav.innerHTML = TOPICS.map(topic => `
    <button class="sidebar-item ${topic.id === currentTopicId ? 'active' : ''}" 
            data-topic="${topic.id}"
            onclick="selectTopic('${topic.id}')">
      <span class="sidebar-dot"></span>
      <span>${topic.label}</span>
    </button>
  `).join('');
}

document.addEventListener('DOMContentLoaded', () => {
  buildSidebar();
  renderTabBar();
  renderContent();
});
