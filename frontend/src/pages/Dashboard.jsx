import { useState, useEffect } from 'react';
import { apiFetch } from '../api';
import StatCard from '../components/StatCard';

export default function Dashboard() {
  const [stats, setStats] = useState({ teachers: 0, rooms: 0, groups: 0, timetable: 0 });

  useEffect(() => {
    loadStats();
  }, []);

  async function loadStats() {
    try {
      const [teachers, rooms, groups, timetable] = await Promise.all([
        apiFetch('/teachers/'),
        apiFetch('/rooms/'),
        apiFetch('/groups/'),
        apiFetch('/timetable/'),
      ]);
      setStats({
        teachers: teachers?.length || 0,
        rooms: rooms?.length || 0,
        groups: groups?.length || 0,
        timetable: timetable?.length || 0,
      });
    } catch (_) {}
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
      </div>
      <div className="stats-row">
        <StatCard
          icon={<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>}
          label="O'qituvchilar"
          value={stats.teachers}
          color="var(--accent)"
        />
        <StatCard
          icon={<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>}
          label="Xonalar"
          value={stats.rooms}
          color="var(--accent3)"
        />
        <StatCard
          icon={<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>}
          label="Guruhlar"
          value={stats.groups}
          color="var(--accent4)"
        />
        <StatCard
          icon={<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>}
          label="Darslar"
          value={stats.timetable}
          color="var(--accent2)"
        />
      </div>
      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: 32, textAlign: 'center' }}>
        <div style={{ fontFamily: "'Syne', sans-serif", fontSize: 20, fontWeight: 800, marginBottom: 8 }}>Xush kelibsiz!</div>
        <div style={{ color: 'var(--text-muted)', fontSize: 14 }}>Yuqoridagi menyu orqali bo'limlarga o'ting</div>
      </div>
    </div>
  );
}
