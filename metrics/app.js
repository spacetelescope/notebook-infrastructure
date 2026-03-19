async function loadData() {
  const res = await fetch("./history.json");
  return await res.json();
}

function getLatestEntries(history) {
  const repos = history.repos || {};
  const latest = [];

  for (const repo in repos) {
    const entries = repos[repo];
    if (entries.length > 0) {
      latest.push({
        repo,
        ...entries[entries.length - 1]
      });
    }
  }

  return latest;
}

function updateSummary(latest) {
  const totalFailures = latest.reduce((a, r) => a + r.fail_latest, 0);
  const newFailures = latest.reduce((a, r) => a + r.new_failures, 0);
  const resolved = latest.reduce((a, r) => a + r.resolved_failures, 0);

  document.getElementById("total-failures").textContent = totalFailures;
  document.getElementById("new-failures").textContent = newFailures;
  document.getElementById("resolved-failures").textContent = resolved;
}

function renderRepoTable(latest) {
  const tbody = document.querySelector("#repoTable tbody");
  tbody.innerHTML = "";

  latest.sort((a, b) => b.fail_latest - a.fail_latest);

  for (const r of latest) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${r.repo}</td>
      <td>${r.fail_latest}</td>
      <td>${r.new_failures}</td>
      <td>${r.resolved_failures}</td>
    `;
    tbody.appendChild(tr);
  }
}

function renderRepoChart(latest) {
  const ctx = document.getElementById("repoChart");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: latest.map(r => r.repo.split("/")[1]),
      datasets: [{
        label: "Failures",
        data: latest.map(r => r.fail_latest)
      }]
    }
  });
}

function renderTrendChart(history) {
  const repos = history.repos || {};
  const dates = new Set();

  for (const repo in repos) {
    repos[repo].forEach(e => dates.add(e.latest_run_created_at.slice(0,10)));
  }

  const sortedDates = Array.from(dates).sort();

  const totals = sortedDates.map(date => {
    let sum = 0;
    for (const repo in repos) {
      const entry = repos[repo].find(e =>
        e.latest_run_created_at.startsWith(date)
      );
      if (entry) sum += entry.fail_latest;
    }
    return sum;
  });

  new Chart(document.getElementById("trendChart"), {
    type: "line",
    data: {
      labels: sortedDates,
      datasets: [{
        label: "Total Failures",
        data: totals,
        fill: false
      }]
    }
  });
}

async function init() {
  const history = await loadData();

  document.getElementById("last-updated").textContent =
    "Last updated: " + history.generated_at;

  const latest = getLatestEntries(history);

  updateSummary(latest);
  renderRepoTable(latest);
  renderRepoChart(latest);
  renderTrendChart(history);
}

init();
