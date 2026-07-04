import { useState, useEffect } from 'react';
import { apiFetch } from '../api';

export default function Sidebar({ activePage, onNavigate }) {
  const [counts, setCounts] = useState({ teachers: 0, rooms: 0, groups: 0 });

  useEffect(() => {
    loadCounts();
  }, [activePage]);

  async function loadCounts() {
    try {
      const [teachers, rooms, groups] = await Promise.all([
        apiFetch('/teachers/'),
        apiFetch('/rooms/'),
        apiFetch('/groups/'),
      ]);
      setCounts({
        teachers: teachers?.length || 0,
        rooms: rooms?.length || 0,
        groups: groups?.length || 0,
      });
    } catch (_) {}
  }

  const items = [
    { key: 'dashboard', icon: '📊', label: 'Dashboard' },
    { key: 'teachers', icon: '👨‍🏫', label: "O'qituvchilar", badge: counts.teachers, badgeStyle: {} },
    { key: 'rooms', icon: '🏛️', label: 'Xonalar', badge: counts.rooms, badgeStyle: { background: 'var(--accent3)', color: '#0f0e17' } },
    { key: 'groups', icon: '👥', label: 'Guruhlar', badge: counts.groups, badgeStyle: { background: 'var(--accent4)', color: '#0f0e17' } },
    { key: 'timetable', icon: '📅', label: 'Jadval' },
  ];

  return (
    <aside className="sidebar">
      <div className="logo">TimeTable</div>
      <div className="logo-sub">Boshqaruv Tizimi</div>
      <nav>
        {items.map((item) => (
          <div
            key={item.key}
            className={`nav-item ${activePage === item.key ? 'active' : ''}`}
            onClick={() => onNavigate(item.key)}
          >
            <span className="nav-icon">{item.icon}</span>
            {item.label}
            {item.badge !== undefined && (
              <span className="nav-badge" style={item.badgeStyle || {}}>
                {item.badge}
              </span>
            )}
          </div>
        ))}
      </nav>
    </aside>
  );
}
