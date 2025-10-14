import { Link } from "react-router-dom";
import { DataTable } from "../components/DataTable";
import { StatusBadge } from "../components/StatusBadge";

interface InvoiceRow {
  id: string;
  encf: string;
  total: string;
  status: "ACEPTADO" | "EN_PROCESO" | "RECHAZADO";
}

const INVOICES: InvoiceRow[] = [
  { id: "1", encf: "E310000000001", total: "RD$25,000", status: "ACEPTADO" },
  { id: "2", encf: "E310000000002", total: "RD$280,000", status: "EN_PROCESO" },
];

export function InvoicesPage() {
  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-white">Comprobantes electrónicos</h1>
          <p className="text-sm text-slate-300">Consulta estados DGII, descargas XML y RI.</p>
        </div>
        <div className="flex gap-2">
          <Link className="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground" to="/emit/ecf">
            Emitir e-CF
          </Link>
          <Link className="rounded-md border border-slate-700 px-4 py-2 text-sm text-slate-200" to="/emit/rfce">
            Emitir RFCE
          </Link>
        </div>
      </header>
      <DataTable
        data={INVOICES}
        columns={[
          {
            header: "ENCF",
            cell: (row) => (
              <Link className="text-sm font-semibold text-primary" to={`/invoices/${row.id}`}>
                {row.encf}
              </Link>
            ),
          },
          { header: "Total", cell: (row) => <span className="text-sm text-slate-300">{row.total}</span> },
          { header: "Estado DGII", cell: (row) => <StatusBadge status={row.status} /> },
        ]}
      />
    </div>
  );
}
