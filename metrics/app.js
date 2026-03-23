let trendChart;
let repoChart;
let detailTrendChart;
let dashboardData = [];
let currentRepo = null;
let currentScope = "all";

async function loadJson(path) {
  const res = await fetch(path, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to load ${path}`);
  return res.json();
}

function requireEl(id) {
  const el = document.getElementById(id);
  if (!el) throw new Error(`Missing required element: #${id}`);
  return el;
}

function shortRepo(repo) {
  return repo.split("/").pop();
}

function safeDate(value) {
  return value ? value.slice(0, 10) : "";
}

function parseIso(value) {
  return value ? new Date(value) : null;
}

function daysAgo(days) {
  const d = new Date();
  d.setUTCDate(d.getUTCDate() - days);
  return d;
}

function getLatestMap(history) {
  const repos = history.repos || {};
  const latest = {};

  for (const [repo, entries] of Object.entries(repos)) {
    if (entries.length) latest[repo] = entries[entries.length - 1];
  }
  return latest;
}

function buildCombinedState(history, details) {
  const latestMap = getLatestMap(history);
  const detailRepos = details.repositories || [];

  return detailRepos.map(repoItem => {
    const latestHistory = latestMap[repoItem.repo] || null;
    return {
      ...repoItem,
      history: history.repos?.[repoItem.repo] || [],
      latestHistory
    };
  });
}

function destroyChart(chart) {
  if (chart) chart.destroy();
}

function baseChartOptions(yTitle) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: { color: "#d9e3f5" }
      }
    },
    scales: {
      x: {
        ticks: { color: "#9fb0cd" },
        grid: { color: "rgba(255,255,255,0.06)" }
      },
      y: {
        ticks: { color: "#9fb0cd" },
        grid: { color: "rgba(255,255,255,0.06)" },
        title: {
          display: true,
          text: yTitle,
          color: "#9fb0cd"
        }
      }
    }
  };
}

function itemFirstSeenDate(item) {
  if (!item.history?.length) return null;
  const sorted = [...item.history].sort(
    (a, b) => new Date(a.latest_run_created_at) - new Date(b.latest_run_created_at)
  );
  return parseIso(sorted[0].latest_run_created_at);
}

function isRecentRepo(item, days = 60) {
  const firstSeen = itemFirstSeenDate(item);
  if (!firstSeen) return false;
  return firstSeen >= daysAgo(days);
}

function applyScopeToRepo(item, scope) {
  if (scope === "all") return item;

  if (scope === "recent60") {
    if (!isRecentRepo(item, 60)) return null;

    return {
      ...item,
      history: item.history.filter(h => parseIso(h.latest_run_created_at) >= daysAgo(60))
    };
  }

  if (scope === "newOnly") {
    if (item.summary.new_failures <= 0) return null;

    return {
      ...item,
      details: {
        ...item.details,
        resolved_failures: [],
        consistent_failures: [],
        only_in_latest: [],
        only_in_previous: [],
        changed_other: []
      }
    };
  }

  return item;
}

function getScopedData(data, scope) {
  return data
    .map(item => applyScopeToRepo(item, scope))
    .filter(Boolean);
}

function renderKpis(data, errorsCount) {
  const latest = data.map(d => d.summary);
  const totalFailures = latest.reduce((a, r) => a + r.fail_latest, 0);
  const totalNew = latest.reduce((a, r) => a + r.new_failures, 0);
  const totalResolved = latest.reduce((a, r) => a + r.resolved_failures, 0);
  const totalConsistent = latest.reduce((a, r) => a + r.consistent_failures, 0);
  const failingRepos = data.filter(d => d.summary.fail_latest > 0).length;

  const kpis = [
    ["Monitored Repos", data.length, `${failingRepos} currently failing`],
    ["Total Failures", totalFailures, "Current latest-run failures"],
    ["New Failures", totalNew, "Regressions from previous run"],
    ["Resolved", totalResolved, "Fixed since previous run"],
    ["Consistent Failures", totalConsistent, `${errorsCount} fetch/report error(s)`],
  ];

  const container = requireEl("kpis");
  container.innerHTML = "";

  for (const [label, value, sub] of kpis) {
    const el = document.createElement("div");
    el.className = "kpi";
    el.innerHTML = `
      <div class="kpi-label">${label}</div>
      <div class="kpi-value">${value}</div>
      <div class="kpi-sub">${sub}</div>
    `;
    container.appendChild(el);
  }
}

