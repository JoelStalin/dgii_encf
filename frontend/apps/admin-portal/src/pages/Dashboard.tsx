import { Activity, Building2, Coins } from "lucide-react";
import { CardKPI } from "../components/CardKPI";

const KPIS = [
  {
    title: "Compañías activas",
    value: "18",
    subtitle: "Tenants con integración DGII operativa",
    icon: <Building2 className="h-5 w-5 text-primary" aria-hidden />,
  },
  {
    title: "Comprobantes del mes",
    value: "12,450",
    subtitle: "e-CF emitidos y recibidos",
    icon: <Activity className="h-5 w-5 text-primary" aria-hidden />,
  },
  {
    title: "Ingresos proyectados",
    value: "RD$ 385,000",
    subtitle: "Planificación por planes tarifarios",
    icon: <Coins className="h-5 w-5 text-primary" aria-hidden />,
  },
];

export function DashboardPage() {
  return (
    <div className="space-y-8">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold text-white">Panel principal</h1>
        <p className="text-sm text-slate-300">
          Monitorea la salud de los tenants, métricas de facturación electrónica y cumplimiento operativo.
        </p>
      </header>
      <section className="grid gap-4 md:grid-cols-3">
        {KPIS.map((kpi) => (
          <CardKPI key={kpi.title} {...kpi} />
        ))}
      </section>
      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-white">Próximas acciones</h2>
        <ul className="space-y-2 text-sm text-slate-300">
          <li>• Validar ambiente de certificación de nuevos clientes.</li>
          <li>• Revisar alertas de planes con consumo atípico.</li>
          <li>• Confirmar renovación de certificados digitales.</li>
        </ul>
      </section>
    </div>
  );
}
