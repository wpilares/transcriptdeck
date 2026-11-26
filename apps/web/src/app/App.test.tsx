import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "@/app/App";
import { axiosInstance } from "@/shared/api/axiosInstance";
import { getHealth } from "@/shared/api/health";

vi.mock("@/shared/api/health", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@/shared/api/health")>()),
  getHealth: vi.fn(),
}));

const getHealthMock = vi.mocked(getHealth);

describe("App", () => {
  beforeEach(() => {
    getHealthMock.mockReset();
    vi.restoreAllMocks();
  });

  it("shows the app name", () => {
    getHealthMock.mockReturnValue(new Promise(() => {}));

    render(<App />);

    expect(screen.getByRole("heading", { name: "TranscriptDeck" })).toBeInTheDocument();
  });

  it("shows both services as ok when the api and the transcriber answer", async () => {
    getHealthMock.mockResolvedValue({ status: "ok", transcriber: "ok" });

    render(<App />);

    expect(await screen.findByText("API: ok")).toBeInTheDocument();
    expect(screen.getByText("Transcriber: ok")).toBeInTheDocument();
  });

  it("shows the transcriber as unreachable when the api cannot reach it", async () => {
    getHealthMock.mockResolvedValue({ status: "ok", transcriber: "unreachable" });

    render(<App />);

    expect(await screen.findByText("Transcriber: unreachable")).toBeInTheDocument();
    expect(screen.getByText("API: ok")).toBeInTheDocument();
  });

  it("shows the api as unreachable when the health request fails", async () => {
    getHealthMock.mockRejectedValue(new Error("Network Error"));

    render(<App />);

    expect(await screen.findByText("API: unreachable")).toBeInTheDocument();
    expect(screen.getByText("Transcriber: unknown")).toBeInTheDocument();
  });

  it("shows the api as unreachable when the answer is not a health report", async () => {
    const { getHealth: realGetHealth } =
      await vi.importActual<typeof import("@/shared/api/health")>("@/shared/api/health");
    getHealthMock.mockImplementation(realGetHealth);
    vi.spyOn(axiosInstance, "get").mockResolvedValue({
      data: "<!doctype html><html><body></body></html>",
    });

    render(<App />);

    expect(await screen.findByText("API: unreachable")).toBeInTheDocument();
    expect(screen.getByText("Transcriber: unknown")).toBeInTheDocument();
  });
});
