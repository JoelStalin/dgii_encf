import { DataTable } from "../components/DataTable";

interface PlanRow {
  name: string;
  type: string;
  minimum: string;
  status: string;
}

const PLANS: PlanRow[] = [
  { name: "Plan Base", type: "FIJO", minimum: "RD$150", status: "Activo" },
  { name: "Plan Escalonado", type: "ESCALONADO", minimum: "RD$250", status: "Borrador" },
];

export function PlansPage() {
  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-white">Planes tarifarios</h1>
          <p className="text-sm text-slate-300">Define reglas de monetización para los tenants de GetUpNet.</p>
        </div>
        <button className="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:bg-primary/90">
          Nuevo plan
        </button>
      </header>
      <DataTable
        data={PLANS}
        columns={[
          { header: "Nombre", cell: (row) => <span className="font-semibold text-slate-200">{row.name}</span> },
          { header: "Tipo", cell: (row) => <span className="text-sm text-slate-300">{row.type}</span> },
          { header: "Mínimo", cell: (row) => <span className="text-sm text-slate-300">{row.minimum}</span> },
          { header: "Estado", cell: (row) => <span className="text-sm text-slate-300">{row.status}</span> },
        ]}
      />
    </div>
  );
}
