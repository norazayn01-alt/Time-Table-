export default function StatCard({ icon, label, value, color }) {
  return (
    <div className="stat-card" style={{ '--c1': color }}>
      <div className="stat-icon">{icon}</div>
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
    </div>
  );
}
