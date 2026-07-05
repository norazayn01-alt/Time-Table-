import { useState, useEffect, useCallback } from 'react';
import { apiFetch } from '../api';
import { ROOM_ICONS } from '../constants';
import Modal from '../components/Modal';
import EmptyState from '../components/EmptyState';

export default function Rooms({ showToast }) {
  const [rooms, setRooms] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [editId, setEditId] = useState(null);
  const [form, setForm] = useState({ name: '', capacity: '', room_type: 'dars' });

  const load = useCallback(async () => {
    try {
      const data = await apiFetch('/rooms/');
      setRooms(data || []);
    } catch (_) {}
  }, []);

  useEffect(() => { load(); }, [load]);

  function openAdd() {
    setEditId(null);
    setForm({ name: '', capacity: '', room_type: 'dars' });
    setModalOpen(true);
  }

  async function openEdit(id) {
    try {
      const r = await apiFetch('/rooms/' + id);
      if (!r) return;
      setEditId(id);
      setForm({ name: r.name, capacity: String(r.capacity), room_type: r.room_type });
      setModalOpen(true);
    } catch (_) {}
  }

  async function save() {
    const body = {
      name: form.name.trim(),
      capacity: parseInt(form.capacity),
      room_type: form.room_type,
    };
    if (!body.name || !body.capacity) {
      showToast("Nom va sig'im majburiy!", 'error');
      return;
    }
    try {
      if (editId) {
        await apiFetch('/rooms/' + editId, { method: 'PUT', body: JSON.stringify(body) });
        showToast('Xona yangilandi!');
      } else {
        await apiFetch('/rooms/', { method: 'POST', body: JSON.stringify(body) });
        showToast("Xona qo'shildi!");
      }
      setModalOpen(false);
      load();
    } catch (_) {}
  }

  async function remove(id) {
    if (!confirm("O'chirishni tasdiqlaysizmi?")) return;
    try {
      await apiFetch('/rooms/' + id, { method: 'DELETE' });
      showToast("Xona o'chirildi");
      load();
    } catch (_) {}
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Xonalar</h1>
        <button className="btn btn-primary" onClick={openAdd} style={{ background: 'linear-gradient(135deg,var(--accent3),#05a87a)' }}>+ Yangi xona</button>
      </div>

      {rooms.length === 0 ? (
        <EmptyState message="Xonalar topilmadi" />
      ) : (
        <div className="cards-grid">
          {rooms.map((r) => (
            <div key={r.id} className="card" style={{ '--c1': '#06d6a0', '--c2': '#0095a8' }}>
              <div className="card-header">
                <div className="card-icon" style={{ background: 'linear-gradient(135deg,var(--accent3),#05a87a)' }}>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
                </div>
                <div className="card-actions">
                  <button className="btn btn-edit" onClick={() => openEdit(r.id)} title="Tahrirlash">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
                  </button>
                  <button className="btn btn-danger" onClick={() => remove(r.id)} title="O'chirish">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                  </button>
                </div>
              </div>
              <div className="card-name">{r.name}</div>
              <div className="card-meta">
                <span>Sig'im: {r.capacity} o'rindiq</span>
                <span>Turi: {r.room_type}</span>
              </div>
              <div style={{ display: 'flex', gap: 6, marginTop: 10 }}>
                <span className="tag" style={{ background: 'rgba(6,214,160,0.15)', color: 'var(--accent3)' }}>ID: {r.id}</span>
                <span className="tag" style={{
                  background: r.is_active ? 'rgba(6,214,160,0.15)' : 'rgba(239,69,101,0.12)',
                  color: r.is_active ? 'var(--accent3)' : 'var(--danger)'
                }}>{r.is_active ? 'Aktiv' : 'Nofaol'}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title={editId ? 'Xonani tahrirlash' : "Xona qo'shish"}>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Xona nomi</label>
            <input className="form-input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="101-xona" />
          </div>
          <div className="form-group">
            <label className="form-label">Sig'im</label>
            <input className="form-input" value={form.capacity} onChange={(e) => setForm({ ...form, capacity: e.target.value })} placeholder="30" type="number" />
          </div>
        </div>
        <div className="form-group">
          <label className="form-label">Xona turi</label>
          <select className="form-select" value={form.room_type} onChange={(e) => setForm({ ...form, room_type: e.target.value })}>
            <option value="dars">Dars xonasi</option>
            <option value="laboratoriya">Laboratoriya</option>
            <option value="majlis_zali">Majlis zali</option>
            <option value="sport_zali">Sport zali</option>
          </select>
        </div>
        <div className="form-actions">
          <button className="btn btn-ghost" onClick={() => setModalOpen(false)}>Bekor</button>
          <button className="btn btn-primary" onClick={save} style={{ background: 'linear-gradient(135deg,var(--accent3),#05a87a)' }}>{editId ? 'Yangilash' : 'Saqlash'}</button>
        </div>
      </Modal>
    </div>
  );
}
