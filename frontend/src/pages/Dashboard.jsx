import React, { useState, useEffect } from "react";
import {
  addSubscription,
  listSubscriptions,
  deleteSubscription,
} from "../api/auth";

export default function Dashboard() {
  const [ticker, setTicker] = useState("");
  const [subs, setSubs] = useState([]);
  const [error, setError] = useState(null);

  const load = async () => {
    try {
      const r = await listSubscriptions();
      setSubs(r.data || []);
    } catch {
      setError("Failed to load subscriptions");
    }
  };

  useEffect(() => {
    load();
  }, []);

  const add = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await addSubscription({ ticker });
      setTicker("");
      await load();
    } catch {
      setError("Failed to add subscription");
    }
  };

  const remove = async (t) => {
    try {
      await deleteSubscription(t);
      await load();
    } catch {
      setError("Failed to delete subscription");
    }
  };

  return (
    <div className="card">
      <h2>Your Subscriptions</h2>
      {error && <div className="alert">{error}</div>}
      <form onSubmit={add}>
        <input
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          placeholder="Ticker (e.g. AAPL)"
        />
        <button className="btn" type="submit">
          Add
        </button>
      </form>

      <ul className="list">
        {subs.map((s) => (
          <li key={s.id}>
            <strong>{s.ticker}</strong>
            <button className="link-button" onClick={() => remove(s.ticker)}>
              Unsubscribe
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
