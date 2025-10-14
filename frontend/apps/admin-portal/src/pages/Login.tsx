import { FormEvent, useMemo, useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useLoginMutation } from "../api/auth";
import { useAuth } from "../auth/use-auth";
import { Spinner } from "../components/Spinner";

export function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const location = useLocation();
  const { mutateAsync, isPending, isError } = useLoginMutation();
  const { isAuthenticated } = useAuth();

  const from = useMemo(() => {
    const state = location.state as { from?: { pathname?: string } } | undefined;
    return state?.from?.pathname ?? "/dashboard";
  }, [location.state]);

  useEffect(() => {
    if (isAuthenticated) {
      navigate(from, { replace: true });
    }
  }, [from, isAuthenticated, navigate]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const response = await mutateAsync({ email, password });
    if (response.mfa_required) {
      navigate("/mfa", { state: { email } });
      return;
    }
    navigate(from, { replace: true });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950">
      <form onSubmit={handleSubmit} className="w-full max-w-md space-y-6 rounded-xl bg-slate-900 p-8 shadow-xl">
        <header className="space-y-2 text-center">
          <h1 className="text-2xl font-semibold text-white">GetUpNet Admin</h1>
          <p className="text-sm text-slate-300">Autenticación multi-factor con controles RBAC.</p>
        </header>
        <div className="space-y-4">
          <label className="block space-y-2">
            <span className="text-sm text-slate-200">Correo electrónico</span>
            <input
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm focus:border-primary focus:outline-none"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </label>
          <label className="block space-y-2">
            <span className="text-sm text-slate-200">Contraseña</span>
            <input
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm focus:border-primary focus:outline-none"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </label>
        </div>
        <button
          className="flex w-full items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90"
          type="submit"
          disabled={isPending}
        >
          {isPending ? <Spinner label="Validando" /> : "Ingresar"}
        </button>
        {isError ? <p className="text-center text-sm text-red-400">Credenciales inválidas o MFA requerido.</p> : null}
      </form>
    </div>
  );
}
