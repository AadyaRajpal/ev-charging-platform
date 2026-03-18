const API_BASE = 'http://10.20.86.66:8000';

export async function fetchStations({ lat, lng, radius = 10, maxResults = 20 }) {
  const url = `${API_BASE}/stations?lat=${lat}&lng=${lng}&radius=${radius}&max_results=${maxResults}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  const data = await res.json();
  return data.stations;
}