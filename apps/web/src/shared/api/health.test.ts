import { afterEach, describe, expect, it, vi } from "vitest";
import { axiosInstance } from "@/shared/api/axiosInstance";
import { getHealth } from "@/shared/api/health";

function answerWith(data: unknown) {
  vi.spyOn(axiosInstance, "get").mockResolvedValue({ data });
}

describe("getHealth", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("returns the health reported by the api", async () => {
    answerWith({ status: "ok", transcriber: "unreachable" });

    await expect(getHealth()).resolves.toEqual({ status: "ok", transcriber: "unreachable" });
  });

  it.each([
    ["an html page", "<!doctype html><html><body></body></html>"],
    ["an empty body", ""],
    ["null", null],
    ["a json object without the expected fields", { message: "hello" }],
    ["an unknown api status", { status: "starting", transcriber: "ok" }],
    ["an unknown transcriber status", { status: "ok", transcriber: 1 }],
  ])("rejects when the body is %s", async (_description, body) => {
    answerWith(body);

    await expect(getHealth()).rejects.toThrow("Unexpected health response");
  });
});
