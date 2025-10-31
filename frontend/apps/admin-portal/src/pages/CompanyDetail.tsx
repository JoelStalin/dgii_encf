import { type PropsWithChildren, FormEvent, useEffect, useState } from "react";
import { NavLink, Outlet, useParams } from "react-router-dom";
import { useAccountingSummary, useCreateLedgerEntry, useLedgerEntries, useTenantSettings, useUpdateTenantSettings } from "../api/accounting";

const TABS = [
  { to: "overview", label: "Resumen" },
  { to: "invoices", label: "Comprobantes" },
  { to: "accounting", label: "Contabilidad" },
  { to: "plans", label: "Planes" },
  { to: "certificates", label: "Certificados" },
  { to: "users", label: "Usuarios" },
  { to: "settings", label: "Parámetros" },
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

export function CompanyAccountingTab() {
  const { id } = useParams();
  const summaryQuery = useAccountingSummary(id);
  const ledgerQuery = useLedgerEntries(id);
  const createLedgerEntry = useCreateLedgerEntry(id);
  const [form, setForm] = useState({
    invoice_id: "",
    referencia: "",
    cuenta: "",
    descripcion: "",
    debit: "0.00",
    credit: "0.00",
    fecha: new Date().toISOString().slice(0, 16),
  });

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    createLedgerEntry.mutate({
      invoice_id: form.invoice_id ? Number(form.invoice_id) : null,
      referencia: form.referencia,
      cuenta: form.cuenta,
      descripcion: form.descripcion || null,
      debit: form.debit || "0",
      credit: form.credit || "0",
      fecha: new Date(form.fecha).toISOString(),
    });
  };

  const summary = summaryQuery.data;
  const ledger = ledgerQuery.data;

  return (
    <div className="space-y-6">
      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Total emitidos" value={summary?.totales.total_emitidos ?? 0} />
        <StatCard label="Aceptados" value={summary?.totales.total_aceptados ?? 0} />
        <StatCard label="Pendientes contables" value={summary?.contabilidad.pendientes ?? 0} />
        <StatCard
          label="Monto emitido"
          value={summary ? Number(summary.totales.total_monto).toLocaleString("es-DO", { style: "currency", currency: "DOP" }) : "RD$0.00"}
          isCurrency
        />
      </section>

      <section className="space-y-3">
        <h3 className="text-lg font-semibold text-white">Registrar asiento</h3>
        <form onSubmit={handleSubmit} className="grid gap-3 rounded-xl border border-slate-800 bg-slate-900/40 p-4 md:grid-cols-2">
          <input
            name="invoice_id"
            value={form.invoice_id}
            onChange={handleChange}
            placeholder="ID del comprobante (opcional)"
            className="rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
          />
          <input
            required
            name="referencia"
            value={form.referencia}
            onChange={handleChange}
            placeholder="Referencia contable"
            className="rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
          />
          <input
            required
            name="cuenta"
            value={form.cuenta}
            onChange={handleChange}
            placeholder="Cuenta contable"
            className="rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
          />
          <input
            required
            type="datetime-local"
            name="fecha"
            value={form.fecha}
            onChange={handleChange}
            className="rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
          />
          <input
            name="debit"
            value={form.debit}
            onChange={handleChange}
            placeholder="Débito"
            className="rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
          />
          <input
            name="credit"
            value={form.credit}
            onChange={handleChange}
            placeholder="Crédito"
            className="rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
          />
          <textarea
            name="descripcion"
            value={form.descripcion}
            onChange={handleChange}
            placeholder="Descripción"
            className="col-span-full rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
            rows={2}
          />
          <div className="col-span-full flex justify-end">
            <button
              type="submit"
              className="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90 disabled:cursor-not-allowed disabled:bg-slate-700"
              disabled={createLedgerEntry.isLoading}
            >
              {createLedgerEntry.isLoading ? "Guardando…" : "Registrar asiento"}
            </button>
          </div>
        </form>
      </section>

      <section className="space-y-3">
        <header className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-white">Libro contable</h3>
          <p className="text-xs text-slate-400">Mostrando {ledger?.items.length ?? 0} de {ledger?.total ?? 0} asientos</p>
        </header>
        <div className="overflow-x-auto rounded-xl border border-slate-800">
          <table className="min-w-full divide-y divide-slate-800 text-sm text-slate-300">
            <thead className="bg-slate-900/60 text-xs uppercase tracking-wide text-slate-400">
              <tr>
                <th className="px-3 py-2 text-left">Fecha</th>
                <th className="px-3 py-2 text-left">Referencia</th>
                <th className="px-3 py-2 text-left">ENCF</th>
                <th className="px-3 py-2 text-left">Cuenta</th>
                <th className="px-3 py-2 text-right">Débito</th>
                <th className="px-3 py-2 text-right">Crédito</th>
              </tr>
            </thead>
            <tbody>
              {ledger?.items.map((item) => (
                <tr key={item.id} className="border-b border-slate-800/80 hover:bg-slate-900/40">
                  <td className="px-3 py-2">{new Date(item.fecha).toLocaleString()}</td>
                  <td className="px-3 py-2 font-medium text-slate-100">{item.referencia}</td>
                  <td className="px-3 py-2 font-mono text-xs text-slate-400">{item.encf ?? "—"}</td>
                  <td className="px-3 py-2">{item.cuenta}</td>
                  <td className="px-3 py-2 text-right text-emerald-300">{Number(item.debit).toLocaleString("es-DO", { minimumFractionDigits: 2 })}</td>
                  <td className="px-3 py-2 text-right text-rose-300">{Number(item.credit).toLocaleString("es-DO", { minimumFractionDigits: 2 })}</td>
                </tr>
              ))}
              {ledger?.items.length === 0 && (
                <tr>
                  <td className="px-3 py-6 text-center text-sm text-slate-500" colSpan={6}>
                    Aún no se registran asientos contables para esta empresa.
                  </td>
                </tr>
              )}
              {!ledger && (
                <tr>
                  <td className="px-3 py-6 text-center text-sm text-slate-500" colSpan={6}>
                    Cargando libro contable…
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export function CompanyPlansTab() {
  return (
    <div className="space-y-4 text-sm text-slate-300">
      <p>
        Plan vigente: <span className="font-semibold text-primary">Plan Mixto Pro</span>
      </p>
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

export function CompanySettingsTab() {
  const { id } = useParams();
  const settingsQuery = useTenantSettings(id);
  const updateSettings = useUpdateTenantSettings(id);
  const [form, setForm] = useState({
    moneda: "DOP",
    cuenta_ingresos: "",
    cuenta_itbis: "",
    cuenta_retenciones: "",
    dias_credito: 0,
    correo_facturacion: "",
    telefono_contacto: "",
    notas: "",
  });

  useEffect(() => {
    if (settingsQuery.data) {
      setForm({
        moneda: settingsQuery.data.moneda,
        cuenta_ingresos: settingsQuery.data.cuenta_ingresos ?? "",
        cuenta_itbis: settingsQuery.data.cuenta_itbis ?? "",
        cuenta_retenciones: settingsQuery.data.cuenta_retenciones ?? "",
        dias_credito: settingsQuery.data.dias_credito,
        correo_facturacion: settingsQuery.data.correo_facturacion ?? "",
        telefono_contacto: settingsQuery.data.telefono_contacto ?? "",
        notas: settingsQuery.data.notas ?? "",
      });
    }
  }, [settingsQuery.data]);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: name === "dias_credito" ? Number(value) : value }));
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    updateSettings.mutate({
      moneda: form.moneda,
      cuenta_ingresos: form.cuenta_ingresos || null,
      cuenta_itbis: form.cuenta_itbis || null,
      cuenta_retenciones: form.cuenta_retenciones || null,
      dias_credito: form.dias_credito,
      correo_facturacion: form.correo_facturacion || null,
      telefono_contacto: form.telefono_contacto || null,
      notas: form.notas || null,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="grid gap-4 md:grid-cols-2">
      <Field label="Moneda">
        <input
          name="moneda"
          value={form.moneda}
          onChange={handleChange}
          className="w-full rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
        />
      </Field>
      <Field label="Días de crédito">
        <input
          name="dias_credito"
          type="number"
          min={0}
          max={365}
          value={form.dias_credito}
          onChange={handleChange}
          className="w-full rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
        />
      </Field>
      <Field label="Cuenta de ingresos">
        <input
          name="cuenta_ingresos"
          value={form.cuenta_ingresos}
          onChange={handleChange}
          placeholder="701-VENT"
          className="w-full rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
        />
      </Field>
      <Field label="Cuenta de ITBIS">
        <input
          name="cuenta_itbis"
          value={form.cuenta_itbis}
          onChange={handleChange}
          placeholder="208-ITBIS"
          className="w-full rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
        />
      </Field>
      <Field label="Cuenta de retenciones">
        <input
          name="cuenta_retenciones"
          value={form.cuenta_retenciones}
          onChange={handleChange}
          placeholder="209-RET"
          className="w-full rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
        />
      </Field>
      <Field label="Correo para facturación">
        <input
          name="correo_facturacion"
          value={form.correo_facturacion}
          onChange={handleChange}
          type="email"
          placeholder="facturacion@empresa.do"
          className="w-full rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
        />
      </Field>
      <Field label="Teléfono de contacto">
        <input
          name="telefono_contacto"
          value={form.telefono_contacto}
          onChange={handleChange}
          placeholder="809-555-0000"
          className="w-full rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
        />
      </Field>
      <Field label="Notas internas" className="md:col-span-2">
        <textarea
          name="notas"
          value={form.notas}
          onChange={handleChange}
          rows={3}
          className="w-full rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:border-primary focus:outline-none"
        />
      </Field>
      <div className="md:col-span-2 flex justify-end gap-3">
        {settingsQuery.data?.updated_at && (
          <span className="self-center text-xs text-slate-500">Última actualización: {new Date(settingsQuery.data.updated_at).toLocaleString()}</span>
        )}
        <button
          type="submit"
          className="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90 disabled:cursor-not-allowed disabled:bg-slate-700"
          disabled={updateSettings.isLoading}
        >
          {updateSettings.isLoading ? "Guardando…" : "Guardar cambios"}
        </button>
      </div>
    </form>
  );
}

interface StatCardProps {
  label: string;
  value: string | number;
  isCurrency?: boolean;
}

function StatCard({ label, value, isCurrency }: StatCardProps) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
      <p className="text-xs uppercase tracking-wide text-slate-400">{label}</p>
      <p className={`mt-2 text-2xl font-semibold ${isCurrency ? "text-primary" : "text-slate-100"}`}>{value}</p>
    </div>
  );
}

interface FieldProps extends PropsWithChildren {
  label: string;
  className?: string;
}

function Field({ label, children, className }: FieldProps) {
  return (
    <label className={`flex flex-col gap-1 text-sm text-slate-200 ${className ?? ""}`}>
      <span className="text-xs uppercase tracking-wide text-slate-400">{label}</span>
      {children}
    </label>
  );
}
