import { useState, useEffect, useRef } from 'react';
import { apiFetch } from '../api';

export default function Navbar({ activePage, onNavigate }) {
  const [activeDropdown, setActiveDropdown] = useState(null); // 'teachers' | 'groups' | 'rooms' | 'timetable' | null
  const [teachers, setTeachers] = useState([]);
  const [groups, setGroups] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [subjects, setSubjects] = useState([]);
  
  const navRef = useRef(null);

  useEffect(() => {
    loadDropdownData();
  }, [activePage]); // Reload when page changes to keep sync

  useEffect(() => {
    function handleClickOutside(event) {
      if (navRef.current && !navRef.current.contains(event.target)) {
        setActiveDropdown(null);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  async function loadDropdownData() {
    try {
      const [tData, gData, rData, ttData] = await Promise.all([
        apiFetch('/teachers/'),
        apiFetch('/groups/'),
        apiFetch('/rooms/'),
        apiFetch('/timetable/'),
      ]);
      setTeachers(tData || []);
      setGroups(gData || []);
      setRooms(rData || []);
      
      // Extract unique subjects
      const uniqueSubjs = Array.from(new Set((ttData || []).map(item => item.subject).filter(Boolean)));
      uniqueSubjs.sort();
      setSubjects(uniqueSubjs);
    } catch (_) {}
  }

  function toggleDropdown(name) {
    setActiveDropdown(activeDropdown === name ? null : name);
  }

  function handleFilterSelect(page, filterKey, filterValue) {
    const filter = { subject: '', teacher_id: '', room_id: '', group_id: '' };
    if (filterKey) {
      filter[filterKey] = String(filterValue);
    }
    onNavigate(page, filter);
    setActiveDropdown(null);
  }

  return (
    <header className="navbar">
      <div className="navbar-container" ref={navRef}>
        <div className="logo-group">
          <div className="logo" style={{ marginBottom: 0 }}>TimeTable</div>
          <div className="logo-sub" style={{ marginBottom: 0, marginLeft: 10 }}>Boshqaruv</div>
        </div>
        
        <nav className="nav-menu">
          <button 
            className={`nav-link ${activePage === 'dashboard' ? 'active' : ''}`}
            onClick={() => handleFilterSelect('dashboard')}
          >
            Dashboard
          </button>

          {/* O'qituvchilar Dropdown */}
          <div className="nav-dropdown-container">
            <button 
              className={`nav-dropdown-btn ${activePage === 'teachers' || (activePage === 'timetable' && activeDropdown === 'teachers') ? 'active' : ''}`}
              onClick={() => toggleDropdown('teachers')}
            >
              <span>Ustozlar</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={activeDropdown === 'teachers' ? 'rotate' : ''}><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            {activeDropdown === 'teachers' && (
              <div className="nav-dropdown-menu">
                <div 
                  className="nav-dropdown-item manage"
                  onClick={() => handleFilterSelect('teachers')}
                >
                  Boshqarish...
                </div>
                {teachers.map(t => (
                  <div
                    key={t.id}
                    className="nav-dropdown-item"
                    onClick={() => handleFilterSelect('timetable', 'teacher_id', t.id)}
                  >
                    {t.full_name}
                  </div>
                ))}
                {teachers.length === 0 && <div className="nav-dropdown-item" style={{ color: 'var(--text-muted)' }}>Ustozlar topilmadi</div>}
              </div>
            )}
          </div>

          {/* Guruhlar Dropdown */}
          <div className="nav-dropdown-container">
            <button 
              className={`nav-dropdown-btn ${activePage === 'groups' || (activePage === 'timetable' && activeDropdown === 'groups') ? 'active' : ''}`}
              onClick={() => toggleDropdown('groups')}
            >
              <span>Guruhlar</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={activeDropdown === 'groups' ? 'rotate' : ''}><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            {activeDropdown === 'groups' && (
              <div className="nav-dropdown-menu">
                <div 
                  className="nav-dropdown-item manage"
                  onClick={() => handleFilterSelect('groups')}
                >
                  Boshqarish...
                </div>
                {groups.map(g => (
                  <div
                    key={g.id}
                    className="nav-dropdown-item"
                    onClick={() => handleFilterSelect('timetable', 'group_id', g.id)}
                  >
                    {g.name}
                  </div>
                ))}
                {groups.length === 0 && <div className="nav-dropdown-item" style={{ color: 'var(--text-muted)' }}>Guruhlar topilmadi</div>}
              </div>
            )}
          </div>

          {/* Xonalar Dropdown */}
          <div className="nav-dropdown-container">
            <button 
              className={`nav-dropdown-btn ${activePage === 'rooms' || (activePage === 'timetable' && activeDropdown === 'rooms') ? 'active' : ''}`}
              onClick={() => toggleDropdown('rooms')}
            >
              <span>Xonalar</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={activeDropdown === 'rooms' ? 'rotate' : ''}><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            {activeDropdown === 'rooms' && (
              <div className="nav-dropdown-menu">
                <div 
                  className="nav-dropdown-item manage"
                  onClick={() => handleFilterSelect('rooms')}
                >
                  Boshqarish...
                </div>
                {rooms.map(r => (
                  <div
                    key={r.id}
                    className="nav-dropdown-item"
                    onClick={() => handleFilterSelect('timetable', 'room_id', r.id)}
                  >
                    {r.name}
                  </div>
                ))}
                {rooms.length === 0 && <div className="nav-dropdown-item" style={{ color: 'var(--text-muted)' }}>Xonalar topilmadi</div>}
              </div>
            )}
          </div>

          {/* Fanlar (Jadval) Dropdown */}
          <div className="nav-dropdown-container">
            <button 
              className={`nav-dropdown-btn ${activePage === 'timetable' && activeDropdown === 'timetable' ? 'active' : ''}`}
              onClick={() => toggleDropdown('timetable')}
            >
              <span>Fanlar (Jadval)</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={activeDropdown === 'timetable' ? 'rotate' : ''}><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            {activeDropdown === 'timetable' && (
              <div className="nav-dropdown-menu">
                <div 
                  className="nav-dropdown-item manage"
                  onClick={() => handleFilterSelect('timetable')}
                >
                  Barcha darslar...
                </div>
                {subjects.map(sub => (
                  <div
                    key={sub}
                    className="nav-dropdown-item"
                    onClick={() => handleFilterSelect('timetable', 'subject', sub)}
                  >
                    {sub}
                  </div>
                ))}
                {subjects.length === 0 && <div className="nav-dropdown-item" style={{ color: 'var(--text-muted)' }}>Darslar topilmadi</div>}
              </div>
            )}
          </div>
        </nav>
      </div>
    </header>
  );
}
