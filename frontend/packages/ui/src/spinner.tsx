import type { HTMLAttributes } from "react";
import { cn } from "./utils";

interface SpinnerProps extends HTMLAttributes<HTMLDivElement> {
  label?: string;
}

export function Spinner({ className, label, ...props }: SpinnerProps) {
  return (
    <div className={cn("flex items-center gap-2 text-sm text-slate-200", className)} {...props}>
      <svg
        className="h-4 w-4 animate-spin text-primary"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
        />
      </svg>
      {label ? <span>{label}</span> : null}
    </div>
  );
}
