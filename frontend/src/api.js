const API = '/api/v1';

export async function apiFetch(url, options = {}) {
  const res = await fetch(API + url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Server xatosi' }));
    throw new Error(err.detail || 'Xato yuz berdi');
  }
  return res.status === 204 ? null : res.json();
}
