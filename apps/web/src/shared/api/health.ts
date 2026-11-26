import { axiosInstance } from "@/shared/api/axiosInstance";

export const ServiceStatus = {
  Ok: "ok",
  Unreachable: "unreachable",
} as const;

export type ServiceStatus = (typeof ServiceStatus)[keyof typeof ServiceStatus];

export type Health = {
  status: typeof ServiceStatus.Ok;
  transcriber: ServiceStatus;
};

function isServiceStatus(value: unknown): value is ServiceStatus {
  return Object.values(ServiceStatus).some((status) => status === value);
}

function isHealth(value: unknown): value is Health {
  if (typeof value !== "object" || value === null) {
    return false;
  }
  const candidate = value as Record<string, unknown>;
  return candidate.status === ServiceStatus.Ok && isServiceStatus(candidate.transcriber);
}

/**
 * Asks the API for its health. Rejects when the request fails and also when the answer
 * is not a health report: a 200 can come from something other than the API, for example
 * the app's own index.html served for a misrouted request.
 */
export async function getHealth(): Promise<Health> {
  const response = await axiosInstance.get<unknown>("/health");
  if (!isHealth(response.data)) {
    throw new Error("Unexpected health response");
  }
  return response.data;
}
