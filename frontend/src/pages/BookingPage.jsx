import { useState } from "react";

import { createReservation } from "../api/reservations";
import StatusBox from "../components/StatusBox";

const initialBooking = {
  reservation_at: "",
  places: "",
  guest_name: "",
  guest_contact: "",
};

export default function BookingPage() {
  const [bookingForm, setBookingForm] = useState(initialBooking);
  const [status, setStatus] = useState("");
  const [tone, setTone] = useState("neutral");

  async function handleSubmit(event) {
    event.preventDefault();
    try {
      const result = await createReservation({
        reservation_at: bookingForm.reservation_at,
        places: bookingForm.places,
        guest_name: bookingForm.guest_name || undefined,
        guest_contact: bookingForm.guest_contact || undefined,
      });
      setTone("success");
      setStatus(`Reservation #${result.id} created for places ${result.places.join(", ")}.`);
      setBookingForm(initialBooking);
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    }
  }

  return (
    <section className="page-stack">
      <div className="section-card__header">
        <h1>Оберіть час, місця і контактні дані</h1>
      </div>

      <div className="booking-layout">
        <div className="section-card">
          <h2>Схема залу</h2>
          <div className="seat-grid seat-grid--booking">
            {Array.from({ length: 15 }, (_, index) => (
              <div key={index + 1} className="seat-box seat-box--soft">{index + 1}</div>
            ))}
          </div>
        </div>

        <form className="section-card form-grid" onSubmit={handleSubmit}>
          <h2>Форма бронювання</h2>
          <label>
            Дата і час
            <input
              placeholder="2026-06-05 18:00"
              value={bookingForm.reservation_at}
              onChange={(event) => setBookingForm({ ...bookingForm, reservation_at: event.target.value })}
              required
            />
          </label>
          <label>
            Місця
            <input
              placeholder="1,2,3"
              value={bookingForm.places}
              onChange={(event) => setBookingForm({ ...bookingForm, places: event.target.value })}
              required
            />
          </label>
          <label>
            Ім'я гостя
            <input
              value={bookingForm.guest_name}
              onChange={(event) => setBookingForm({ ...bookingForm, guest_name: event.target.value })}
            />
          </label>
          <label>
            Контакт
            <input
              value={bookingForm.guest_contact}
              onChange={(event) => setBookingForm({ ...bookingForm, guest_contact: event.target.value })}
            />
          </label>
          <button className="button button--primary" type="submit">
            Надіслати бронювання
          </button>
          <StatusBox tone={tone} message={status} />
        </form>
      </div>
    </section>
  );
}
