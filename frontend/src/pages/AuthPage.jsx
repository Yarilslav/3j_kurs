import { useState } from "react";
import { useOutletContext } from "react-router-dom";

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
  const { currentUser, refreshCurrentUser } = useOutletContext();
  const [mode, setMode] = useState("login");
  const [registerForm, setRegisterForm] = useState(initialRegister);
  const [loginForm, setLoginForm] = useState(initialLogin);
  const [status, setStatus] = useState("");
  const [tone, setTone] = useState("neutral");
  const [me, setMe] = useState(currentUser);
  const [loading, setLoading] = useState(false);

  async function handleRegister(event) {
    event.preventDefault();
    setLoading(true);
    setStatus("");
    setTone("neutral");
    try {
      await registerUser(registerForm);
      setTone("success");
      setStatus("Registration complete. You can now sign in.");
      setMode("login");
      setRegisterForm(initialRegister);
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleLogin(event) {
    event.preventDefault();
    setLoading(true);
    setStatus("");
    setTone("neutral");
    try {
      await loginUser(loginForm);
      const currentUser = await fetchMe();
      setMe(currentUser);
      await refreshCurrentUser();
      setTone("success");
      setStatus("Login complete. Cookie-based auth is active.");
      setLoginForm(initialLogin);
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="page-stack">
      <div className="section-card__header">
        <h1>Вхід та реєстрація</h1>
      </div>

      <div className="auth-mode-switch">
        <button
          type="button"
          className={mode === "login" ? "switch-button switch-button--active" : "switch-button"}
          onClick={() => setMode("login")}
        >
          Вхід
        </button>
        <button
          type="button"
          className={mode === "register" ? "switch-button switch-button--active" : "switch-button"}
          onClick={() => setMode("register")}
        >
          Реєстрація
        </button>
      </div>

      <div className="auth-layout">
        <form className="section-card form-grid" onSubmit={mode === "login" ? handleLogin : handleRegister}>
          <h2>{mode === "login" ? "Логін" : "Реєстрація"}</h2>

          {mode === "register" ? (
            <>
              <label>
                Ім'я
                <input value={registerForm.name} onChange={(event) => setRegisterForm({ ...registerForm, name: event.target.value })} required />
              </label>
              <label>
                Email
                <input type="email" value={registerForm.email} onChange={(event) => setRegisterForm({ ...registerForm, email: event.target.value })} required />
              </label>
              <label>
                Логін
                <input value={registerForm.login} onChange={(event) => setRegisterForm({ ...registerForm, login: event.target.value })} required />
              </label>
              <label>
                Телефон
                <input value={registerForm.phone_number} onChange={(event) => setRegisterForm({ ...registerForm, phone_number: event.target.value })} />
              </label>
              <label>
                Пароль
                <input type="password" value={registerForm.password} onChange={(event) => setRegisterForm({ ...registerForm, password: event.target.value })} required />
              </label>
            </>
          ) : (
            <>
              <label>
                Логін
                <input value={loginForm.login} onChange={(event) => setLoginForm({ ...loginForm, login: event.target.value })} required />
              </label>
              <label>
                Пароль
                <input type="password" value={loginForm.password} onChange={(event) => setLoginForm({ ...loginForm, password: event.target.value })} required />
              </label>
            </>
          )}

          <button className="button button--primary" type="submit" disabled={loading}>
            {loading ? "Зачекайте..." : mode === "login" ? "Увійти" : "Зареєструватися"}
          </button>
          <StatusBox tone={tone} message={status ? `! ${status}` : ""} />
        </form>

        <aside className="section-card auth-sidecard">
          <div className="section-pill">Ваш профіль</div>
          <h2>Поточний користувач</h2>
          {me ? (
            <dl className="data-list">
              <div>
                <dt>Ім'я</dt>
                <dd>{me.name}</dd>
              </div>
              <div>
                <dt>Логін</dt>
                <dd>{me.login}</dd>
              </div>
              <div>
                <dt>Роль</dt>
                <dd>{me.role}</dd>
              </div>
              <div>
                <dt>Email</dt>
                <dd>{me.email}</dd>
              </div>
              <div>
                <dt>Телефон</dt>
                <dd>{me.phone_number || "Не вказано"}</dd>
              </div>
              <div>
                <dt>Адреса</dt>
                <dd>{me.address || "Не вказано"}</dd>
              </div>
            </dl>
          ) : (
            <p>Після входу тут з'являться ваші дані з бекенду.</p>
          )}
        </aside>
      </div>
    </section>
  );
}
