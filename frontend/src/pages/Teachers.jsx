import { useState, useEffect, useCallback } from 'react';
import { apiFetch } from '../api';
import Modal from '../components/Modal';
import EmptyState from '../components/EmptyState';

export default function Teachers({ showToast }) {
  const [teachers, setTeachers] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [editId, setEditId] = useState(null);
  const [form, setForm] = useState({ full_name: '', subject: '', email: '' });

  const load = useCallback(async () => {
    try {
      const data = await apiFetch('/teachers/');
      setTeachers(data || []);
    } catch (_) {}
  }, []);

  useEffect(() => { load(); }, [load]);

  function openAdd() {
    setEditId(null);
    setForm({ full_name: '', subject: '', email: '' });
    setModalOpen(true);
  }

  async function openEdit(id) {
    try {
      const t = await apiFetch('/teachers/' + id);
      if (!t) return;
      setEditId(id);
      setForm({ full_name: t.full_name, subject: t.subject, email: t.email || '' });
      setModalOpen(true);
    } catch (_) {}
  }

  async function save() {
    const body = {
      full_name: form.full_name.trim(),
      subject: form.subject.trim(),
      email: form.email.trim() || null,
    };
    if (!body.full_name || !body.subject) {
      showToast('Ism va fan majburiy!', 'error');
      return;
    }
    try {
      if (editId) {
        await apiFetch('/teachers/' + editId, { method: 'PUT', body: JSON.stringify(body) });
        showToast("O'qituvchi yangilandi!");
      } else {
        await apiFetch('/teachers/', { method: 'POST', body: JSON.stringify(body) });
        showToast("O'qituvchi qo'shildi!");
      }
      setModalOpen(false);
      load();
    } catch (_) {}
  }

  async function remove(id) {
    if (!confirm("O'chirishni tasdiqlaysizmi?")) return;
    try {
      await apiFetch('/teachers/' + id, { method: 'DELETE' });
      showToast("O'qituvchi o'chirildi");
      load();
    } catch (_) {}
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">O'qituvchilar</h1>
        <button className="btn btn-primary" onClick={openAdd}>+ Yangi qo'shish</button>
      </div>

      {teachers.length === 0 ? (
        <EmptyState message="O'qituvchilar topilmadi" />
      ) : (
        <div className="cards-grid">
          {teachers.map((t) => (
            <div key={t.id} className="card" style={{ '--c1': '#ff6b35', '--c2': '#7c3aed' }}>
              <div className="card-header">
                <div className="card-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                </div>
                <div className="card-actions">
                  <button className="btn btn-edit" onClick={() => openEdit(t.id)} title="Tahrirlash">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
                  </button>
                  <button className="btn btn-danger" onClick={() => remove(t.id)} title="O'chirish">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                  </button>
                </div>
              </div>
              <div className="card-name">{t.full_name}</div>
              <div className="card-meta">
                <span>Fan: {t.subject}</span>
                {t.email && <span>Email: {t.email}</span>}
              </div>
              <div style={{ display: 'flex', gap: 6, marginTop: 10 }}>
                <span className="tag" style={{ background: 'rgba(255,107,53,0.15)', color: 'var(--accent)' }}>ID: {t.id}</span>
                <span className="tag" style={{
                  background: t.is_active ? 'rgba(6,214,160,0.15)' : 'rgba(239,69,101,0.12)',
                  color: t.is_active ? 'var(--accent3)' : 'var(--danger)'
                }}>{t.is_active ? 'Aktiv' : 'Nofaol'}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title={editId ? "O'qituvchini tahrirlash" : "O'qituvchi qo'shish"}>
        <div className="form-group">
          <label className="form-label">To'liq ism</label>
          <input className="form-input" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} placeholder="Aliyev Bobur" />
        </div>
        <div className="form-group">
          <label className="form-label">Fan</label>
          <input className="form-input" value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} placeholder="Matematika" />
        </div>
        <div className="form-group">
          <label className="form-label">Email (ixtiyoriy)</label>
          <input className="form-input" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} placeholder="aliyev@school.uz" type="email" />
        </div>
        <div className="form-actions">
          <button className="btn btn-ghost" onClick={() => setModalOpen(false)}>Bekor</button>
          <button className="btn btn-primary" onClick={save}>{editId ? 'Yangilash' : 'Saqlash'}</button>
        </div>
      </Modal>
    </div>
  );
}
