interface JsonViewProps {
  data: unknown;
}

export function JsonView({ data }: JsonViewProps) {
  return (
    <pre className="max-h-72 overflow-auto rounded-xl border border-slate-800 bg-slate-950/60 p-4 text-xs text-slate-200">
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}
