# Manifiestos Kubernetes (Amazon EKS)

Este directorio contiene la estructura base de Kustomize para desplegar la plataforma GetUpNet en Amazon Elastic Kubernetes Service (EKS). Los manifiestos siguen las recomendaciones de seguridad (TLS 1.3, RBAC, IRSA, NetworkPolicies) y soportan los entornos `staging` y `production`.

## Estructura

- `base/`: recursos comunes (Deployments, Services, ServiceAccounts con IRSA, ConfigMap compartido, NetworkPolicy).
- `overlays/`: ajustes por entorno (imágenes, HPA, PDB, variables específicas).

```
base/
  config/
  rbac/
  services/
  namespace.yaml
  kustomization.yaml
  kustomizeconfig.yaml
overlays/
  staging/
  production/
```

## Variables y secretos

Los Deployments consumen `ConfigMap` y un `Secret` denominado `getupnet-secrets`. En producción se recomienda gestionar los secretos mediante **External Secrets Operator** apuntando a **AWS Secrets Manager**. Ejemplo:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: getupnet-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: getupnet-secrets-store
    kind: ClusterSecretStore
  target:
    name: getupnet-secrets
    creationPolicy: Merge
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: /getupnet/production/database
    - secretKey: REDIS_URL
      remoteRef:
        key: /getupnet/production/redis
    - secretKey: JWT_PRIVATE_KEY
      remoteRef:
        key: /getupnet/security/jwt
```

## Uso

1. Autenticar contra AWS y obtener credenciales del clúster:
   ```bash
   aws eks update-kubeconfig --name getupnet-prod --region us-east-1
   ```
2. Aplicar la infraestructura base (cert-manager, external-secrets, ingress) según `docs/guide/16-arquitectura-eks.md`.
3. Desplegar el entorno deseado:
   ```bash
   kubectl apply -k deploy/k8s/overlays/staging
   # o
   kubectl apply -k deploy/k8s/overlays/production
   ```
4. Verificar estado:
   ```bash
   kubectl get pods -n getupnet-app
   kubectl get hpa -n getupnet-app
   ```

## Buenas prácticas

- Actualiza las imágenes con tags firmados (`cosign`) antes de aplicar los parches.
- Configura `PodSecurityStandards` en modo `baseline` como mínimo para el namespace `getupnet-app`.
- Ajusta `resources.requests/limits` según observaciones de Prometheus.
- Añade `Ingress` y certificados TLS mediante `kustomize` o `Helm` complementario (nginx-ingress / AWS Load Balancer Controller).

Para más detalles, consulta la guía completa en `docs/guide/16-arquitectura-eks.md`.
