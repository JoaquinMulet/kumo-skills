---
name: aws-deploy
description: Deploy serverless Python applications to AWS using SAM CLI, with anti-patterns discovered in production. Use when deploying Lambda functions, configuring SAM templates, writing DynamoDB code, debugging SAM build/deploy errors, setting up multi-environment deployments, or using Bedrock Converse API. Covers Docker/zip Lambdas, DynamoDB constraints (float/Decimal, reserved words), SQS+Lambda patterns, CloudWatch Alarms, boto3 version management, and Bedrock structured outputs.
---

# AWS Deploy - SAM + Anti-Patterns de Produccion

Deploy serverless Python applications (Lambda, S3, SQS, DynamoDB, API Gateway) to AWS using SAM CLI. Includes anti-patterns criticos descubiertos en produccion y referencia de Bedrock Converse API.

## When to Use

- Deploying Lambda functions (Python, Docker, ZIP)
- Configuring `template.yaml` for SAM
- Writing code that interacts with DynamoDB
- Setting up multi-environment deploys (dev/staging/prod)
- Debugging `sam build` or `sam deploy` errors
- Adding production infrastructure (DLQ, alarms, lifecycle rules)
- Consuming streaming APIs (Fireworks, OpenAI-compatible) from Lambda
- Designing async flows with SQS + Lambda + DynamoDB
- Using Bedrock Converse API for structured outputs

## Prerequisites

- AWS SAM CLI installed (`sam --version`)
  - Windows default: `C:\Program Files\Amazon\AWSSAMCLI\bin\sam.cmd`
  - If not in PATH, use full path
- AWS CLI configured (`aws configure`)
- Docker running (for `PackageType: Image` functions)

## Project Structure

```
project/
  infra/
    template.yaml       # SAM template (required)
    samconfig.toml       # Deploy config per environment (recommended)
  Dockerfile             # For container-based Lambdas
  Dockerfile.ingest      # Separate lightweight Dockerfile per function (optional)
  lambda_handlers/       # Lambda code
  requirements.txt       # Python dependencies
```

---

# PART I: SAM Template Reference

Moved to [`reference/plantillas-sam.md`](reference/plantillas-sam.md). Read it before writing that part.

# PART II: Multi-Environment Config

## samconfig.toml

```toml
# Default = dev
[default.deploy.parameters]
stack_name = "my-app-dev"
resolve_s3 = true
s3_prefix = "my-app-sam-dev"
region = "us-east-1"
confirm_changeset = false
capabilities = "CAPABILITY_NAMED_IAM"
image_repositories = ["MyFunction=123456789.dkr.ecr.us-east-1.amazonaws.com/my-app"]
parameter_overrides = "Environment=dev"

# Production
[prod.deploy.parameters]
stack_name = "my-app-prod"
resolve_s3 = true
s3_prefix = "my-app-sam-prod"
region = "us-east-1"
confirm_changeset = true          # Always confirm in prod
capabilities = "CAPABILITY_NAMED_IAM"
image_repositories = ["MyFunction=123456789.dkr.ecr.us-east-1.amazonaws.com/my-app"]
parameter_overrides = "Environment=prod"
```

## Build and Deploy Commands

```bash
# Build (from directory containing template.yaml)
sam build

# Deploy dev (default)
sam deploy

# Deploy production
sam deploy --config-env prod

# Build + deploy in one go
sam build && sam deploy --config-env prod

# Force rebuild without cache
sam build --no-cached

# Deploy with specific overrides
sam deploy --parameter-overrides "Environment=staging BucketName=my-existing-bucket"
```

---

# PART III: Anti-Patterns Descubiertos en Produccion

## ANTI-PATTERN 1: Float en DynamoDB

### Problema

DynamoDB no acepta valores `float` de Python. `boto3` lanza `TypeError` al intentar guardar floats.

```
TypeError: Float types are not supported. Use Decimal types instead.
```

### Donde Aparece

Cualquier dato proveniente de:
- `model_dump()` de Pydantic (genera floats)
- Respuestas JSON parseadas con `json.loads()` (genera floats)
- Metricas como `duration_ms`, `total_tokens`, etc.

### Solucion

Aplicar conversion recursiva antes de guardar:

