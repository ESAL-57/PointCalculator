const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

async function requestApi(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || `API request failed: ${response.status}`);
  }

  return data;
}

export function getStatus() {
  return requestApi("/api/status/");
}

export function getOptions() {
  return requestApi("/api/options/");
}

export function calculateTeam(players) {
  return requestApi("/api/calculate/", {
    method: "POST",
    body: JSON.stringify({ players }),
  });
}

export function calculatePlayer(player) {
  return requestApi("/api/calculate-player/", {
    method: "POST",
    body: JSON.stringify({ player }),
  });
}

export function crawlPlayer(gameName, tagLine) {
  const params = new URLSearchParams({ gameName, tagLine });
  return requestApi(`/api/crawl/player/?${params.toString()}`);
}
