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

export async function getHealth(): Promise<Health> {
  const response = await axiosInstance.get<unknown>("/health");
  if (!isHealth(response.data)) {
    throw new Error("Unexpected health response");
  }
  return response.data;
}