function renderRepoNav(data, filter = "") {
  const nav = requireEl("repoNav");
  nav.innerHTML = "";

  const filtered = data
    .filter(d => d.repo.toLowerCase().includes(filter.toLowerCase()))
    .sort((a, b) => b.summary.fail_latest - a.summary.fail_latest || a.repo.localeCompare(b.repo));

  for (const item of filtered) {
    const btn = document.createElement("button");
    btn.className = "repo-nav-button";
    btn.dataset.repo = item.repo;
    btn.innerHTML = `
      <div class="repo-nav-top">
        <div class="repo-short">${shortRepo(item.repo)}</div>
        <span class="badge ${item.summary.fail_latest > 0 ? "red" : "green"}">${item.summary.fail_latest}</span>
      </div>
      <div class="repo-full">${item.repo}</div>
    `;
    btn.addEventListener("click", () => showRepoView(item.repo));
    nav.appendChild(btn);
  }

  updateSidebarSelection();
}

function renderRepoTable(data) {
  const tbody = requireEl("repoTable").querySelector("tbody");
  tbody.innerHTML = "";

  const sorted = [...data].sort((a, b) =>
    b.summary.fail_latest - a.summary.fail_latest ||
    b.summary.new_failures - a.summary.new_failures
  );

  for (const item of sorted) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><a href="#" data-repo-link="${item.repo}">${item.repo}</a></td>
      <td><span class="badge ${item.summary.fail_latest > 0 ? "red" : "green"}">${item.summary.fail_latest}</span></td>
      <td>${item.summary.new_failures}</td>
      <td>${item.summary.resolved_failures}</td>
      <td>${item.summary.consistent_failures}</td>
      <td><a href="${item.latest_run.url}" target="_blank" rel="noopener">#${item.latest_run.number}</a></td>
    `;
    tbody.appendChild(tr);
  }

  tbody.querySelectorAll("[data-repo-link]").forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      showRepoView(e.target.dataset.repoLink);
    });
  });
}

function renderErrors(errors) {
  const wrap = requireEl("errorList");
  wrap.innerHTML = "";

  if (!errors?.length) {
    wrap.innerHTML = `<div class="muted">No repo-level errors in this run.</div>`;
    return;
  }

  for (const err of errors) {
    const div = document.createElement("div");
    div.className = "error-item";
    div.textContent = err;
    wrap.appendChild(div);
  }
}

function renderTrendChart(data) {
  const dateSet = new Set();
  data.forEach(repo => repo.history.forEach(entry => dateSet.add(safeDate(entry.latest_run_created_at))));
  const labels = [...dateSet].sort();

  const totals = labels.map(date => {
    let total = 0;
    for (const repo of data) {
      const match = repo.history.find(h => safeDate(h.latest_run_created_at) === date);
      if (match) total += match.fail_latest;
    }
    return total;
  });

  destroyChart(trendChart);
  trendChart = new Chart(requireEl("trendChart"), {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Total Failures",
        data: totals,
        tension: 0.25,
        borderWidth: 2,
        fill: true,
        backgroundColor: "rgba(110,168,254,0.14)",
        borderColor: "rgba(110,168,254,1)",
        pointRadius: 3,
      }]
    },
    options: baseChartOptions("Failures")
  });
}

function renderRepoChart(data) {
  const sorted = [...data].sort((a, b) => b.summary.fail_latest - a.summary.fail_latest);

  destroyChart(repoChart);
  repoChart = new Chart(requireEl("repoChart"), {
    type: "bar",
    data: {
      labels: sorted.map(x => shortRepo(x.repo)),
      datasets: [{
        label: "Latest Failures",
        data: sorted.map(x => x.summary.fail_latest),
        backgroundColor: sorted.map(x =>
          x.summary.fail_latest > 0 ? "rgba(255,107,107,0.7)" : "rgba(77,212,172,0.65)"
        )
      }]
    },
    options: {
      ...baseChartOptions("Failures"),
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
    }
  });
}

function statCard(label, value, colorClass = "blue") {
  return `
    <div class="stat-card">
      <div class="label">${label}</div>
      <div class="value"><span class="badge ${colorClass}">${value}</span></div>
    </div>
  `;
}

function pathList(items, badgeClass = "blue", badgeTextFn = null, searchTerm = "") {
  const lower = searchTerm.toLowerCase();
  const filtered = items.filter(item => {
    const text = typeof item === "string" ? item : item.notebook;
    return text.toLowerCase().includes(lower);
  });

  if (!filtered.length) return `<div class="muted">None</div>`;

  return `
    <div class="path-list">
      ${filtered.map(item => {
        const path = typeof item === "string" ? item : item.notebook;
        const badgeText = badgeTextFn ? badgeTextFn(item) : "";
        return `
          <div class="path-item">
            <code>${path}</code>
            ${badgeText ? `<span class="badge ${badgeClass}">${badgeText}</span>` : ""}
          </div>
        `;
      }).join("")}
    </div>
  `;
}

function renderDetailTrend(item) {
  const labels = item.history.map(h => safeDate(h.latest_run_created_at));
  const values = item.history.map(h => h.fail_latest);

  destroyChart(detailTrendChart);
  detailTrendChart = new Chart(requireEl("detailTrendChart"), {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: shortRepo(item.repo),
        data: values,
        tension: 0.25,
        borderWidth: 2,
        fill: true,
        backgroundColor: "rgba(77,212,172,0.14)",
        borderColor: "rgba(77,212,172,1)",
        pointRadius: 3,
      }]
    },
    options: baseChartOptions("Failures")
  });
}

function renderDetailSections(item, searchTerm = "") {
  const d = item.details;
  const container = requireEl("detailSections");

  const sections = [
    {
      title: "New Failures",
      count: d.new_failures.length,
      body: pathList(d.new_failures, "red", () => "New", searchTerm)
    },
    {
      title: "Resolved Failures",
      count: d.resolved_failures.length,
      body: pathList(d.resolved_failures, "green", () => "Fixed", searchTerm)
    },
    {
      title: "Consistent Failures",
      count: d.consistent_failures.length,
      body: pathList(d.consistent_failures, "yellow", () => "Ongoing", searchTerm)
    },
    {
      title: "Only in Latest Run",
      count: d.only_in_latest.length,
      body: pathList(d.only_in_latest, "blue", x => x.conclusion, searchTerm)
    },
    {
      title: "Only in Previous Run",
      count: d.only_in_previous.length,
      body: pathList(d.only_in_previous, "blue", x => x.conclusion, searchTerm)
    },
    {
      title: "Other Status Changes",
      count: d.changed_other.length,
      body: d.changed_other.length
        ? `
          <div class="path-list">
            ${d.changed_other
              .filter(x => x.notebook.toLowerCase().includes(searchTerm.toLowerCase()))
              .map(x => `
                <div class="path-item">
                  <code>${x.notebook}</code>
                  <span class="badge blue">${x.previous} → ${x.current}</span>
                </div>
              `).join("")}
          </div>
        `
        : `<div class="muted">None</div>`
    }
  ];

  container.innerHTML = sections.map(section => `
    <section class="detail-block">
      <div class="detail-block-header">
        <h4>${section.title}</h4>
        <span class="badge blue">${section.count}</span>
      </div>
      <div class="detail-block-body">${section.body}</div>
    </section>
  `).join("");
}

function updateSidebarSelection() {
  const overviewBtn = requireEl("showOverviewBtn");
  overviewBtn.classList.toggle("active", currentRepo === null);

  document.querySelectorAll(".repo-nav-button[data-repo]").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.repo === currentRepo);
  });

  document.querySelectorAll(".toggle-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.scope === currentScope);
  });
}

function showOverviewView() {
  currentRepo = null;
  requireEl("overviewView").classList.remove("hidden");
  requireEl("repoView").classList.add("hidden");
  requireEl("pageTitle").textContent = `Cross-Repo CI Health · ${scopeLabel(currentScope)}`;
  updateSidebarSelection();
}

function showRepoView(repoName) {
  const scoped = getScopedData(dashboardData, currentScope);
  const item = scoped.find(d => d.repo === repoName);
  if (!item) return;

  currentRepo = repoName;

  requireEl("overviewView").classList.add("hidden");
  requireEl("repoView").classList.remove("hidden");
  requireEl("pageTitle").textContent = `${item.repo} · ${scopeLabel(currentScope)}`;

  requireEl("detailTitle").textContent = item.repo;
  requireEl("detailSubtitle").textContent =
    `Latest run #${item.latest_run.number} vs previous run #${item.previous_run.number}`;

  requireEl("detailStats").innerHTML = `
    ${statCard("Failures", item.summary.fail_latest, item.summary.fail_latest > 0 ? "red" : "green")}
    ${statCard("New", item.summary.new_failures, item.summary.new_failures > 0 ? "red" : "blue")}
    ${statCard("Resolved", item.summary.resolved_failures, item.summary.resolved_failures > 0 ? "green" : "blue")}
    ${statCard("Consistent", item.summary.consistent_failures, item.summary.consistent_failures > 0 ? "yellow" : "blue")}
  `;

  requireEl("detailLinks").innerHTML = `
    <a class="button ghost" href="${item.latest_run.url}" target="_blank" rel="noopener">Latest run #${item.latest_run.number}</a>
    <a class="button ghost" href="${item.previous_run.url}" target="_blank" rel="noopener">Previous run #${item.previous_run.number}</a>
  `;

  renderDetailTrend(item);
  renderDetailSections(item, requireEl("notebookSearch").value || "");
  updateSidebarSelection();
}

