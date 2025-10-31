import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "./client";

export interface LedgerSummary {
  totales: {
    total_emitidos: number;
    total_aceptados: number;
    total_rechazados: number;
    total_monto: string;
  };
  contabilidad: {
    contabilizados: number;
    pendientes: number;
  };
  series: Array<{ periodo: string; cantidad: number; monto: string }>;
}

export interface LedgerEntry {
  id: number;
  invoice_id: number | null;
  encf: string | null;
  referencia: string;
  cuenta: string;
  descripcion: string | null;
  debit: string;
  credit: string;
  fecha: string;
}

export interface LedgerPaginated {
  items: LedgerEntry[];
  total: number;
  page: number;
  size: number;
}

export interface TenantSettings {
  moneda: string;
  cuenta_ingresos: string | null;
  cuenta_itbis: string | null;
  cuenta_retenciones: string | null;
  dias_credito: number;
  correo_facturacion: string | null;
  telefono_contacto: string | null;
  notas: string | null;
  updated_at: string;
}

export interface TenantSettingsPayload {
  moneda: string;
  cuenta_ingresos: string | null;
  cuenta_itbis: string | null;
  cuenta_retenciones: string | null;
  dias_credito: number;
  correo_facturacion: string | null;
  telefono_contacto: string | null;
  notas: string | null;
}

export function useAccountingSummary(tenantId: string | undefined) {
  return useQuery({
    queryKey: ["accounting-summary", tenantId],
    enabled: Boolean(tenantId),
    queryFn: async () => {
      const { data } = await api.get<LedgerSummary>(`/api/admin/tenants/${tenantId}/accounting/summary`);
      return data;
    },
  });
}

export function useLedgerEntries(tenantId: string | undefined, page = 1) {
  return useQuery({
    queryKey: ["ledger", tenantId, page],
    enabled: Boolean(tenantId),
    queryFn: async () => {
      const { data } = await api.get<LedgerPaginated>(`/api/admin/tenants/${tenantId}/accounting/ledger`, {
        params: { page },
      });
      return data;
    },
  });
}

export function useTenantSettings(tenantId: string | undefined) {
  return useQuery({
    queryKey: ["tenant-settings", tenantId],
    enabled: Boolean(tenantId),
    queryFn: async () => {
      const { data } = await api.get<TenantSettings>(`/api/admin/tenants/${tenantId}/settings`);
      return data;
    },
  });
}

export function useUpdateTenantSettings(tenantId: string | undefined) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: TenantSettingsPayload) => {
      const { data } = await api.put<TenantSettings>(`/api/admin/tenants/${tenantId}/settings`, payload);
      return data;
    },
    onSuccess: (data) => {
      queryClient.setQueryData(["tenant-settings", tenantId], data);
    },
  });
}

export interface LedgerEntryPayload {
  invoice_id: number | null;
  referencia: string;
  cuenta: string;
  descripcion: string | null;
  debit: string;
  credit: string;
  fecha: string;
}

export function useCreateLedgerEntry(tenantId: string | undefined) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: LedgerEntryPayload) => {
      const { data } = await api.post<LedgerEntry>(`/api/admin/tenants/${tenantId}/accounting/ledger`, payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ledger", tenantId] });
      queryClient.invalidateQueries({ queryKey: ["accounting-summary", tenantId] });
    },
  });
}
