import { DataTable } from "../components/DataTable";

interface PlatformUser {
  email: string;
  role: string;
  scope: string;
}

const USERS: PlatformUser[] = [
  { email: "super@getupnet.do", role: "super_admin", scope: "PLATFORM" },
  { email: "ops@getupnet.do", role: "platform_admin", scope: "PLATFORM" },
];

export function PlatformUsersPage() {
  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-white">Usuarios plataforma</h1>
          <p className="text-sm text-slate-300">Controla roles y permisos globales del ecosistema.</p>
        </div>
        <button className="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:bg-primary/90">
          Invitar usuario
        </button>
      </header>
      <DataTable
        data={USERS}
        columns={[
          { header: "Correo", cell: (row) => <span className="text-sm text-slate-200">{row.email}</span> },
          { header: "Rol", cell: (row) => <span className="text-sm text-slate-300">{row.role}</span> },
          { header: "Scope", cell: (row) => <span className="text-sm text-slate-300">{row.scope}</span> },
        ]}
      />
    </div>
  );
}
