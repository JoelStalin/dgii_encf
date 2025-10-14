import { JsonView } from "../components/JsonView";

const SAMPLE_LOG = {
  id: "log-123",
  actor: "platform_admin@getupnet.do",
  action: "PLAN_CHARGE_COMPUTED",
  resource: "invoice:ecf:310000000000",
  hash_prev: "c61f...",
  hash_curr: "a12b...",
  ts: "2024-05-08T18:20:00Z",
};

export function AuditLogsPage() {
  return (
    <div className="space-y-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold text-white">Auditoría</h1>
        <p className="text-sm text-slate-300">
          Registros WORM con hash encadenado para cumplimiento DGII y PCI DSS.
        </p>
      </header>
      <JsonView data={SAMPLE_LOG} />
    </div>
  );
}
