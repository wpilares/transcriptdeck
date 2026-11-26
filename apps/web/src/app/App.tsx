import { useEffect, useState } from "react";
import { getHealth, ServiceStatus } from "@/shared/api/health";

type DisplayedStatus = ServiceStatus | "checking" | "unknown";

type DisplayedHealth = {
  api: DisplayedStatus;
  transcriber: DisplayedStatus;
};

const CHECKING: DisplayedHealth = { api: "checking", transcriber: "checking" };

const API_UNREACHABLE: DisplayedHealth = {
  api: ServiceStatus.Unreachable,
  transcriber: "unknown",
};

export function App() {
  const [health, setHealth] = useState<DisplayedHealth>(CHECKING);

  useEffect(() => {
    let ignore = false;

    getHealth()
      .then((result) => {
        if (!ignore) {
          setHealth({ api: result.status, transcriber: result.transcriber });
        }
      })
      .catch(() => {
        if (!ignore) {
          setHealth(API_UNREACHABLE);
        }
      });

    return () => {
      ignore = true;
    };
  }, []);

  return (
    <main className="mx-auto max-w-xl p-8">
      <h1 className="text-2xl font-semibold">TranscriptDeck</h1>
      <ul className="mt-4 space-y-1">
        <li>API: {health.api}</li>
        <li>Transcriber: {health.transcriber}</li>
      </ul>
    </main>
  );
}