```python
from decimal import Decimal

def _float_to_decimal(obj):
    """Recursively convert float values to Decimal for DynamoDB."""
    if isinstance(obj, float):
        return Decimal(str(obj))  # str() evita imprecision
    elif isinstance(obj, dict):
        return {k: _float_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_float_to_decimal(v) for v in obj]
    return obj
```

**CRITICO:** Usar `Decimal(str(value))`, NUNCA `Decimal(value)` directamente.
`Decimal(0.1)` produce `0.1000000000000000055511151231257827021181583404541015625`.

### Regla

> Antes de cualquier `put_item()` o `update_item()` con datos dinamicos,
> pasar el payload por `_float_to_decimal()`.

---

## ANTI-PATTERN 2: Palabras Reservadas en DynamoDB

### Problema

DynamoDB tiene ~580 palabras reservadas. Usar una como nombre de atributo en
`UpdateExpression` sin alias genera `ValidationException`.

```
ValidationException: Invalid UpdateExpression: 
Attribute name is a reserved keyword; reserved keyword: status
```

### Palabras Reservadas Comunes que Generan Bugs

| Palabra | Uso tipico |
|---------|-----------|
| `status` | Estado de un job/tarea |
| `error` | Mensaje de error |
| `result` | Resultado de procesamiento |
| `name` | Nombre de entidad |
| `type` | Tipo de recurso |
| `data` | Payload de datos |
| `size` | Tamano de archivo |
| `count` | Contadores |
| `time` | Timestamps |
| `value` | Valores genericos |

### Solucion

Usar `ExpressionAttributeNames` para TODOS los campos, no solo los reservados:

```python
def update_item_safe(table, key: dict, **fields):
    update_expr_parts = []
    expr_names = {}
    expr_values = {}
    
    for field_name, field_value in fields.items():
        alias = f"#{field_name}"
        placeholder = f":{field_name}"
        update_expr_parts.append(f"{alias} = {placeholder}")
        expr_names[alias] = field_name
        expr_values[placeholder] = _float_to_decimal(field_value)
    
    table.update_item(
        Key=key,
        UpdateExpression="SET " + ", ".join(update_expr_parts),
        ExpressionAttributeNames=expr_names,
        ExpressionAttributeValues=expr_values
    )
```

### Regla

> SIEMPRE usar `ExpressionAttributeNames` con alias `#campo` para todos
> los atributos en `UpdateExpression`. Nunca escribir nombres directos.

---

## ANTI-PATTERN 3: Runtime/Architectures en Globals de SAM con Docker

### Problema

Cuando una Lambda usa `PackageType: Image` (Docker), NO puede heredar
`Runtime` ni `Architectures` de la seccion `Globals` del template SAM.
CloudFormation lanza error de validacion.

```
Error: WorkerFunction: Runtime and Architectures cannot be specified 
when PackageType is Image
```

### Solucion

Si el stack tiene mezcla de Lambdas nativas y Docker:

1. **Remover** `Runtime` y `Architectures` de `Globals:`
2. **Definir** `Runtime` y `Architectures` individualmente en cada Lambda nativa
3. La Lambda Docker solo necesita `PackageType: Image` y `ImageUri`

```yaml
Globals:
  Function:
    Timeout: 300
    MemorySize: 1024
    # NO poner Runtime ni Architectures aqui

Resources:
  # Lambda nativa - define Runtime individualmente
  DispatcherFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.11
      Architectures: [arm64]
      Handler: api.dispatcher.handler

  # Lambda Docker - NO tiene Runtime
  WorkerFunction:
    Type: AWS::Serverless::Function
    Properties:
      PackageType: Image
      ImageUri: !Ref WorkerImageUri
      Architectures: [arm64]  # OK en la funcion, no en Globals
```

### Regla

> En templates SAM con mix de Lambdas nativas y Docker, NUNCA poner
> `Runtime` ni `Architectures` en la seccion `Globals`.

---

## ANTI-PATTERN 4: Asumir Tipo de `chunk.usage` en Streaming

### Problema

Al consumir APIs OpenAI-compatible (Fireworks, Together, Groq) con `stream=True`,
la propiedad `chunk.usage` puede ser un objeto Pydantic o un diccionario Python raw,
dependiendo del chunk. Acceder con notacion de atributo (`.prompt_tokens`) genera
`AttributeError` cuando llega como dict.

```
AttributeError: 'dict' object has no attribute 'prompt_tokens'
```

### Solucion

Duck-typing defensivo con `isinstance()`:

