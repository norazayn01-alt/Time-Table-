import { useEffect } from 'react';

export default function Toast({ message, type, onHide }) {
  useEffect(() => {
    if (message) {
      const timer = setTimeout(onHide, 3000);
      return () => clearTimeout(timer);
    }
  }, [message, onHide]);

  return (
    <div className={`toast ${message ? 'show' : ''} ${type || ''}`}>
      {type === 'success' ? '✅ ' : '❌ '}{message}
    </div>
  );
}
