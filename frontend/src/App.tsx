import { useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowUpRight,
  Brain,
  Database,
  Eye,
  Lock,
  Network,
  RefreshCw,
  Shield,
  Terminal,
} from "lucide-react";
import "./App.css";

type EventType =
  | "session_event"
  | "key_event"
  | "network_event"
  | "focus_event";

type LabEvent = {
  id: number;
  type: EventType;
  source: string;
  status: "NORMAL" | "DETECTED";
  detail: string;
  time: string;
};

type Finding = {
  rule_id: string;
  severity: string;
  score: number;
  title: string;
  description: string;
};

const demoEvents = [
  {
    event_type: "session_event",
    data: { state: "STARTED" },
  },
  {
    event_type: "key_event",
    data: {
      key_category: "ALPHANUMERIC",
      action: "DOWN",
      dwell_ms: 25,
    },
  },
  {
    event_type: "network_event",
    data: {
      destination_type: "SIMULATED_C2",
    },
  },
  {
    event_type: "focus_event",
    data: { state: "ACTIVE" },
  },
];

const initialEvents: LabEvent[] = [
  {
    id: 12,
    type: "network_event",
    source: "lab-simulator",
    status: "DETECTED",
    detail: "Simulated C2 communication",
    time: "16:07:31",
  },
  {
    id: 11,
    type: "key_event",
    source: "lab-simulator",
    status: "DETECTED",
    detail: "High-frequency simulated input",
    time: "16:07:30",
  },
  {
    id: 10,
    type: "key_event",
    source: "lab-simulator",
    status: "NORMAL",
    detail: "Authorized simulated key event",
    time: "16:07:29",
  },
  {
    id: 9,
    type: "session_event",
    source: "lab-simulator",
    status: "NORMAL",
    detail: "Session initialized",
    time: "16:07:28",
  },
];