```python
async for chunk in stream:
    if chunk.usage:
        usage = chunk.usage
        if isinstance(usage, dict):
            prompt_tokens = usage.get('prompt_tokens', 0) or 0
            completion_tokens = usage.get('completion_tokens', 0) or 0
        else:
            prompt_tokens = getattr(usage, 'prompt_tokens', 0) or 0
            completion_tokens = getattr(usage, 'completion_tokens', 0) or 0
```

### Regla

> Al procesar chunks de streaming, SIEMPRE verificar el tipo de `chunk.usage`
> con `isinstance(usage, dict)` antes de acceder a sus propiedades.

---

## ANTI-PATTERN 5: SQS VisibilityTimeout vs Lambda Timeout

### Problema

Si `VisibilityTimeout` de SQS es menor que el timeout de Lambda, SQS re-entrega
el mensaje mientras el worker aun lo esta procesando, causando duplicados.

### Solucion

```
VisibilityTimeout >= Lambda Timeout + margen de seguridad

Ejemplo:
  Lambda Timeout = 300s (5 min)
  VisibilityTimeout = 360s (6 min)
  Margen = 60s
```

Complementar con **Conditional Update** en DynamoDB (lease con timeout):

```python
def claim_job(job_id: str) -> bool:
    """Atomic claim con deteccion de worker zombie."""
    now = int(time.time())
    stale_threshold = now - STALE_JOB_THRESHOLD_SECONDS
    
    table.update_item(
        Key={"jobId": job_id},
        UpdateExpression="SET #s = :processing, claimedAt = :now",
        ConditionExpression=(
            "#s = :queued OR "
            "(#s = :processing AND claimedAt < :stale_threshold)"
        ),
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={...}
    )
```

### Regla

> `VisibilityTimeout` debe ser SIEMPRE mayor que el Lambda timeout.
> Implementar idempotencia con conditional updates en DynamoDB.

---

## ANTI-PATTERN 6: Lambda boto3 Desactualizado (CRITICO)

> **Incidente 2026-02-12**: boto3 del Lambda Python runtime es viejo, NO soporta features nuevas como Structured Outputs (`outputConfig`).

### Problema

La imagen base `public.ecr.aws/lambda/python:3.12` incluye un boto3 preinstalado.
Agregar `boto3>=X.Y.Z` en `requirements.txt` NO lo actualiza porque pip ve que ya esta satisfecho.

### Solucion: Forzar upgrade en Dockerfile

```dockerfile
# DESPUES de instalar requirements.txt
RUN pip install --no-cache-dir --upgrade --force-reinstall boto3 botocore
```

Flags importantes:
- `--upgrade`: permite instalar version mas nueva
- `--force-reinstall`: reinstala aunque ya exista
- `--no-cache-dir`: evita cache Docker de pip

### Verificacion

Agregar logging en el handler para verificar version:
```python
import boto3, botocore
print(f"boto3={boto3.__version__}, botocore={botocore.__version__}")
```

### Alternativa: Lambda Layer

Para funciones ZIP (no Docker), crear Lambda Layer con boto3 actualizado.

### Regla

> Al usar features nuevas de AWS (Bedrock Structured Outputs, etc.), SIEMPRE
> forzar `--force-reinstall boto3 botocore` en el Dockerfile.

---

## ANTI-PATTERN 7: Bedrock Converse API - `**dict` Splat en toolConfig

### Problema

Pasar `tools` y `toolChoice` como top-level kwargs usando `**dict` splat genera error.
Bedrock Converse API espera un unico kwarg `toolConfig` que contiene ambos.

```
Unknown parameter: tools
Unknown parameter: toolChoice
```

### Solucion

```python
# INCORRECTO - splat de dict
params = {"tools": [...], "toolChoice": {...}}
response = bedrock.converse(modelId=MODEL, messages=msgs, **params)

# CORRECTO - toolConfig como kwarg explicito
response = bedrock.converse(
    modelId=MODEL,
    messages=msgs,
    toolConfig={
        "tools": [...],
        "toolChoice": {...},
    },
)
```

### Regla

> Bedrock Converse API: `tools` y `toolChoice` van DENTRO de `toolConfig`,
> nunca como kwargs de nivel superior.

---

# PART IV: Bedrock Converse API Reference

Moved to [`reference/bedrock-converse.md`](reference/bedrock-converse.md). Read it before writing that part.

