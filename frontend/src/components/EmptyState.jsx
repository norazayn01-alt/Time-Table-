export default function EmptyState({ message, icon }) {
  return (
    <div className="empty" style={{ gridColumn: '1 / -1' }}>
      <div className="empty-icon">
        {icon || (
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" style={{ opacity: 0.3 }}><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        )}
      </div>
      <div className="empty-text">{message}</div>
    </div>
  );
}
