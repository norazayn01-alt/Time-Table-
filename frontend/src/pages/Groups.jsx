import { useState, useEffect, useCallback } from 'react';
import { apiFetch } from '../api';
import Modal from '../components/Modal';
import EmptyState from '../components/EmptyState';

export default function Groups({ showToast }) {
  const [groups, setGroups] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [editId, setEditId] = useState(null);
  const [form, setForm] = useState({ name: '', student_count: '', course_year: '1', specialization: '' });

  const load = useCallback(async () => {
    try {
      const data = await apiFetch('/groups/');
      setGroups(data || []);
    } catch (_) {}
  }, []);

  useEffect(() => { load(); }, [load]);

  function openAdd() {
    setEditId(null);
    setForm({ name: '', student_count: '', course_year: '1', specialization: '' });
    setModalOpen(true);
  }

  async function openEdit(id) {
    try {
      const g = await apiFetch('/groups/' + id);
      if (!g) return;
      setEditId(id);
      setForm({ name: g.name, student_count: String(g.student_count), course_year: String(g.course_year), specialization: g.specialization || '' });
      setModalOpen(true);
    } catch (_) {}
  }

  async function save() {
    const body = {
      name: form.name.trim(),
      student_count: parseInt(form.student_count),
      course_year: parseInt(form.course_year),
      specialization: form.specialization.trim() || null,
    };
    if (!body.name || !body.student_count) {
      showToast('Nom va talabalar soni majburiy!', 'error');
      return;
    }
    try {
      if (editId) {
        await apiFetch('/groups/' + editId, { method: 'PUT', body: JSON.stringify(body) });
        showToast('Guruh yangilandi!');
      } else {
        await apiFetch('/groups/', { method: 'POST', body: JSON.stringify(body) });
        showToast("Guruh qo'shildi!");
      }
      setModalOpen(false);
      load();
    } catch (_) {}
  }

  async function remove(id) {
    if (!confirm("O'chirishni tasdiqlaysizmi?")) return;
    try {
      await apiFetch('/groups/' + id, { method: 'DELETE' });
      showToast("Guruh o'chirildi");
      load();
    } catch (_) {}
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Guruhlar</h1>
        <button className="btn btn-primary" onClick={openAdd} style={{ background: 'linear-gradient(135deg,var(--accent4),#e6b800)', color: '#0f0e17' }}>+ Yangi guruh</button>
      </div>

      {groups.length === 0 ? (
        <EmptyState message="Guruhlar topilmadi" />
      ) : (
        <div className="cards-grid">
          {groups.map((g) => (
            <div key={g.id} className="card" style={{ '--c1': '#ffd166', '--c2': '#e6b800' }}>
              <div className="card-header">
                <div className="card-icon" style={{ background: 'linear-gradient(135deg,var(--accent4),#e6b800)' }}>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                </div>
                <div className="card-actions">
                  <button className="btn btn-edit" onClick={() => openEdit(g.id)} title="Tahrirlash">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
                  </button>
                  <button className="btn btn-danger" onClick={() => remove(g.id)} title="O'chirish">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                  </button>
                </div>
              </div>
              <div className="card-name">{g.name}</div>
              <div className="card-meta">
                <span>Kurs: {g.course_year}-kurs</span>
                <span>Soni: {g.student_count} talaba</span>
                {g.specialization && <span>Yo'nalish: {g.specialization}</span>}
              </div>
              <div style={{ display: 'flex', gap: 6, marginTop: 10 }}>
                <span className="tag" style={{ background: 'rgba(255,209,102,0.15)', color: 'var(--accent4)' }}>ID: {g.id}</span>
                <span className="tag" style={{
                  background: g.is_active ? 'rgba(6,214,160,0.15)' : 'rgba(239,69,101,0.12)',
                  color: g.is_active ? 'var(--accent3)' : 'var(--danger)'
                }}>{g.is_active ? 'Aktiv' : 'Nofaol'}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title={editId ? 'Guruhni tahrirlash' : "Guruh qo'shish"}>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Guruh nomi</label>
            <input className="form-input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="CS-101" />
          </div>
          <div className="form-group">
            <label className="form-label">Talabalar soni</label>
            <input className="form-input" value={form.student_count} onChange={(e) => setForm({ ...form, student_count: e.target.value })} placeholder="25" type="number" />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Kurs yili</label>
            <select className="form-select" value={form.course_year} onChange={(e) => setForm({ ...form, course_year: e.target.value })}>
              <option value="1">1-kurs</option>
              <option value="2">2-kurs</option>
              <option value="3">3-kurs</option>
              <option value="4">4-kurs</option>
              <option value="5">5-kurs</option>
              <option value="6">6-kurs</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Yo'nalish</label>
            <input className="form-input" value={form.specialization} onChange={(e) => setForm({ ...form, specialization: e.target.value })} placeholder="Informatika" />
          </div>
        </div>
        <div className="form-actions">
          <button className="btn btn-ghost" onClick={() => setModalOpen(false)}>Bekor</button>
          <button className="btn btn-primary" onClick={save} style={{ background: 'linear-gradient(135deg,var(--accent4),#e6b800)', color: '#0f0e17' }}>{editId ? 'Yangilash' : 'Saqlash'}</button>
        </div>
      </Modal>
    </div>
  );
}
