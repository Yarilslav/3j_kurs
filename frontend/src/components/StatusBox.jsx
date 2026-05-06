export default function StatusBox({ tone = "neutral", title, message }) {
  if (!message) {
    return null;
  }

  return (
    <div className={`status-box status-box--${tone}`}>
      {title ? <strong>{title}</strong> : null}
      <p>{message}</p>
    </div>
  );
}