# PART V: Common Errors Table

| Error | Cause | Fix |
|-------|-------|-----|
| `sam` not found | Not in PATH (Windows) | Use `& "C:\Program Files\Amazon\AWSSAMCLI\bin\sam.cmd"` |
| `ResourceNotFoundException` on deploy | ECR repo doesn't exist | Create ECR repo first or use `resolve_image_repos = true` |
| `CAPABILITY_NAMED_IAM` error | Missing capability | Add `capabilities = "CAPABILITY_NAMED_IAM"` to samconfig |
| Docker build fails | Docker not running | Start Docker Desktop |
| Env var mismatch | Template uses `BUCKET_NAME`, code reads `S3_BUCKET` | Verify env var names match between template and code |
| Image push timeout | Large image or slow connection | Normal for first push; subsequent pushes use layer cache |
| ChangeSet empty | No resource diff detected | Nothing to deploy, resources already up to date |
| `Unknown parameter outputConfig` | Lambda's boto3 is too old | Force boto3 upgrade in Dockerfile (Anti-Pattern 6) |
| `Unknown parameter: tools/toolChoice` | Using `**dict` splat | Use `toolConfig={tools:..., toolChoice:...}` (Anti-Pattern 7) |
| `TypeError: Float types` | Python float in DynamoDB | Use `_float_to_decimal()` (Anti-Pattern 1) |
| `ValidationException: reserved keyword` | Attribute name is reserved | Use `ExpressionAttributeNames` (Anti-Pattern 2) |
| `Runtime cannot be specified when PackageType is Image` | Runtime in Globals with Docker Lambda | Remove Runtime from Globals (Anti-Pattern 3) |
| Write silently no-ops in AWS but all tests pass | Handler policy is read-only (`DynamoDBReadPolicy`) and moto does NOT validate IAM; AccessDenied may be swallowed by best-effort try/except | Add `DynamoDBCrudPolicy` in the SAME commit as any new write; verify post-deploy by reading the persisted record, never by the 200 response |

---

# PART VI: Production Readiness Checklist

### Code
- [ ] No debug logging (memory profiling, raw API responses)
- [ ] No hardcoded credentials or account IDs in code
- [ ] Environment variables match between template and code
- [ ] Model/API fallback values are correct for production
- [ ] Error handling returns structured responses (no stack traces to clients)

### DynamoDB
- [ ] All data passes through `_float_to_decimal()` before writes
- [ ] All `UpdateExpression` use `ExpressionAttributeNames` with `#` aliases
- [ ] Workers implement atomic `claim_job()` for idempotency

### Streaming APIs
- [ ] `chunk.usage` handled with duck-typing (`isinstance(usage, dict)`)
- [ ] Timeout and retry logic for external API calls

### Infrastructure
- [ ] DLQ configured for async Lambda invocations
- [ ] CloudWatch Alarms on errors, near-timeout, and DLQ messages
- [ ] S3 lifecycle rules for temporary and output files
- [ ] Separate Docker images for functions with different dependency profiles
- [ ] `SQS VisibilityTimeout` > `Lambda Timeout`
- [ ] `confirm_changeset = true` in production config
- [ ] boto3 force-reinstalled if using new AWS features

### SAM Template
- [ ] No `Runtime`/`Architectures` in `Globals` if stack has Docker Lambdas
- [ ] Each native Lambda defines its own `Runtime` and `Architectures`

### Security
- [ ] `.gitignore` excludes sensitive files (PDFs, credentials, build artifacts)
- [ ] S3 bucket has public access blocked
- [ ] IAM policies use least privilege (specific resource ARNs, not `*` where possible)
- [ ] Every handler that WRITES has a write-capable policy — moto does not validate IAM: a new `update_item` in a read-only handler passes all tests and gets AccessDenied only in AWS (worse if swallowed by a best-effort catch). Template-contract test the policy; smoke-test writes by persisted effect
- [ ] No PII or sensitive data logged to CloudWatch
- [ ] S3 versioning enabled for audit trail

### Operations
- [ ] Multi-environment config (dev/staging/prod) in samconfig.toml
- [ ] Separate stack names per environment
- [ ] Outputs exported for cross-stack references
- [ ] Deployment tested in dev before prod

---

# Useful SAM CLI Commands

Moved to [`reference/comandos-sam.md`](reference/comandos-sam.md). Read it before writing that part.
