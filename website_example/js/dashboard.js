// ─── Content Map ────────────────────────────────────────────────────────────
const TOPICS = [
  {
    id: 'organicflow',
    label: 'OrganicFlow',
    tabs: [
      { id: 'whitepaper', label: 'White Paper', file: 'pages/organicflow_whitepaper.html' },
      { id: 'bench1',  label: 'Bench 1',  file: 'pages/organicflow_bench1.html' },
      { id: 'bench2',  label: 'Bench 2',  file: 'pages/organicflow_bench2.html' },
      { id: 'bench3',  label: 'Bench 3',  file: 'pages/organicflow_bench3.html' },
      { id: 'bench4',  label: 'Bench 4',  file: 'pages/organicflow_bench4.html' },
      { id: 'bench5',  label: 'Bench 5',  file: 'pages/organicflow_bench5.html' },
      { id: 'bench6',  label: 'Bench 6',  file: 'pages/organicflow_bench6.html' },
      { id: 'bench7',  label: 'Bench 7',  file: 'pages/organicflow_bench7.html' },
      { id: 'bench8',  label: 'Bench 8',  file: 'pages/organicflow_bench8.html' },
      { id: 'bench9',  label: 'Bench 9',  file: 'pages/organicflow_bench9.html' },
      { id: 'bench10', label: 'Bench 10', file: 'pages/organicflow_bench10.html' },
      { id: 'bench11', label: 'Bench 11', file: 'pages/organicflow_bench11.html' },
      { id: 'bench12', label: 'Bench 12', file: 'pages/organicflow_bench12.html' },
      { id: 'bench13', label: 'Bench 13', file: 'pages/organicflow_bench13.html' },
      { id: 'bench14', label: 'Bench 14', file: 'pages/organicflow_bench14.html' },
    ]
  },
  {
    id: 'organiccloud',
    label: 'OrganicCloud',
    tabs: [
      { id: 'whitepaper',            label: 'White Paper',          file: 'pages/organiccloud_whitepaper.html' },
      { id: 'basic_tests',           label: 'Basic Tests',          file: 'pages/organiccloud_basic.html' },
      { id: 'adv_resilience',        label: 'Resilience & Faults',  file: 'pages/organiccloud_advanced_resilience.html' },
      { id: 'adv_autonomic',         label: 'Autonomic Systems',    file: 'pages/organiccloud_advanced_autonomic.html' },
      { id: 'adv_runtime',           label: 'Runtime & Memory',     file: 'pages/organiccloud_advanced_runtime.html' },
    ]
  },
  {
    id: 'organicllm',
    label: 'LLM Convertor',
    tabs: [
      { id: 'whitepaper',   label: 'White Paper',   file: 'pages/organicllm_whitepaper.html' },
      { id: 'basic_tests',  label: 'Basic Tests',   file: 'pages/organicllm_basic.html' },
      { id: 'advance_test', label: 'Advanced Test', file: 'pages/organicllm_advanced.html' },
    ]
  },
];

// ─── State ───────────────────────────────────────────────────────────────────
let currentTopic = TOPICS[0].id;
let currentTab   = TOPICS[0].tabs[0].id;
const cache = {};

// ─── Collapsible (used by pages) ─────────────────────────────────────────────
function toggleCollapse(btn) {
  const body = btn.closest('.collapse-trigger, .code-block-wrapper').querySelector('.collapse-body');
  const icon = btn.querySelector('.collapse-icon');
  const open = body.style.display !== 'none';
  body.style.display = open ? 'none' : 'block';
  icon.textContent = open ? '▶' : '▼';
}

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
  contentEl.innerHTML = '<div class="loading-pulse">Loading…</div>';
  const html = await loadContent(tab.file);

  // Inject HTML — re-execute style and script tags manually
  const wrapper = document.createElement('div');
  wrapper.className = 'content-inner';
  wrapper.innerHTML = html;

  // Re-execute <script> tags (innerHTML doesn't run them)
  wrapper.querySelectorAll('script').forEach(oldScript => {
    const newScript = document.createElement('script');
    Array.from(oldScript.attributes).forEach(attr => {
      newScript.setAttribute(attr.name, attr.value);
    });
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

  // Sidebar active state
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
    const isFirst = tab.id === 'whitepaper';
    const cls = `tab-item${tab.id === currentTab ? ' active' : ''}${isFirst ? ' tab-whitepaper' : ''}`;
    return `<button class="${cls}" data-tab="${tab.id}" onclick="selectTab('${tab.id}')">${tab.label}</button>`;
  }).join('');
}

// ─── Sidebar Build ────────────────────────────────────────────────────────────
function buildSidebar() {
  const sidebar = document.getElementById('sidebar-nav');
  sidebar.innerHTML = TOPICS.map(topic => `
    <button class="sidebar-item${topic.id === currentTopic ? ' active' : ''}"
            data-topic="${topic.id}"
            onclick="selectTopic('${topic.id}')">
      <span class="sidebar-dot"></span>
      <span>${topic.label}</span>
    </button>
  `).join('');
}

// ─── Init ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  buildSidebar();
  renderTabBar();
  renderContent();
});
