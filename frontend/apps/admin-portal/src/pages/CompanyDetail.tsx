import { NavLink, Outlet, useParams } from "react-router-dom";

const TABS = [
  { to: "overview", label: "Resumen" },
  { to: "invoices", label: "Comprobantes" },
  { to: "plans", label: "Planes" },
  { to: "certificates", label: "Certificados" },
  { to: "users", label: "Usuarios" },
];

export function CompanyDetailLayout() {
  const { id } = useParams();

  return (
    <div className="space-y-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold text-white">Detalle de compañía #{id}</h1>
        <p className="text-sm text-slate-300">Consulta comprobantes, planes tarifarios y equipos delegados.</p>
      </header>
      <nav className="flex flex-wrap gap-3">
        {TABS.map((tab) => (
          <NavLink
            key={tab.to}
            to={tab.to}
            className={({ isActive }) =>
              `rounded-full border px-4 py-1 text-sm transition ${isActive ? "border-primary bg-primary/20 text-primary" : "border-slate-700 text-slate-300 hover:border-primary hover:text-primary"}`
            }
          >
            {tab.label}
          </NavLink>
        ))}
      </nav>
      <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-6">
        <Outlet />
      </div>
    </div>
  );
}

export function CompanyOverviewTab() {
  return (
    <div className="space-y-4 text-sm text-slate-300">
      <p>RNC emisor: <span className="font-mono text-slate-100">131093457</span></p>
      <p>Ambiente actual: <span className="font-semibold text-primary">certecf</span></p>
      <p>Última sincronización DGII: hace 12 minutos.</p>
    </div>
  );
}

export function CompanyInvoicesTab() {
  return (
    <div className="space-y-4 text-sm text-slate-300">
      <p>Listado de comprobantes con filtros avanzados estará disponible en futuras iteraciones.</p>
    </div>
  );
}

export function CompanyPlansTab() {
  return (
    <div className="space-y-4 text-sm text-slate-300">
      <p>Plan vigente: <span className="font-semibold text-primary">Plan Mixto Pro</span></p>
      <p>Overrides: +RD$150 fijo por comprobante de contingencia.</p>
      <button className="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:bg-primary/90">
        Asignar nuevo plan
      </button>
    </div>
  );
}

export function CompanyCertificatesTab() {
  return (
    <div className="space-y-4 text-sm text-slate-300">
      <p>Último certificado subido: 2024-05-01.</p>
      <button className="rounded-md border border-dashed border-primary px-4 py-2 text-sm text-primary hover:bg-primary/10">
        Subir .p12
      </button>
    </div>
  );
}

export function CompanyUsersTab() {
  return (
    <div className="space-y-4 text-sm text-slate-300">
      <p>Usuarios delegados (RBAC multi-tenant) se mostrarán aquí.</p>
      <button className="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:bg-primary/90">
        Invitar usuario
      </button>
    </div>
  );
}
