import { useEffect, useMemo, useState } from "react";
import { Bot, Database, Globe2, MessageSquareQuote, Radar, UploadCloud } from "lucide-react";

type VerticalItem = {
  slug: string;
  name: string;
  sector: string;
  short_description: string;
  common_use_cases: string[];
  tone_guidance: string;
};

type Citation = {
  chunk_id: number;
  document_title: string;
  snippet: string;
  score: number;
};

type ChatPayload = {
  conversation_id: number;
  intent: string;
  answer: string;
  citations: Citation[];
  actions: Array<{ type: string; label: string; payload: Record<string, unknown> }>;
  memory_summary: string;
};

type StatsPayload = {
  document_count: number;
  chunk_count: number;
  conversation_count: number;
};

const API_BASE = "http://localhost:4300";

export default function App() {
  const [verticals, setVerticals] = useState<VerticalItem[]>([]);
  const [verticalCount, setVerticalCount] = useState(0);
  const [stats, setStats] = useState<StatsPayload | null>(null);
  const [selectedVertical, setSelectedVertical] = useState("b2b-saas");
  const [message, setMessage] = useState("Can you explain pricing and help me book a demo?");
  const [chat, setChat] = useState<ChatPayload | null>(null);
  const [importTitle, setImportTitle] = useState("Business FAQ");
  const [importContent, setImportContent] = useState(
    "We offer onboarding, support, and customized implementation packages for enterprise clients.",
  );
  const [status, setStatus] = useState("Ready");

  useEffect(() => {
    Promise.all([
      fetch(`${API_BASE}/verticals`).then((response) => response.json()),
      fetch(`${API_BASE}/stats`).then((response) => response.json()),
    ])
      .then(([verticalPayload, statsPayload]) => {
        setVerticals(verticalPayload.items);
        setVerticalCount(verticalPayload.count);
        setStats(statsPayload);
      })
      .catch(() => {
        setStatus("API unavailable. Start the FastAPI backend to activate the workspace.");
      });
  }, []);

  const sectorPreview = useMemo(() => {
    const sectors = new Set(verticals.map((item) => item.sector));
    return Array.from(sectors).slice(0, 6);
  }, [verticals]);

  async function refreshStats() {
    const statsPayload = (await fetch(`${API_BASE}/stats`).then((response) => response.json())) as StatsPayload;
    setStats(statsPayload);
  }

  async function seedDemo() {
    setStatus("Seeding demo workspace...");
    const response = await fetch(`${API_BASE}/seed-demo`, { method: "POST" });
    if (!response.ok) {
      setStatus("Failed to seed demo workspace.");
      return;
    }
    await refreshStats();
    setStatus("Demo workspace seeded.");
  }

  async function importDocument() {
    setStatus("Importing knowledge...");
    const response = await fetch(`${API_BASE}/documents/import`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        workspace_id: "demo-workspace",
        title: importTitle,
        vertical: selectedVertical,
        content: importContent,
        source_type: "manual",
      }),
    });
    if (!response.ok) {
      setStatus("Import failed.");
      return;
    }
    await refreshStats();
    setStatus("Knowledge imported.");
  }

  async function sendChat() {
    setStatus("Thinking...");
    const response = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        workspace_id: "demo-workspace",
        vertical: selectedVertical,
        message,
      }),
    });
    if (!response.ok) {
      setStatus("Chat failed.");
      return;
    }
    const payload = (await response.json()) as ChatPayload;
    setChat(payload);
    setStatus(`Intent detected: ${payload.intent}`);
  }

  return (
    <main className="min-h-screen bg-transparent text-[#f5efe7]">
      <div className="mx-auto w-[min(1440px,calc(100vw-32px))] py-6 md:py-8">
        <section className="grid gap-5 md:grid-cols-[1.1fr,0.9fr]">
          <div className="rounded-[28px] border border-white/10 bg-white/5 p-7 shadow-panel backdrop-blur-xl">
            <p className="font-mono text-xs uppercase tracking-[0.32em] text-bronze">Omni RAG Agent Studio</p>
            <h1 className="mt-3 max-w-[10ch] font-display text-5xl leading-[0.92] tracking-[-0.05em] md:text-7xl">
              Agentic RAG for business knowledge at real-world scale.
            </h1>
            <p className="mt-5 max-w-3xl text-base leading-8 text-white/70">
              A multi-business starter for grounded support, sales, knowledge retrieval, and safe escalation. The
              backend combines retrieval, memory, and action planning instead of pretending one prompt can solve every
              business workflow.
            </p>

            <div className="mt-7 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <SignalCard label="Vertical coverage" value={`${verticalCount}+`} icon={<Globe2 className="h-5 w-5" />} />
              <SignalCard label="Knowledge docs" value={`${stats?.document_count ?? 0}`} icon={<Database className="h-5 w-5" />} />
              <SignalCard label="Indexed chunks" value={`${stats?.chunk_count ?? 0}`} icon={<Radar className="h-5 w-5" />} />
              <SignalCard
                label="Conversations"
                value={`${stats?.conversation_count ?? 0}`}
                icon={<Bot className="h-5 w-5" />}
              />
            </div>
          </div>

          <div className="rounded-[28px] border border-white/10 bg-white/5 p-6 shadow-panel backdrop-blur-xl">
            <div className="flex flex-wrap gap-2">
              {sectorPreview.map((sector) => (
                <span key={sector} className="rounded-full border border-white/10 bg-white/5 px-3 py-2 font-mono text-xs text-white/70">
                  {sector}
                </span>
              ))}
            </div>

            <div className="mt-5 rounded-[24px] border border-bronze/20 bg-gradient-to-br from-bronze/15 to-white/5 p-5">
              <h2 className="text-lg font-semibold">Why this shape works</h2>
              <p className="mt-3 leading-7 text-white/70">
                Recent production discussions consistently point to stale retrieval, weak business memory, and missing
                controls as the failure points. This starter bakes in those concerns from day one with citations, action
                planning, and multi-vertical adaptability.
              </p>
            </div>

            <div className="mt-5 grid gap-3 sm:grid-cols-2">
              <MiniStat label="Retrieval style" value="Hybrid lexical" />
              <MiniStat label="Agent mode" value="Answer + act" />
              <MiniStat label="Persistence" value="SQLite memory" />
              <MiniStat label="Frontend" value="Tailwind + React" />
            </div>
          </div>
        </section>

        <section className="mt-5 grid gap-5 lg:grid-cols-[0.92fr,1.08fr]">
          <div className="space-y-5">
            <Panel title="Industry Atlas" icon={<Globe2 className="h-5 w-5" />}>
              <div className="grid gap-3">
                <label className="text-sm text-white/70">Choose a vertical</label>
                <select
                  className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none"
                  value={selectedVertical}
                  onChange={(event) => setSelectedVertical(event.target.value)}
                >
                  {verticals.map((item) => (
                    <option key={item.slug} value={item.slug} className="bg-[#091017]">
                      {item.name} - {item.sector}
                    </option>
                  ))}
                </select>
              </div>
              <div className="mt-4 grid gap-3">
                {verticals.slice(0, 5).map((item) => (
                  <div key={item.slug} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <div className="flex items-center justify-between gap-3">
                      <strong>{item.name}</strong>
                      <span className="font-mono text-xs text-bronze">{item.sector}</span>
                    </div>
                    <p className="mt-2 text-sm leading-6 text-white/65">{item.short_description}</p>
                  </div>
                ))}
              </div>
            </Panel>

            <Panel title="Knowledge Import" icon={<UploadCloud className="h-5 w-5" />}>
              <div className="grid gap-3">
                <input
                  className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none"
                  value={importTitle}
                  onChange={(event) => setImportTitle(event.target.value)}
                  placeholder="Document title"
                />
                <textarea
                  className="min-h-40 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none"
                  value={importContent}
                  onChange={(event) => setImportContent(event.target.value)}
                />
                <div className="flex flex-wrap gap-3">
                  <button
                    className="rounded-full bg-gradient-to-r from-bronze to-[#efc17d] px-5 py-3 font-semibold text-[#111]"
                    onClick={importDocument}
                  >
                    Import knowledge
                  </button>
                  <button
                    className="rounded-full border border-white/15 bg-white/5 px-5 py-3 font-semibold text-white"
                    onClick={seedDemo}
                  >
                    Seed demo workspace
                  </button>
                </div>
                <p className="text-sm text-white/65">{status}</p>
              </div>
            </Panel>
          </div>

          <div className="space-y-5">
            <Panel title="Agentic Brain" icon={<MessageSquareQuote className="h-5 w-5" />}>
              <div className="grid gap-3">
                <textarea
                  className="min-h-28 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none"
                  value={message}
                  onChange={(event) => setMessage(event.target.value)}
                />
                <button
                  className="w-fit rounded-full bg-gradient-to-r from-mint to-[#8be6cf] px-5 py-3 font-semibold text-[#0b1515]"
                  onClick={sendChat}
                >
                  Run chat
                </button>
              </div>

              <div className="mt-5 grid gap-4">
                <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <strong>Intent</strong>
                    <span className="rounded-full border border-white/10 px-3 py-1 font-mono text-xs text-white/70">
                      {chat?.intent ?? "awaiting request"}
                    </span>
                  </div>
                  <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-white/75">
                    {chat?.answer ?? "Ask a question to see grounded retrieval, memory, and actions."}
                  </p>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <strong>Citations</strong>
                    <div className="mt-3 grid gap-3">
                      {(chat?.citations ?? []).length === 0 ? (
                        <p className="text-sm text-white/55">No citations yet.</p>
                      ) : (
                        chat?.citations.map((citation) => (
                          <div key={citation.chunk_id} className="rounded-2xl border border-white/10 bg-black/10 p-3">
                            <div className="flex items-center justify-between gap-2">
                              <span className="font-semibold">{citation.document_title}</span>
                              <span className="font-mono text-xs text-bronze">{citation.score.toFixed(2)}</span>
                            </div>
                            <p className="mt-2 text-sm leading-6 text-white/65">{citation.snippet}</p>
                          </div>
                        ))
                      )}
                    </div>
                  </div>

                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <strong>Planned Actions</strong>
                    <div className="mt-3 grid gap-3">
                      {(chat?.actions ?? []).length === 0 ? (
                        <p className="text-sm text-white/55">No actions yet.</p>
                      ) : (
                        chat?.actions.map((action) => (
                          <div key={`${action.type}-${action.label}`} className="rounded-2xl border border-white/10 bg-black/10 p-3">
                            <div className="flex items-center justify-between gap-2">
                              <span className="font-semibold">{action.label}</span>
                              <span className="font-mono text-xs text-mint">{action.type}</span>
                            </div>
                            <p className="mt-2 text-sm leading-6 text-white/65">{JSON.stringify(action.payload)}</p>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </Panel>
          </div>
        </section>
      </div>
    </main>
  );
}

function Panel(props: { title: string; icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <section className="rounded-[28px] border border-white/10 bg-white/5 p-6 shadow-panel backdrop-blur-xl">
      <div className="flex items-center gap-3">
        <div className="rounded-2xl border border-white/10 bg-white/5 p-3 text-bronze">{props.icon}</div>
        <h2 className="text-xl font-semibold tracking-[-0.02em]">{props.title}</h2>
      </div>
      <div className="mt-5">{props.children}</div>
    </section>
  );
}

function SignalCard(props: { label: string; value: string; icon: React.ReactNode }) {
  return (
    <div className="rounded-[24px] border border-white/10 bg-white/5 p-4">
      <div className="flex items-center justify-between gap-2 text-white/65">
        <span className="text-sm">{props.label}</span>
        <span className="text-bronze">{props.icon}</span>
      </div>
      <div className="mt-3 font-display text-3xl tracking-[-0.04em]">{props.value}</div>
    </div>
  );
}

function MiniStat(props: { label: string; value: string }) {
  return (
    <div className="rounded-[22px] border border-white/10 bg-white/5 p-4">
      <div className="text-sm text-white/65">{props.label}</div>
      <div className="mt-2 text-lg font-semibold">{props.value}</div>
    </div>
  );
}
