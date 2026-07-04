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
        <h1 className="page-title">O'qituvchilar <span>👨‍🏫</span></h1>
        <button className="btn btn-primary" onClick={openAdd}>+ Yangi qo'shish</button>
      </div>

      {teachers.length === 0 ? (
        <EmptyState message="O'qituvchilar topilmadi" />
      ) : (
        <div className="cards-grid">
          {teachers.map((t) => (
            <div key={t.id} className="card" style={{ '--c1': '#ff6b35', '--c2': '#7c3aed' }}>
              <div className="card-header">
                <div className="card-icon">👨‍🏫</div>
                <div className="card-actions">
                  <button className="btn btn-edit" onClick={() => openEdit(t.id)} title="Tahrirlash">✏️</button>
                  <button className="btn btn-danger" onClick={() => remove(t.id)} title="O'chirish">🗑</button>
                </div>
              </div>
              <div className="card-name">{t.full_name}</div>
              <div className="card-meta">
                <span>📚 {t.subject}</span>
                {t.email && <span>✉️ {t.email}</span>}
              </div>
              <div style={{ display: 'flex', gap: 6, marginTop: 10 }}>
                <span className="tag" style={{ background: 'rgba(255,107,53,0.15)', color: 'var(--accent)' }}>ID: {t.id}</span>
                <span className="tag" style={{
                  background: t.is_active ? 'rgba(6,214,160,0.15)' : 'rgba(239,69,101,0.12)',
                  color: t.is_active ? 'var(--accent3)' : 'var(--danger)'
                }}>{t.is_active ? '✅ Aktiv' : '❌ Nofaol'}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title={editId ? "✏️ O'qituvchini tahrirlash" : "👨‍🏫 O'qituvchi qo'shish"}>
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
