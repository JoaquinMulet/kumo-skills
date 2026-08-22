---
name: agents-sdk
description: Build AI agents on Cloudflare Workers using the Agents SDK. Load when creating stateful agents, durable workflows, real-time WebSocket apps, scheduled tasks, MCP servers, chat applications, voice agents, or browser automation. Covers Agent class, state management, callable RPC, Workflows, durable execution, queues, retries, observability, and React hooks. Biases towards retrieval from Cloudflare docs over pre-trained knowledge.
---

# Cloudflare Agents SDK

**Prefer retrieval over pre-training** for any Agents SDK task.

## Retrieval Sources

Cloudflare docs: https://developers.cloudflare.com/agents/

**Full current index:** https://developers.cloudflare.com/agents/llms.txt, if a URL below 404s or a topic is missing, fetch the index and regenerate. Any docs page can be retrieved as Markdown by appending `index.md` or sending `Accept: text/markdown`.

The docs are organized into sections: **Harnesses** (Think), **Runtime** (lifecycle, communication, execution, operations), **Communication Channels** (chat, email, Slack, voice, webhooks), **Tools** (browser, Code Mode, sandbox, payments), and **MCP**.

| Topic | Docs URL | Use for |
|-------|----------|---------|
| Getting started | [Quick start](https://developers.cloudflare.com/agents/getting-started/quick-start/) | First agent, project setup |
| Adding to existing project | [Add to existing project](https://developers.cloudflare.com/agents/getting-started/add-to-existing-project/) | Install into existing Workers app |
| Configuration | [Configuration](https://developers.cloudflare.com/agents/runtime/operations/configuration/) | `wrangler.jsonc`, bindings, assets, deployment |
| Agent class | [Agents API](https://developers.cloudflare.com/agents/runtime/agents-api/) | Agent lifecycle, patterns, pitfalls |
| State | [Store and sync state](https://developers.cloudflare.com/agents/runtime/lifecycle/state/) | `setState`, `validateStateChange`, persistence |
| Routing | [Routing](https://developers.cloudflare.com/agents/runtime/communication/routing/) | URL patterns, `routeAgentRequest` |
| Callable methods | [Callable methods](https://developers.cloudflare.com/agents/runtime/lifecycle/callable-methods/) | `@callable`, RPC, streaming, timeouts |
| Scheduling | [Schedule tasks](https://developers.cloudflare.com/agents/runtime/execution/schedule-tasks/) | `schedule()`, `scheduleEvery()`, cron |
| Workflows | [Run workflows](https://developers.cloudflare.com/agents/runtime/execution/run-workflows/) | `AgentWorkflow`, durable multi-step tasks |
| HTTP/WebSockets | [WebSockets](https://developers.cloudflare.com/agents/runtime/communication/websockets/) | Lifecycle hooks, hibernation |
| Chat agents | [Chat agents](https://developers.cloudflare.com/agents/communication-channels/chat/chat-agents/) | `AIChatAgent`, streaming, tools, persistence |
| Client SDK | [Client SDK](https://developers.cloudflare.com/agents/communication-channels/chat/client-sdk/) | `useAgent`, `useAgentChat`, React hooks |
| Client tools (Think) | [Client tools](https://developers.cloudflare.com/agents/harnesses/think/client-tools/) | Client-side tools, `autoContinueAfterToolResult` |
| Server-driven messages | [Autonomous responses](https://developers.cloudflare.com/agents/communication-channels/chat/autonomous-responses/) | `saveMessages`, `waitUntilStable`, server-initiated turns |
| Resumable streaming | [Chat SDK](https://developers.cloudflare.com/agents/runtime/communication/chat-sdk/), [HTTP/SSE](https://developers.cloudflare.com/agents/runtime/communication/http-sse/) | Stream recovery on disconnect (no longer its own page) |
| Sessions | [Sessions](https://developers.cloudflare.com/agents/runtime/lifecycle/sessions/) | Message trees, context blocks, compaction, FTS |
| Sub-agents | [Sub-agents](https://developers.cloudflare.com/agents/runtime/execution/sub-agents/) | `subAgent()`, isolated storage, typed RPC |
| Agent Skills | [Agent Skills](https://developers.cloudflare.com/agents/runtime/execution/agent-skills/) | On-demand instructions/scripts via `agents/skills` |
| Email | [Email](https://developers.cloudflare.com/agents/communication-channels/email/) | Email routing, secure reply resolver |
| MCP client | [MCP client](https://developers.cloudflare.com/agents/model-context-protocol/apis/client-api/) | Connecting to MCP servers |
| MCP server | [Handler APIs](https://developers.cloudflare.com/agents/model-context-protocol/apis/handler-api/) | Building MCP servers (stateless handlers) |
| McpAgent (deprecated) | [McpAgent](https://developers.cloudflare.com/agents/model-context-protocol/apis/agent-api/) | Feature-frozen; migrate to handler APIs |
| MCP transports | [MCP transports](https://developers.cloudflare.com/agents/model-context-protocol/protocol/transport/) | Streamable HTTP, SSE, RPC transport options |
| Securing MCP servers | [Securing MCP](https://developers.cloudflare.com/agents/model-context-protocol/guides/securing-mcp-server/) | OAuth, proxy MCP, hardening |
| Human-in-the-loop | [Human-in-the-loop](https://developers.cloudflare.com/agents/concepts/agentic-patterns/human-in-the-loop/) | Approval flows, `needsApproval`, workflows |
| Durable execution | [Durable execution](https://developers.cloudflare.com/agents/runtime/execution/durable-execution/) | `runFiber()`, `stash()`, surviving DO eviction |
| Queue | [Queue](https://developers.cloudflare.com/agents/runtime/execution/queue-tasks/) | Built-in FIFO queue, `queue()` |
| Retries | [Retries](https://developers.cloudflare.com/agents/runtime/execution/retries/) | `this.retry()`, backoff/jitter |
| Observability | [Observability](https://developers.cloudflare.com/agents/runtime/operations/observability/) | Diagnostics-channel events |
| Push notifications | [Push notifications](https://developers.cloudflare.com/agents/communication-channels/webhooks/push-notifications/) | Web Push + VAPID from agents |
| Webhooks | [Webhooks](https://developers.cloudflare.com/agents/communication-channels/webhooks/) | Receiving external webhooks |
| Cross-domain auth | [Cross-domain auth](https://developers.cloudflare.com/agents/runtime/operations/cross-domain-authentication/) | WebSocket auth, tokens, CORS |
| Readonly connections | [Readonly](https://developers.cloudflare.com/agents/runtime/communication/readonly-connections/) | `shouldConnectionBeReadonly` |
| Voice | [Voice](https://developers.cloudflare.com/agents/communication-channels/voice/) | Experimental STT/TTS, `withVoice` |
| Browse the web | [Browser tools](https://developers.cloudflare.com/agents/tools/browser/) | CDP browser automation (Browser Run) |
| Code Mode | [Code Mode](https://developers.cloudflare.com/agents/tools/codemode/) | Tool orchestration via generated code |
| Sandbox | [Sandbox](https://developers.cloudflare.com/agents/tools/sandbox/) | Isolated Linux environments for agents |
| Think | [Think](https://developers.cloudflare.com/agents/harnesses/think/) | Recommended chat-agent harness — see section below |
| Testing | [Testing your Agents](https://developers.cloudflare.com/agents/getting-started/testing-your-agent/) | Vitest + Workers test pool |
| Limits | [Limits](https://developers.cloudflare.com/agents/platform/limits/) | Concurrency, storage, compute limits |
| Migrations | [MCP SDK v2](https://developers.cloudflare.com/agents/model-context-protocol/guides/migrate-to-mcp-sdk-v2/) | Split MCP TypeScript SDK v2 packages |

> The AI SDK v5/v6 migration guides (`guides/migration-to-ai-sdk-v5|v6`) were removed from the docs.

## Think Harness (`@cloudflare/think`). Recommended for chat agents

Think is Cloudflare's opinionated chat-agent harness built on the Agents SDK: message tree with branching, persistent memory, built-in workspace tools (including bash), lifecycle hooks, streaming, durable recovery, and FTS5 search via Sessions.

| Topic | Docs URL | Use for |
|-------|----------|---------|
| Overview | [Think](https://developers.cloudflare.com/agents/harnesses/think/) | What Think provides, when to use it |
| Getting started | [Getting started](https://developers.cloudflare.com/agents/harnesses/think/getting-started/) | First Think agent, step by step |
| Tools | [Tools](https://developers.cloudflare.com/agents/harnesses/think/tools/) | Built-in/custom tools, approvals, MCP, code exec |
| Client tools | [Client tools](https://developers.cloudflare.com/agents/harnesses/think/client-tools/) | Browser-side tools, approvals, multi-tab broadcast |
| Actions | [Actions](https://developers.cloudflare.com/agents/harnesses/think/actions/) | Server-side tools, idempotency, human approvals |
| Channels | [Channels](https://developers.cloudflare.com/agents/harnesses/think/channels/) | Per-channel policy, out-of-band notices |
| Messengers | [Messengers](https://developers.cloudflare.com/agents/harnesses/think/messengers/) | Telegram/Chat SDK webhooks, routing, recovery |
| Lifecycle hooks | [Lifecycle hooks](https://developers.cloudflare.com/agents/harnesses/think/lifecycle-hooks/) | `beforeTurn`, `beforeToolCall`, `onChunk`, etc. |
| Scheduled tasks | [Scheduled tasks](https://developers.cloudflare.com/agents/harnesses/think/scheduled-tasks/) | Recurring timezone-aware turns, scheduling DSL |
| Programmatic submissions | [Programmatic submissions](https://developers.cloudflare.com/agents/harnesses/think/programmatic-submissions/) | `submitMessages()`, idempotent retry, cancellation |
| Sub-agents | [Sub-agent RPC](https://developers.cloudflare.com/agents/harnesses/think/sub-agents/) | `chat()`, `saveMessages()`, `continueLastTurn()` |
| Workflows | [Workflows](https://developers.cloudflare.com/agents/harnesses/think/workflows/) | `ThinkWorkflow`, `step.prompt()`, structured output |
| Recovery | [Durable recovery](https://developers.cloudflare.com/agents/harnesses/think/recovery/) | Stream-stall watchdog, repairing interrupted turns |
| Configuration | [Configuration](https://developers.cloudflare.com/agents/harnesses/think/configuration/) | Overrides, dynamic config, package exports |

See also **[references/think.md](references/think.md)**.

## Capabilities

The Agents SDK provides:

- **Persistent state.** SQLite-backed, auto-synced to clients via `setState`
- **Callable RPC.** `@callable()` methods invoked over WebSocket
- **Scheduling.** One-time, recurring (`scheduleEvery`), and cron tasks
- **Workflows.** Durable multi-step background processing via `AgentWorkflow`
- **Durable execution.** `runFiber()` / `stash()` for work that survives DO eviction
- **Queue.** Built-in FIFO queue with retries via `queue()`
- **Retries.** `this.retry()` with exponential backoff and jitter
- **MCP integration.** Connect to MCP servers or build your own with the handler APIs (`McpAgent` is deprecated/feature-frozen)
- **Email handling.** Receive and reply to emails with secure routing
- **Streaming chat.** `AIChatAgent` with resumable streams, message persistence, tools
- **Server-driven messages.** `saveMessages`, `waitUntilStable` for proactive agent turns
- **React hooks.** `useAgent`, `useAgentChat` for client apps
- **Observability.** `diagnostics_channel` events for state, RPC, schedule, lifecycle
- **Push notifications.** Web Push + VAPID delivery from agents
- **Webhooks.** Receive and verify external webhooks
- **Voice** (experimental), STT/TTS via `@cloudflare/voice`
- **Browser tools** (experimental), CDP-powered browsing via `agents/browser`
- **Think.** Recommended chat-agent harness via `@cloudflare/think` (message tree, branching, messengers, scheduled tasks, sub-agents, skills)

## FIRST: Verify Installation

```bash
npm ls agents  # Should show agents package
```

If not installed:
```bash
npm install agents
```

For chat agents:
```bash
npm install agents @cloudflare/ai-chat ai @ai-sdk/react
```

## Wrangler Configuration

```jsonc
{
  "compatibility_flags": ["nodejs_compat"],
  "durable_objects": {
    "bindings": [{ "name": "MyAgent", "class_name": "MyAgent" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyAgent"] }]
}
```

**Gotchas:**
- Do NOT enable `experimentalDecorators` in tsconfig (breaks `@callable`)
- Never edit old migrations, always add new tags
- Each agent class needs its own DO binding + migration entry
- Add `"ai": { "binding": "AI" }` for Workers AI

## Agent Class

```typescript
import { Agent, routeAgentRequest, callable } from "agents";

type State = { count: number };

export class Counter extends Agent<Env, State> {
  initialState = { count: 0 };

  validateStateChange(nextState: State, source: Connection | "server") {
    if (nextState.count < 0) throw new Error("Count cannot be negative");
  }

  onStateUpdate(state: State, source: Connection | "server") {
    console.log("State updated:", state);
  }

  @callable()
  increment() {
    this.setState({ count: this.state.count + 1 });
    return this.state.count;
  }
}

export default {
  fetch: (req, env) => routeAgentRequest(req, env) ?? new Response("Not found", { status: 404 })
};
```

## Routing

Requests route to `/agents/{agent-name}/{instance-name}`:

| Class | URL |
|-------|-----|
| `Counter` | `/agents/counter/user-123` |
| `ChatRoom` | `/agents/chat-room/lobby` |

Client: `useAgent({ agent: "Counter", name: "user-123" })`

Custom routing: use `getAgentByName(env.MyAgent, "instance-id")` then `agent.fetch(request)`.

## Core APIs

| Task | API |
|------|-----|
| Read state | `this.state.count` |
| Write state | `this.setState({ count: 1 })` |
| SQL query | `` this.sql`SELECT * FROM users WHERE id = ${id}` `` |
| Schedule (delay) | `await this.schedule(60, "task", payload)` |
| Schedule (cron) | `await this.schedule("0 * * * *", "task", payload)` |
| Schedule (interval) | `await this.scheduleEvery(30, "poll")` |
| RPC method | `@callable() myMethod() { ... }` |
| Streaming RPC | `@callable({ streaming: true }) stream(res) { ... }` |
| Start workflow | `await this.runWorkflow("ProcessingWorkflow", params)` |
| Durable fiber | `await this.runFiber("name", async (ctx) => { ... })` |
| Enqueue work | `this.queue("handler", payload)` |
| Retry with backoff | `await this.retry(fn, { maxAttempts: 5 })` |
| Broadcast to clients | `this.broadcast(message)` |
| Get connections | `this.getConnections(tag?)` |

## React Client

```tsx
import { useAgent } from "agents/react";

function App() {
  const [state, setLocalState] = useState({ count: 0 });

  const agent = useAgent({
    agent: "Counter",
    name: "my-instance",
    onStateUpdate: (newState) => setLocalState(newState),
    onIdentity: (name, agentType) => console.log(`Connected to ${name}`)
  });

  return (
    <button onClick={() => agent.setState({ count: state.count + 1 })}>
      Count: {state.count}
    </button>
  );
}
```

## References

### Core
- **[references/state-scheduling.md](references/state-scheduling.md).** State persistence, scheduling, SQL
- **[references/callable.md](references/callable.md).** RPC methods, streaming, timeouts
- **[references/routing.md](references/routing.md).** URL patterns, custom routing, `getAgentByName`
- **[references/configuration.md](references/configuration.md).** Wrangler config, bindings, Vite setup

### Chat & Streaming
- **[references/streaming-chat.md](references/streaming-chat.md).** AIChatAgent, resumable streams, tools
- **[references/client-sdk.md](references/client-sdk.md).** `useAgent`, `useAgentChat`, `AgentClient`
- **[references/server-driven-messages.md](references/server-driven-messages.md).** Trigger patterns, `saveMessages`
- **[references/human-in-the-loop.md](references/human-in-the-loop.md).** Approval flows, `needsApproval`

### Background Processing
- **[references/workflows.md](references/workflows.md).** Durable Workflows integration
- **[references/durable-execution.md](references/durable-execution.md).** `runFiber`, `stash`, surviving eviction
- **[references/queue-retries.md](references/queue-retries.md).** Built-in queue, retry with backoff

### Integrations
- **[references/mcp.md](references/mcp.md).** MCP client and server, transports, securing
- **[references/email.md](references/email.md).** Email routing and handling
- **[references/webhooks-push.md](references/webhooks-push.md).** Webhooks, push notifications
- **[references/observability.md](references/observability.md).** Diagnostics-channel events

### Experimental
- **[references/think.md](references/think.md).** `@cloudflare/think` higher-level chat agent
- **[references/voice.md](references/voice.md).** `@cloudflare/voice` STT/TTS
- **[references/codemode.md](references/codemode.md).** Code Mode for tool orchestration
- **[references/browse-the-web.md](references/browse-the-web.md).** CDP browser tools
