import { useAuth } from "../auth/use-auth";

export function ProfilePage() {
  const { user, tenantId, permissions } = useAuth();

  return (
    <div className="space-y-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold text-white">Perfil</h1>
        <p className="text-sm text-slate-300">Información del usuario autenticado y permisos asignados.</p>
      </header>
      <section className="space-y-2 rounded-xl border border-slate-800 bg-slate-900/40 p-6 text-sm text-slate-300">
        <p>Correo: <span className="font-semibold text-white">{user?.email}</span></p>
        <p>Scope: <span className="font-semibold text-primary">{user?.scope}</span></p>
        <p>Tenant ID: <span className="font-mono">{tenantId ?? "N/A"}</span></p>
      </section>
      <section className="space-y-2 rounded-xl border border-slate-800 bg-slate-900/40 p-6 text-sm text-slate-300">
        <h2 className="text-lg font-semibold text-white">Permisos</h2>
        <ul className="grid gap-2 md:grid-cols-2">
          {permissions.map((permission) => (
            <li key={permission} className="rounded-md border border-slate-800 bg-slate-950/40 px-3 py-2 font-mono text-xs">
              {permission}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
