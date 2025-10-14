export function PlanEditorPage() {
  return (
    <div className="space-y-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold text-white">Editor de plan tarifario</h1>
        <p className="text-sm text-slate-300">
          Configura valores fijos, porcentajes y tramos escalonados siguiendo las fórmulas descritas en la guía 13.
        </p>
      </header>
      <form className="space-y-4">
        <div className="grid gap-4 md:grid-cols-2">
          <label className="space-y-2 text-sm text-slate-300">
            Nombre del plan
            <input className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2" placeholder="Plan Mixto Pro" />
          </label>
          <label className="space-y-2 text-sm text-slate-300">
            Tipo
            <select className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2">
              <option value="FIJO">FIJO</option>
              <option value="PORCENTAJE">PORCENTAJE</option>
              <option value="MIXTO">MIXTO</option>
              <option value="ESCALONADO">ESCALONADO</option>
            </select>
          </label>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          <label className="space-y-2 text-sm text-slate-300">
            Valor fijo (RD$)
            <input type="number" className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2" />
          </label>
          <label className="space-y-2 text-sm text-slate-300">
            Porcentaje (%)
            <input type="number" className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2" />
          </label>
          <label className="space-y-2 text-sm text-slate-300">
            Mínimo (RD$)
            <input type="number" className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2" />
          </label>
        </div>
        <div className="space-y-2 text-sm text-slate-300">
          Tramos escalonados (JSON)
          <textarea
            className="h-40 w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-xs"
            placeholder='[{"from": 0, "to": 250000, "percent": 0.85}]'
          />
        </div>
        <div className="flex justify-end gap-2">
          <button type="button" className="rounded-md border border-slate-700 px-4 py-2 text-sm text-slate-200">
            Cancelar
          </button>
          <button type="submit" className="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground">
            Guardar plan
          </button>
        </div>
      </form>
    </div>
  );
}
