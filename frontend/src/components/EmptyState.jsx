export default function EmptyState({ message, icon = '🔍' }) {
  return (
    <div className="empty" style={{ gridColumn: '1 / -1' }}>
      <div className="empty-icon">{icon}</div>
      <div className="empty-text">{message}</div>
    </div>
  );
}
