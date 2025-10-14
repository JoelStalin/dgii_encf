import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from "axios";

export interface CreateApiClientOptions {
  baseURL: string;
  getAccessToken?: () => string | null | undefined;
  getTenantId?: () => string | null | undefined;
  onUnauthorized?: () => void;
  withCredentials?: boolean;
  headers?: Record<string, string>;
  generateRequestId?: () => string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}

export function createApiClient(options: CreateApiClientOptions): AxiosInstance {
  const instance = axios.create({
    baseURL: options.baseURL,
    withCredentials: options.withCredentials ?? true,
    headers: options.headers,
  });

  instance.interceptors.request.use((config) => {
    const token = options.getAccessToken?.();
    if (token) {
      config.headers = config.headers ?? {};
      config.headers.Authorization = `Bearer ${token}`;
    }
    const tenantId = options.getTenantId?.();
    if (tenantId) {
      config.headers = config.headers ?? {};
      config.headers["X-Tenant-ID"] = tenantId;
    }
    if (!config.headers?.["X-Request-ID"]) {
      const requestId = options.generateRequestId?.() ?? globalThis.crypto?.randomUUID?.() ?? Math.random().toString(36).slice(2);
      config.headers = config.headers ?? {};
      config.headers["X-Request-ID"] = requestId;
    }
    return config;
  });

  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        options.onUnauthorized?.();
      }
      return Promise.reject(error);
    },
  );

  return instance;
}

export async function fetchPaginated<T>(
  client: AxiosInstance,
  url: string,
  config?: AxiosRequestConfig,
): Promise<PaginatedResponse<T>> {
  const response: AxiosResponse<PaginatedResponse<T>> = await client.get(url, config);
  return response.data;
}

export interface MutationConfig<TPayload> {
  client: AxiosInstance;
  url: string;
  method?: "post" | "put" | "patch" | "delete";
  payload?: TPayload;
  config?: AxiosRequestConfig;
}

export async function mutate<TResponse, TPayload = unknown>({
  client,
  url,
  method = "post",
  payload,
  config,
}: MutationConfig<TPayload>): Promise<TResponse> {
  const response = await client.request<TResponse>({
    url,
    method,
    data: payload,
    ...config,
  });
  return response.data;
}
