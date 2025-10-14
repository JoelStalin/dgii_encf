import { Link } from "react-router-dom";
import { DataTable } from "../components/DataTable";
import { FileDownloader } from "../components/FileDownloader";

interface CompanyRow {
  id: string;
  name: string;
  rnc: string;
  env: string;
  status: string;
}

const SAMPLE: CompanyRow[] = [
  { id: "1", name: "Comercial Acme", rnc: "101112233", env: "testecf", status: "Activa" },
  { id: "2", name: "Servicios Beta", rnc: "131415161", env: "certecf", status: "En certificación" },
];

export function CompaniesPage() {
  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-white">Compañías</h1>
          <p className="text-sm text-slate-300">Gestiona tenants, ambientes DGII y certificados.</p>
        </div>
        <button className="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:bg-primary/90">
          Crear compañía
        </button>
      </header>
      <DataTable
        data={SAMPLE}
        columns={[
          {
            header: "Compañía",
            cell: (row) => (
              <div className="space-y-1">
                <Link className="text-sm font-semibold text-primary" to={`/companies/${row.id}`}>
                  {row.name}
                </Link>
                <p className="text-xs text-slate-400">RNC: {row.rnc}</p>
              </div>
            ),
          },
          { header: "Ambiente", cell: (row) => <span className="text-sm text-slate-200">{row.env}</span> },
          { header: "Estado", cell: (row) => <span className="text-sm text-slate-200">{row.status}</span> },
          {
            header: "Documentos",
            cell: () => (
              <div className="flex gap-2">
                <FileDownloader href="#" label="XML" />
                <FileDownloader href="#" label="RI" />
              </div>
            ),
          },
        ]}
      />
    </div>
  );
}
