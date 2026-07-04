import { useState, useEffect, useCallback, useMemo } from 'react';
import { apiFetch } from '../api';
import { DAYS, DAY_COLORS, STD_SLOTS } from '../constants';
import Modal from '../components/Modal';
import EmptyState from '../components/EmptyState';

export default function Timetable({ showToast }) {
  const [ttData, setTtData] = useState([]);
  const [teachersList, setTeachersList] = useState([]);
  const [roomsList, setRoomsList] = useState([]);
  const [groupsList, setGroupsList] = useState([]);
  const [view, setView] = useState('grid');
  const [modalOpen, setModalOpen] = useState(false);
  const [editId, setEditId] = useState(null);
  const [form, setForm] = useState({ subject: '', teacher_id: '', room_id: '', group_id: '', day_of_week: '1', start_time: '08:00', end_time: '09:30' });

  // Filters
  const [fSubject, setFSubject] = useState('');
  const [fTeacher, setFTeacher] = useState('');
  const [fRoom, setFRoom] = useState('');
  const [fGroup, setFGroup] = useState('');

  const load = useCallback(async () => {
    try {
      const [data, teachers, rooms, groups] = await Promise.all([
        apiFetch('/timetable/'),
        apiFetch('/teachers/'),
        apiFetch('/rooms/'),
        apiFetch('/groups/'),
      ]);
      setTtData(data || []);
      setTeachersList(teachers || []);
      setRoomsList(rooms || []);
      setGroupsList(groups || []);
    } catch (_) {}
  }, []);

  useEffect(() => { load(); }, [load]);

  const maps = useMemo(() => ({
    tMap: Object.fromEntries(teachersList.map(t => [t.id, t.full_name])),
    rMap: Object.fromEntries(roomsList.map(r => [r.id, r.name])),
    gMap: Object.fromEntries(groupsList.map(g => [g.id, g.name])),
  }), [teachersList, roomsList, groupsList]);

  const filtered = useMemo(() => {
    const subj = fSubject.trim().toLowerCase();
    return ttData.filter(e =>
      (!subj || e.subject.toLowerCase().includes(subj)) &&
      (!fTeacher || String(e.teacher_id) === fTeacher) &&
      (!fRoom || String(e.room_id) === fRoom) &&
      (!fGroup || String(e.group_id) === fGroup)
    );
  }, [ttData, fSubject, fTeacher, fRoom, fGroup]);

  function clearFilters() {
    setFSubject('');
    setFTeacher('');
    setFRoom('');
    setFGroup('');
  }

  function openAdd() {
    setEditId(null);
    setForm({
      subject: '',
      teacher_id: teachersList[0]?.id || '',
      room_id: roomsList[0]?.id || '',
      group_id: groupsList[0]?.id || '',
      day_of_week: '1',
      start_time: '08:00',
      end_time: '09:30',
    });
    setModalOpen(true);
  }

  async function openEdit(id) {
    try {
      const t = await apiFetch('/timetable/' + id);
      if (!t) return;
      setEditId(id);
      setForm({
        subject: t.subject,
        teacher_id: t.teacher_id,
        room_id: t.room_id,
        group_id: t.group_id,
        day_of_week: String(t.day_of_week),
        start_time: t.start_time.slice(0, 5),
        end_time: t.end_time.slice(0, 5),
      });
      setModalOpen(true);
    } catch (_) {}
  }

  async function save() {
    const body = {
      subject: form.subject.trim(),
      teacher_id: parseInt(form.teacher_id),
      room_id: parseInt(form.room_id),
      group_id: parseInt(form.group_id),
      day_of_week: parseInt(form.day_of_week),
      start_time: form.start_time + ':00',
      end_time: form.end_time + ':00',
    };
    if (!body.subject) {
      showToast('Fan nomi majburiy!', 'error');
      return;
    }
    try {
      if (editId) {
        await apiFetch('/timetable/' + editId, { method: 'PUT', body: JSON.stringify(body) });
        showToast('Dars yangilandi!');
      } else {
        await apiFetch('/timetable/', { method: 'POST', body: JSON.stringify(body) });
        showToast("Dars jadvalga qo'shildi!");
      }
      setModalOpen(false);
      load();
    } catch (_) {}
  }

  async function remove(id) {
    if (!confirm("O'chirishni tasdiqlaysizmi?")) return;
    try {
      await apiFetch('/timetable/' + id, { method: 'DELETE' });
      showToast("Dars o'chirildi");
      load();
    } catch (_) {}
  }

  // Build grid slots
  const gridSlots = useMemo(() => {
    const slots = STD_SLOTS.map(s => ({ ...s }));
    const stdStarts = new Set(slots.map(s => s.start));
    filtered.forEach(d => {
      const st = d.start_time.slice(0, 5);
      const en = d.end_time.slice(0, 5);
      if (!stdStarts.has(st)) {
        slots.push({ n: '', start: st, end: en });
        stdStarts.add(st);
      }
    });
    slots.sort((a, b) => a.start.localeCompare(b.start));
    return slots;
  }, [filtered]);

  // Cell map for grid
  const cellMap = useMemo(() => {
    const cm = {};
    [1, 2, 3, 4, 5, 6].forEach(d => { cm[d] = {}; });
    filtered.forEach(lesson => {
      const d = lesson.day_of_week;
      const st = lesson.start_time.slice(0, 5);
      if (!cm[d]) cm[d] = {};
      if (!cm[d][st]) cm[d][st] = [];
      cm[d][st].push(lesson);
    });
    return cm;
  }, [filtered]);

  const allDays = [1, 2, 3, 4, 5, 6];

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Dars Jadvali <span>📅</span></h1>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <button className={`view-toggle-btn ${view === 'grid' ? 'active' : ''}`} onClick={() => setView('grid')}>🗓 Jadval</button>
          <button className={`view-toggle-btn ${view === 'list' ? 'active' : ''}`} onClick={() => setView('list')}>📋 Ro'yxat</button>
          <button className="btn btn-primary" onClick={openAdd} style={{ background: 'linear-gradient(135deg,var(--accent2),#6d28d9)' }}>+ Dars qo'shish</button>
        </div>
      </div>

      {/* Filters */}
      <div className="filter-bar">
        <div className="filter-item">
          <label className="filter-label">🔍 Fan bo'yicha</label>
          <input className="form-input" value={fSubject} onChange={(e) => setFSubject(e.target.value)} placeholder="Fan nomi..." />
        </div>
        <div className="filter-item">
          <label className="filter-label">👨‍🏫 O'qituvchi</label>
          <select className="form-select" value={fTeacher} onChange={(e) => setFTeacher(e.target.value)}>
            <option value="">Barchasi</option>
            {teachersList.map(t => <option key={t.id} value={t.id}>{t.full_name}</option>)}
          </select>
        </div>
        <div className="filter-item">
          <label className="filter-label">🏛️ Xona</label>
          <select className="form-select" value={fRoom} onChange={(e) => setFRoom(e.target.value)}>
            <option value="">Barchasi</option>
            {roomsList.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
          </select>
        </div>
        <div className="filter-item">
          <label className="filter-label">👥 Guruh</label>
          <select className="form-select" value={fGroup} onChange={(e) => setFGroup(e.target.value)}>
            <option value="">Barchasi</option>
            {groupsList.map(g => <option key={g.id} value={g.id}>{g.name}</option>)}
          </select>
        </div>
        <button className="btn btn-ghost" onClick={clearFilters} style={{ padding: '10px 14px', whiteSpace: 'nowrap' }}>✕ Tozalash</button>
      </div>

      {/* Grid View */}
      {view === 'grid' && (
        filtered.length === 0 ? (
          <EmptyState message="Ko'rsatiladigan dars topilmadi" icon="📅" />
        ) : (
          <div className="grid-wrap">
            <table className="grid-table">
              <thead>
                <tr>
                  <th className="grid-time-hdr">Dars<br />soati</th>
                  {allDays.map(d => (
                    <th key={d} className="grid-day-hdr" style={{ '--dc': DAY_COLORS[d] }}>{DAYS[d]}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {gridSlots.map((slot, si) => (
                  <tr key={si}>
                    <td className="grid-time-cell">
                      <div className="grid-period-num">{slot.n}</div>
                      <div className="grid-period-time">{slot.start}<br />{slot.end}</div>
                    </td>
                    {allDays.map(day => {
                      const lessons = cellMap[day]?.[slot.start] || [];
                      if (!lessons.length) return <td key={day} className="grid-cell grid-empty"></td>;
                      return (
                        <td key={day} className="grid-cell">
                          {lessons.map(l => (
                            <div key={l.id} className="grid-lesson" style={{ '--dc': DAY_COLORS[l.day_of_week] }}>
                              <div className="grid-lesson-subject" title={l.subject}>{l.subject}</div>
                              <div className="grid-lesson-meta">👨‍🏫 {maps.tMap[l.teacher_id] || '?'}</div>
                              <div className="grid-lesson-meta">🏛️ {maps.rMap[l.room_id] || '?'}</div>
                              <div className="grid-lesson-meta">👥 {maps.gMap[l.group_id] || '?'}</div>
                              <div className="grid-lesson-actions">
                                <button className="btn btn-edit" onClick={() => openEdit(l.id)} style={{ padding: '3px 7px', fontSize: 10 }}>✏️</button>
                                <button className="btn btn-danger" onClick={() => remove(l.id)} style={{ padding: '3px 7px', fontSize: 10 }}>🗑</button>
                              </div>
                            </div>
                          ))}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      )}

      {/* List View */}
      {view === 'list' && (
        <div className="tt-wrap">
          <table className="tt-table">
            <thead>
              <tr>
                <th>#</th><th>Kun</th><th>Vaqt</th><th>Fan</th>
                <th>O'qituvchi</th><th>Xona</th><th>Guruh</th><th>Amal</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr><td colSpan="8"><EmptyState message="Darslar topilmadi" icon="📅" /></td></tr>
              ) : (
                [...filtered]
                  .sort((a, b) => a.day_of_week - b.day_of_week || a.start_time.localeCompare(b.start_time))
                  .map((t, i) => (
                    <tr key={t.id}>
                      <td style={{ color: 'var(--text-muted)', fontSize: 12 }}>{i + 1}</td>
                      <td>
                        <span className="day-badge" style={{ background: DAY_COLORS[t.day_of_week] + '22', color: DAY_COLORS[t.day_of_week] }}>
                          {DAYS[t.day_of_week]}
                        </span>
                      </td>
                      <td><span className="time-range">{t.start_time.slice(0, 5)} – {t.end_time.slice(0, 5)}</span></td>
                      <td style={{ fontWeight: 500 }}>{t.subject}</td>
                      <td>{maps.tMap[t.teacher_id] || t.teacher_id}</td>
                      <td>{maps.rMap[t.room_id] || t.room_id}</td>
                      <td>{maps.gMap[t.group_id] || t.group_id}</td>
                      <td>
                        <div style={{ display: 'flex', gap: 4 }}>
                          <button className="btn btn-edit" onClick={() => openEdit(t.id)} style={{ padding: '6px 10px' }}>✏️</button>
                          <button className="btn btn-danger" onClick={() => remove(t.id)} style={{ padding: '6px 10px' }}>🗑</button>
                        </div>
                      </td>
                    </tr>
                  ))
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Modal */}
      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title={editId ? '✏️ Darsni tahrirlash' : "📅 Dars qo'shish"}>
        <div className="form-group">
          <label className="form-label">Fan</label>
          <input className="form-input" value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} placeholder="Matematika" />
        </div>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">O'qituvchi</label>
            <select className="form-select" value={form.teacher_id} onChange={(e) => setForm({ ...form, teacher_id: e.target.value })}>
              {teachersList.map(t => <option key={t.id} value={t.id}>{t.full_name}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Xona</label>
            <select className="form-select" value={form.room_id} onChange={(e) => setForm({ ...form, room_id: e.target.value })}>
              {roomsList.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
            </select>
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Guruh</label>
            <select className="form-select" value={form.group_id} onChange={(e) => setForm({ ...form, group_id: e.target.value })}>
              {groupsList.map(g => <option key={g.id} value={g.id}>{g.name}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Hafta kuni</label>
            <select className="form-select" value={form.day_of_week} onChange={(e) => setForm({ ...form, day_of_week: e.target.value })}>
              {Object.entries(DAYS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
            </select>
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Boshlanish</label>
            <input className="form-input" value={form.start_time} onChange={(e) => setForm({ ...form, start_time: e.target.value })} type="time" />
          </div>
          <div className="form-group">
            <label className="form-label">Tugash</label>
            <input className="form-input" value={form.end_time} onChange={(e) => setForm({ ...form, end_time: e.target.value })} type="time" />
          </div>
        </div>
        <div className="form-actions">
          <button className="btn btn-ghost" onClick={() => setModalOpen(false)}>Bekor</button>
          <button className="btn btn-primary" onClick={save} style={{ background: 'linear-gradient(135deg,var(--accent2),#6d28d9)' }}>{editId ? 'Yangilash' : 'Saqlash'}</button>
        </div>
      </Modal>
    </div>
  );
}
