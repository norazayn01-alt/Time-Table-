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
        <h1 className="page-title">Dashboard <span>↗</span></h1>
      </div>
      <div className="stats-row">
        <StatCard icon="👨‍🏫" label="O'qituvchilar" value={stats.teachers} color="var(--accent)" />
        <StatCard icon="🏛️" label="Xonalar" value={stats.rooms} color="var(--accent3)" />
        <StatCard icon="👥" label="Guruhlar" value={stats.groups} color="var(--accent4)" />
        <StatCard icon="📅" label="Darslar" value={stats.timetable} color="var(--accent2)" />
      </div>
      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: 32, textAlign: 'center' }}>
        <div style={{ fontSize: 48, marginBottom: 12 }}>🎓</div>
        <div style={{ fontFamily: "'Syne', sans-serif", fontSize: 20, fontWeight: 800, marginBottom: 8 }}>Xush kelibsiz!</div>
        <div style={{ color: 'var(--text-muted)', fontSize: 14 }}>Yuqoridagi menyu orqali bo'limlarga o'ting</div>
      </div>
    </div>
  );
}
