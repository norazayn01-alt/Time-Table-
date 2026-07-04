export default function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;

  function handleOverlayClick(e) {
    if (e.target === e.currentTarget) onClose();
  }

  return (
    <div className="modal-overlay open" onClick={handleOverlayClick}>
      <div className="modal">
        <button className="modal-close" onClick={onClose}>✕</button>
        <div className="modal-title">{title}</div>
        {children}
      </div>
    </div>
  );
}
