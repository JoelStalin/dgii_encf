import { FormEvent, useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../auth/use-auth";
import type { AuthSession } from "../store/auth-store";
import { Spinner } from "../components/Spinner";

interface LocationState {
  email: string;
}

export function MFAPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { setSession } = useAuth();
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const email = (location.state as LocationState | undefined)?.email;

  useEffect(() => {
    if (!email) {
      navigate("/login", { replace: true });
    }
  }, [email, navigate]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const { data } = await api.post<AuthSession & { permissions: string[] }>("/auth/mfa/verify", {
        email,
        code,
      });
      setSession({
        accessToken: data.accessToken,
        refreshToken: data.refreshToken,
        user: data.user,
        permissions: data.permissions,
      });
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError("Código inválido o expirado.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950">
      <form onSubmit={handleSubmit} className="w-full max-w-md space-y-6 rounded-xl bg-slate-900 p-8 shadow-xl">
        <header className="space-y-2 text-center">
          <h1 className="text-2xl font-semibold text-white">Verificación MFA</h1>
          <p className="text-sm text-slate-300">Confirma tu identidad para emitir e-CF y RFCE.</p>
        </header>
        <div className="space-y-4">
          <label className="block space-y-2">
            <span className="text-sm text-slate-200">Código</span>
            <input
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-center text-lg tracking-[0.35em] focus:border-primary focus:outline-none"
              type="text"
              inputMode="numeric"
              pattern="[0-9]{6}"
              maxLength={6}
              value={code}
              onChange={(event) => setCode(event.target.value)}
              required
            />
          </label>
        </div>
        <button
          className="flex w-full items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90"
          type="submit"
          disabled={loading}
        >
          {loading ? <Spinner label="Verificando" /> : "Confirmar"}
        </button>
        {error ? <p className="text-center text-sm text-red-400">{error}</p> : null}
      </form>
    </div>
  );
}