function scopeLabel(scope) {
  if (scope === "recent60") return "Last 60 Days";
  if (scope === "newOnly") return "New Only";
  return "All";
}

function rerender() {
  const scoped = getScopedData(dashboardData, currentScope);
  const repoFilter = requireEl("repoSearch").value || "";

  renderKpis(scoped, 0);
  renderRepoNav(scoped, repoFilter);
  renderRepoTable(scoped);
  renderTrendChart(scoped);
  renderRepoChart(scoped);

  if (currentRepo && scoped.some(x => x.repo === currentRepo)) {
    showRepoView(currentRepo);
  } else {
    showOverviewView();
  }
}

function wireScopeToggle() {
  document.querySelectorAll(".toggle-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      currentScope = btn.dataset.scope;
      rerender();
    });
  });
}

async function init() {
  const [history, details] = await Promise.all([
    loadJson("./history.json"),
    loadJson("./details.json")
  ]);

  requireEl("lastUpdated").textContent =
    `Last updated ${details.generated_at || history.generated_at || "unknown"} · Workflow: ${details.workflow_name || history.workflow_name || "unknown"}`;

  dashboardData = buildCombinedState(history, details);

  renderErrors(details.errors || []);
  wireScopeToggle();

  requireEl("showOverviewBtn").addEventListener("click", showOverviewView);

  requireEl("repoSearch").addEventListener("input", () => {
    rerender();
  });

  requireEl("notebookSearch").addEventListener("input", () => {
    if (currentRepo) showRepoView(currentRepo);
  });

  rerender();
}

init().catch(err => {
  console.error(err);
  const lastUpdated = document.getElementById("lastUpdated");
  if (lastUpdated) {
    lastUpdated.textContent = `Failed to load dashboard data: ${err.message}`;
  }
});
