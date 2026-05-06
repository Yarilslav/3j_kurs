import { useState } from "react";

import { fetchMe, loginUser, registerUser } from "../api/auth";
import StatusBox from "../components/StatusBox";

const initialRegister = {
  name: "",
  email: "",
  login: "",
  phone_number: "",
  password: "",
};

const initialLogin = {
  login: "",
  password: "",
};

export default function AuthPage() {
  const [mode, setMode] = useState("login");
  const [registerForm, setRegisterForm] = useState(initialRegister);
  const [loginForm, setLoginForm] = useState(initialLogin);
  const [status, setStatus] = useState("");
  const [me, setMe] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleRegister(event) {
    event.preventDefault();
    setLoading(true);
    setStatus("");
    try {
      await registerUser(registerForm);
      setStatus("Registration complete. You can now sign in.");
      setMode("login");
      setRegisterForm(initialRegister);
    } catch (error) {
      setStatus(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleLogin(event) {
    event.preventDefault();
    setLoading(true);
    setStatus("");
    try {
      await loginUser(loginForm);
      const currentUser = await fetchMe();
      setMe(currentUser);
      setStatus("Login complete. Cookie-based auth is active.");
      setLoginForm(initialLogin);
    } catch (error) {
      setStatus(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="stack-large">
      <div className="page-header">
        <span className="eyebrow">Route /auth</span>
        <h1>Login / registration</h1>
        <p>One combined screen for the core auth flow required by the assignment.</p>
      </div>

      <div className="auth-toggle">
        <button type="button" className={mode === "login" ? "button button--primary" : "button"} onClick={() => setMode("login")}>
          Login
        </button>
        <button type="button" className={mode === "register" ? "button button--primary" : "button"} onClick={() => setMode("register")}>
          Register
        </button>
      </div>

      <div className="two-column">
        <form className="panel form-grid" onSubmit={mode === "login" ? handleLogin : handleRegister}>
          <h2>{mode === "login" ? "Login form" : "Registration form"}</h2>

          {mode === "register" ? (
            <>
              <label>
                Name
                <input value={registerForm.name} onChange={(event) => setRegisterForm({ ...registerForm, name: event.target.value })} required />
              </label>
              <label>
                Email
                <input type="email" value={registerForm.email} onChange={(event) => setRegisterForm({ ...registerForm, email: event.target.value })} required />
              </label>
              <label>
                Login
                <input value={registerForm.login} onChange={(event) => setRegisterForm({ ...registerForm, login: event.target.value })} required />
              </label>
              <label>
                Phone
                <input value={registerForm.phone_number} onChange={(event) => setRegisterForm({ ...registerForm, phone_number: event.target.value })} />
              </label>
              <label>
                Password
                <input type="password" value={registerForm.password} onChange={(event) => setRegisterForm({ ...registerForm, password: event.target.value })} required />
              </label>
            </>
          ) : (
            <>
              <label>
                Login
                <input value={loginForm.login} onChange={(event) => setLoginForm({ ...loginForm, login: event.target.value })} required />
              </label>
              <label>
                Password
                <input type="password" value={loginForm.password} onChange={(event) => setLoginForm({ ...loginForm, password: event.target.value })} required />
              </label>
            </>
          )}

          <button className="button button--primary" type="submit" disabled={loading}>
            {loading ? "Please wait..." : mode === "login" ? "Sign in" : "Create account"}
          </button>
          <StatusBox tone={status.includes("complete") ? "success" : "warning"} message={status} />
        </form>

        <aside className="panel">
          <h2>Current session</h2>
          {me ? (
            <dl className="data-list">
              <div>
                <dt>Name</dt>
                <dd>{me.name}</dd>
              </div>
              <div>
                <dt>Login</dt>
                <dd>{me.login}</dd>
              </div>
              <div>
                <dt>Role</dt>
                <dd>{me.role}</dd>
              </div>
            </dl>
          ) : (
            <p>No authenticated user loaded yet.</p>
          )}
        </aside>
      </div>
    </section>
  );
}
