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
    <section className="stack-large">
      <div className="page-header">
        <span className="eyebrow">Route /booking</span>
        <h1>Seat booking flow</h1>
        <p>Low-fi page for choosing date/time, seats, and guest contact details.</p>
      </div>

      <div className="two-column">
        <div className="panel">
          <h2>Seat map placeholder</h2>
          <div className="seat-grid">
            {Array.from({ length: 15 }, (_, index) => (
              <div key={index + 1} className="seat-box">
                {index + 1}
              </div>
            ))}
          </div>
        </div>

        <form className="panel form-grid" onSubmit={handleSubmit}>
          <h2>Reservation form</h2>
          <label>
            Date and time
            <input
              placeholder="2026-06-05 18:00"
              value={bookingForm.reservation_at}
              onChange={(event) => setBookingForm({ ...bookingForm, reservation_at: event.target.value })}
              required
            />
          </label>
          <label>
            Places
            <input
              placeholder="1,2,3"
              value={bookingForm.places}
              onChange={(event) => setBookingForm({ ...bookingForm, places: event.target.value })}
              required
            />
          </label>
          <label>
            Guest name
            <input
              value={bookingForm.guest_name}
              onChange={(event) => setBookingForm({ ...bookingForm, guest_name: event.target.value })}
            />
          </label>
          <label>
            Guest contact
            <input
              value={bookingForm.guest_contact}
              onChange={(event) => setBookingForm({ ...bookingForm, guest_contact: event.target.value })}
            />
          </label>
          <button className="button button--primary" type="submit">
            Send reservation
          </button>
          <StatusBox tone={tone} message={status} />
        </form>
      </div>
    </section>
  );
}
