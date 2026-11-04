# PART IV: Bedrock Converse API Reference

## outputConfig (Structured Outputs - constrained decoding)

> Lanzado: Feb 9, 2026. Requiere boto3 >= 1.37.0 (aprox.)

Garantiza JSON valido conforme a un schema. Sin retries, sin parsing manual.

```python
response = bedrock_runtime.converse(
    modelId="qwen.qwen3-vl-235b-a22b",
    messages=[...],
    inferenceConfig={"maxTokens": 2048, "temperature": 0.0},
    outputConfig={
        "textFormat": {
            "type": "json_schema",
            "structure": {
                "jsonSchema": {
                    "schema": json.dumps(schema_dict),  # STRING, no dict
                    "name": "my_schema",
                    "description": "...",
                }
            },
        }
    },
)
# Respuesta en: response["output"]["message"]["content"][0]["text"]
```

Requisitos del schema:
- `additionalProperties: false` es OBLIGATORIO
- `schema` debe ser STRING (`json.dumps`), NO dict
- Recomendado: `temperature: 0.0` para outputs deterministas

## toolConfig (Tool Use / Function Calling)

Alternativa para structured output que funciona con boto3 viejo:

```python
response = bedrock_runtime.converse(
    modelId=MODEL_ID,
    messages=[...],
    toolConfig={              # NO usar **splat, pasar como kwarg
        "tools": [{
            "toolSpec": {
                "name": "my_tool",
                "description": "...",
                "inputSchema": {"json": schema_dict},
            }
        }],
        "toolChoice": {"tool": {"name": "my_tool"}},
    },
)
# Respuesta en: response["output"]["message"]["content"][0]["toolUse"]["input"]
# stopReason sera "tool_use"
```

## Compatibilidad de Modelos con Converse API

| Modelo | toolConfig | outputConfig | Notas |
|--------|-----------|-------------|-------|
| Qwen3 VL 235B | SI | SI (requiere boto3 nuevo) | Mejor VLM disponible |
| Llama 4 Maverick | NO (toolChoice falla) | SI (requiere boto3 nuevo) | Tool Use no soportado |
| Amazon Nova | SI | Pendiente verificar | Soporta prefilling como alternativa |

---
