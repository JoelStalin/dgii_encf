# 14. Frontend RBAC y Guardias de Ruta

Este capítulo cubre la implementación de control de acceso basado en roles y permisos (RBAC) en los portales Admin y Cliente desarrollados con React + Vite + Tailwind + shadcn/ui. Describe el modelo de seguridad, la sincronización con el backend FastAPI y patrones reutilizables para proteger rutas, componentes y acciones sensibles.

## 14.1 Principios de seguridad

- **Defensa en profundidad**: el backend valida permisos en cada endpoint y el frontend evita mostrar acciones no autorizadas.
- **Menor privilegio**: las vistas se adaptan dinámicamente a `scope` (`PLATFORM` o `TENANT`) y permisos individuales incluidos en el JWT.
- **Trazabilidad**: cada acción relevante envía encabezados `X-Trace-ID` y `X-Request-ID` generados desde el cliente.
- **Usabilidad segura**: feedback claro cuando un usuario no posee permiso, ofreciendo rutas alternativas o solicitud de acceso.

## 14.2 Estructura de autenticación en el frontend

```
/frontend/apps/*
  src/
    auth/
      auth-provider.tsx      # Contexto + React Query para sesiones
      use-auth.ts            # Hook que expone user, scope, permissions
      guards.tsx             # Componentes de guardias (RequireAuth, RequirePermission)
    store/
      auth-store.ts          # Zustand para tokens y estado de MFA
    api/
      client.ts              # Instancia fetch/axios con interceptores de tokens
      auth.ts                # Hooks React Query (`useLogin`, `useRefreshToken`)
```

- `auth-provider` monta `QueryClientProvider`, `AuthProvider` y propaga eventos de expiración.
- `auth-store` persiste `accessToken`, `refreshToken`, `user` y `permissions` en `sessionStorage` o `IndexedDB` en modo cifrado (AES-GCM) cuando el navegador lo soporte.
- El hook `useAuth()` centraliza el acceso a los datos del usuario autenticado y expone métodos `hasPermission`, `hasAnyPermission` y `hasScope`.

## 14.3 Guardias reutilizables

```tsx
export function RequirePermission({ anyOf, children }: RequirePermissionProps) {
  const { hasAnyPermission, loading } = useAuth();
  if (loading) {
    return <Spinner label="Verificando permisos" />;
  }
  if (!hasAnyPermission(anyOf)) {
    return <ForbiddenState />;
  }
  return <>{children}</>;
}
```

- `RequirePermission` se usa tanto en rutas (React Router) como en componentes (`<RequirePermission anyOf={["TENANT_INVOICE_EMIT"]}>...</RequirePermission>`).
- `RequireScope` restringe vistas completas a `PLATFORM` o `TENANT`.
- `RequireMFA` fuerza la verificación TOTP antes de operaciones críticas (ej. subir certificados).

## 14.4 Sincronización con FastAPI

1. **Login** (`POST /auth/login`): retorna `access` y `refresh`, más bandera `mfa_required`.
2. **MFA** (`POST /auth/mfa/verify`): completa la sesión y obtiene `permissions`.
3. **Perfil** (`GET /me`): usado para poblar `user`, `roles`, `permissions`, `scope` y `tenant_id`.
4. **Refresh** (`POST /auth/refresh`): renovado mediante interceptor cuando el token expira en <60 s.

Los portales envían tokens en cabecera `Authorization` y `X-Tenant-ID` cuando aplica. Para paneles protegidos con cookies (CSRF doble), se incluye `X-CSRF-Token` generado desde el backend.

## 14.5 Ejemplo de definición de rutas

```tsx
const router = createBrowserRouter([
  {
    path: "/dashboard",
    element: (
      <RequireAuth>
        <RequirePermission anyOf={["PLATFORM_TENANT_VIEW", "PLATFORM_PLAN_CRUD"]}>
          <DashboardPage />
        </RequirePermission>
      </RequireAuth>
    ),
  },
  {
    path: "/companies/:id",
    element: (
      <RequireAuth>
        <RequireScope scope="PLATFORM">
          <CompanyLayout />
        </RequireScope>
      </RequireAuth>
    ),
    children: [
      {
        path: "plans",
        element: (
          <RequirePermission anyOf={["PLATFORM_TENANT_PLAN_ASSIGN"]}>
            <CompanyPlansTab />
          </RequirePermission>
        ),
      },
    ],
  },
]);
```

## 14.6 Componentes de UX relacionados

- **NavigationMenu**: oculta enlaces según permisos disponibles.
- **ActionButton**: recibe `requiredPermissions` y se deshabilita automáticamente si no se cumplen.
- **AuditDrawer**: muestra bitácora contextual solo si `PLATFORM_AUDIT_VIEW` o `TENANT_AUDIT_VIEW` está habilitado.
- **SessionTimeoutDialog**: advierte expiración de token y permite renovar usando `useRefreshToken()`.

## 14.7 Testing de seguridad en UI

- **Unit Tests** (Vitest/React Testing Library): asegurar que componentes protegidos no se renderizan sin permisos.
- **Cypress e2e**: escenarios que validan redirecciones y mensajes cuando faltan permisos o scope.
- **Contract Tests**: mocks de `/me` con diferentes combinaciones de roles para validar el comportamiento adaptativo del menú.
- **Accessibility**: garantizar que estados de "acceso denegado" sean anunciados por lectores de pantalla.

## 14.8 Roadmap

- Integrar WebAuthn como segundo factor para operaciones de plataforma.
- Soporte para delegación temporal de permisos (ej. reemplazos de firmantes) y expiración automática.
- Sincronización con SIEM para alertar actividades sospechosas detectadas desde la UI.
