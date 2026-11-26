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

export async function getHealth(): Promise<Health> {
  const response = await axiosInstance.get<Health>("/health");
  return response.data;
}
