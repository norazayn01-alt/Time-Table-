import { useState, useCallback } from 'react';
import Navbar from './components/Navbar';
import Toast from './components/Toast';
import Dashboard from './pages/Dashboard';
import Teachers from './pages/Teachers';
import Rooms from './pages/Rooms';
import Groups from './pages/Groups';
import Timetable from './pages/Timetable';
import './App.css';

export default function App() {
  const [page, setPage] = useState('dashboard');
  const [filters, setFilters] = useState({ subject: '', teacher_id: '', room_id: '', group_id: '' });
  const [toast, setToast] = useState({ message: '', type: 'success' });

  const showToast = useCallback((message, type = 'success') => {
    setToast({ message, type });
  }, []);

  const hideToast = useCallback(() => {
    setToast({ message: '', type: 'success' });
  }, []);

  const handleNavigate = useCallback((newPage, newFilters) => {
    setPage(newPage);
    if (newFilters) {
      setFilters(newFilters);
    } else {
      setFilters({ subject: '', teacher_id: '', room_id: '', group_id: '' });
    }
  }, []);

  return (
    <>
      <Navbar activePage={page} onNavigate={handleNavigate} />
      <main className="main">
        {page === 'dashboard' && <Dashboard />}
        {page === 'teachers' && <Teachers showToast={showToast} />}
        {page === 'rooms' && <Rooms showToast={showToast} />}
        {page === 'groups' && <Groups showToast={showToast} />}
        {page === 'timetable' && (
          <Timetable 
            showToast={showToast} 
            initialFilters={filters}
            onFiltersChange={setFilters}
          />
        )}
      </main>
      <Toast message={toast.message} type={toast.type} onHide={hideToast} />
    </>
  );
}