function App() {
  const [events, setEvents] = useState(initialEvents);
  const [running, setRunning] = useState(false);
  const [riskScore, setRiskScore] = useState(65);
  const [severity, setSeverity] = useState("HIGH");
  const [findings, setFindings] = useState<Finding[]>([
    {
      rule_id: "SYL-NET-001",
      severity: "HIGH",
      score: 40,
      title: "Simulated C2 communication",
      description:
        "Network telemetry matched the simulated command-and-control rule.",
    },
    {
      rule_id: "SYL-KB-001",
      severity: "MEDIUM",
      score: 25,
      title: "High-frequency key activity",
      description:
        "Simulated input activity exceeded the configured behavioral threshold.",
    },
  ]);
  const [eventsAnalyzed, setEventsAnalyzed] = useState(4);

  const detected = useMemo(
    () => events.filter((event) => event.status === "DETECTED").length,
    [events]
  );

  const runAnalysis = async () => {
    setRunning(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          events: demoEvents,
        }),
      });

      if (!response.ok) {
        throw new Error("API request failed");
      }

      const result = await response.json();

      setRiskScore(result.detection.risk.score);
      setSeverity(result.detection.risk.severity);
      setFindings(result.detection.findings);
      setEventsAnalyzed(result.detection.events_analyzed);

      const now = new Date().toLocaleTimeString([], {
        hour12: false,
      });

      setEvents([
        {
          id: Date.now(),
          type: "network_event",
          source: "detection-engine",
          status: "DETECTED",
          detail: "Behavioral pattern confirmed",
          time: now,
        },
        ...initialEvents,
      ]);
    } catch (error) {
      console.error("SYLTHEN API error:", error);
      alert(
        "Could not connect to SYLTHEN backend. Make sure FastAPI is running on port 8000."
      );
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <Shield size={22} />
          </div>

          <div>
            <h1>SYLTHEN</h1>
            <span>SECURITY LAB</span>
          </div>
        </div>

        <nav>
          <button className="nav-item active">
            <Activity size={18} />
            Overview
          </button>

          <button className="nav-item">
            <Terminal size={18} />
            Telemetry
          </button>

          <button className="nav-item">
            <AlertTriangle size={18} />
            Detections
            <span className="nav-count">{detected}</span>
          </button>

          <button className="nav-item">
            <Brain size={18} />
            Behavioral Analysis
          </button>

          <button className="nav-item">
            <Database size={18} />
            Evidence
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="system-status">
            <span className="status-dot" />
            <div>
              <strong>Core operational</strong>
              <small>All systems nominal</small>
            </div>
          </div>

          <span className="version">SYLTHEN v1.0.0</span>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <p className="eyebrow">
              ETHICAL SPYWARE SIMULATION & DETECTION
            </p>
            <h2>Security Overview</h2>
          </div>

          <div className="topbar-actions">
            <span className="live-indicator">
              <span className="status-dot" />
              LAB SESSION ACTIVE
            </span>

            <button
              className="analysis-button"
              onClick={runAnalysis}
              disabled={running}
            >
              <RefreshCw
                size={16}
                className={running ? "spin" : ""}
              />
              {running ? "Analyzing..." : "Run Analysis"}
            </button>
          </div>
        </header>

        <section className="hero-grid">
          <div className="risk-card">
            <div className="card-heading">
              <div>
                <span className="label">CURRENT RISK</span>
                <h3>{severity}</h3>
              </div>

              <div className="risk-icon">
                <AlertTriangle size={20} />
              </div>
            </div>

            <div className="score">
              <strong>{riskScore}</strong>
              <span> / 100</span>
            </div>

            <div className="risk-bar">
              <div
                className="risk-fill"
                style={{ width: `${riskScore}%` }}
              />
            </div>

            <div className="risk-footer">
              <span>{findings.length} active findings</span>
              <span className="up">
                <ArrowUpRight size={14} />
                {findings.length > 0
                  ? `+${Math.max(...findings.map((f) => f.score))}`
                  : "+0"}
              </span>
            </div>
          </div>

          <StatCard
            icon={<Activity size={19} />}
            label="EVENTS ANALYZED"
            value={String(eventsAnalyzed)}
            detail="Current session"
          />

          <StatCard
            icon={<AlertTriangle size={19} />}
            label="DETECTIONS"
            value={String(findings.length)}
            detail="Requires review"
          />

          <StatCard
            icon={<Lock size={19} />}
            label="ENCRYPTION"
            value="AES-256"
            detail="Authenticated storage"
          />
        </section>

        <section className="content-grid">
          <div className="panel events-panel">
            <div className="panel-header">
              <div>
                <span className="label">LIVE TELEMETRY</span>
                <h3>Event Stream</h3>
              </div>

              <span className="event-count">
                {events.length} EVENTS
              </span>
            </div>

            <div className="events-table">
              <div className="table-head">
                <span>EVENT</span>
                <span>SOURCE</span>
                <span>STATUS</span>
                <span>TIME</span>
              </div>

              {events.map((event) => (
                <div className="event-row" key={event.id}>
                  <div className="event-name">
                    <EventIcon type={event.type} />
                    <div>
                      <strong>{formatEvent(event.type)}</strong>
                      <small>{event.detail}</small>
                    </div>
                  </div>

                  <span className="muted">{event.source}</span>

                  <span
                    className={`badge ${
                      event.status === "DETECTED"
                        ? "danger"
                        : "normal"
                    }`}
                  >
                    {event.status}
                  </span>

                  <span className="muted">{event.time}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="panel findings-panel">
            <div className="panel-header">
              <div>
                <span className="label">DETECTION ENGINE</span>
                <h3>Findings</h3>
              </div>

              <span className="engine-status">ACTIVE</span>
            </div>

            {findings.map((finding) => (
              <FindingCard
                key={finding.rule_id}
                severity={finding.severity}
                score={`+${finding.score}`}
                title={finding.title}
                description={finding.description}
              />
            ))}
          </div>
        </section>

        <section className="bottom-grid">
          <div className="panel architecture-panel">
            <div className="panel-header">
              <div>
                <span className="label">SYSTEM PIPELINE</span>
                <h3>Security Architecture</h3>
              </div>
            </div>

            <div className="pipeline">
              <PipelineItem icon={<Terminal />} text="Telemetry" />
              <span className="connector">→</span>
              <PipelineItem icon={<Lock />} text="Encryption" />
              <span className="connector">→</span>
              <PipelineItem icon={<Database />} text="Storage" />
              <span className="connector">→</span>
              <PipelineItem icon={<Brain />} text="Detection" />
              <span className="connector">→</span>
              <PipelineItem icon={<Eye />} text="Analysis" />
            </div>
          </div>

          <div className="panel session-panel">
            <span className="label">SESSION</span>
            <h3>demo-session-001</h3>

            <div className="session-info">
              <div>
                <span>STATUS</span>
                <strong>AUTHORIZED LAB</strong>
              </div>

              <div>
                <span>STORAGE</span>
                <strong>SQLITE</strong>
              </div>

              <div>
                <span>INTEGRITY</span>
                <strong>VERIFIED</strong>
              </div>
            </div>
          </div>
        </section>

        <footer>
          <span>SYLTHEN • Ethical Security Research Framework</span>
          <span>Authorized laboratory telemetry only</span>
        </footer>
      </main>
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
  detail,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  detail: string;
}) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <span className="label">{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </div>
  );
}

function FindingCard({
  severity,
  score,
  title,
  description,
}: {
  severity: string;
  score: string;
  title: string;
  description: string;
}) {
  return (
    <div className="finding">
      <div className="severity-line" />
      <div className="finding-main">
        <div className="finding-top">
          <span className={`severity ${severity.toLowerCase()}`}>
            {severity}
          </span>
          <span className="finding-score">{score}</span>
        </div>

        <strong>{title}</strong>
        <p>{description}</p>
      </div>
    </div>
  );
}

function PipelineItem({
  icon,
  text,
}: {
  icon: React.ReactNode;
  text: string;
}) {
  return (
    <div className="pipeline-item">
      {icon}
      <span>{text}</span>
    </div>
  );
}

function EventIcon({ type }: { type: EventType }) {
  if (type === "network_event") {
    return <Network size={17} />;
  }

  if (type === "key_event") {
    return <Terminal size={17} />;
  }

  return <Activity size={17} />;
}

function formatEvent(type: EventType) {
  return type
    .replace("_event", "")
    .replace("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

export default App;