import { useParams } from "react-router-dom";
import { StatusBadge } from "../components/StatusBadge";

export function InvoiceDetailPage() {
  const { id } = useParams();

  return (
    <div className="space-y-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold text-white">Detalle de comprobante #{id}</h1>
        <p className="text-sm text-slate-300">Visualiza XML firmado, RI y bitácora de auditoría.</p>
      </header>
      <section className="space-y-3 rounded-xl border border-slate-800 bg-slate-900/40 p-6">
        <div className="flex flex-wrap items-center gap-3 text-sm text-slate-300">
          <span>ENCF: <span className="font-mono text-slate-100">E310000000001</span></span>
          <StatusBadge status="ACEPTADO" />
          <span>Track ID: <span className="font-mono text-slate-100">abc-123-xyz</span></span>
          <span>Monto: <span className="font-semibold text-primary">RD$25,000</span></span>
        </div>
        <div className="flex gap-2 text-sm">
          <a className="rounded-md border border-slate-700 px-4 py-2 text-slate-200 hover:border-primary hover:text-primary" href="#">
            Descargar XML
          </a>
          <a className="rounded-md border border-slate-700 px-4 py-2 text-slate-200 hover:border-primary hover:text-primary" href="#">
            Descargar RI
          </a>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <p>Último evento: ACECF aceptado el 2024-05-08 11:24 AST.</p>
          <p>Hash auditoría: <span className="font-mono">a12b3c...ff</span></p>
        </div>
      </section>
    </div>
  );
}
