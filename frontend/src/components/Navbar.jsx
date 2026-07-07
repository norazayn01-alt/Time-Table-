import { useState, useEffect, useRef } from 'react';

export default function Navbar({ activePage, onNavigate }) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  const pages = {
    dashboard: 'Dashboard',
    teachers: "O'qituvchilar",
    groups: 'Guruhlar',
    timetable: 'Fanlar (Jadval)',
    rooms: 'Xonalar',
  };

  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <header className="navbar">
      <div className="navbar-container">
        <div className="logo-group">
          <div className="logo" style={{ marginBottom: 0 }}>TimeTable</div>
          <div className="logo-sub" style={{ marginBottom: 0, marginLeft: 10 }}>Boshqaruv</div>
        </div>
        <div className="nav-dropdown-container" ref={dropdownRef}>
          <button className="nav-dropdown-btn" onClick={() => setIsOpen(!isOpen)}>
            <span>{pages[activePage]}</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={isOpen ? 'rotate' : ''}><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          {isOpen && (
            <div className="nav-dropdown-menu">
              {Object.entries(pages).map(([key, label]) => (
                <div
                  key={key}
                  className={`nav-dropdown-item ${activePage === key ? 'active' : ''}`}
                  onClick={() => {
                    onNavigate(key);
                    setIsOpen(false);
                  }}
                >
                  {label}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
