export interface CaptureJob {
  idempotencyKey: string;
  amountCents: number;
}

export async function processCapture(
  job: CaptureJob,
  jobs: JobRepository,
  payments: PaymentGateway,
): Promise<CaptureResult> {
  const existing = await jobs.findByIdempotencyKey(job.idempotencyKey);
  if (existing?.status === "completed") return existing.result;
  const result = await payments.capture(job.amountCents, job.idempotencyKey);
  await jobs.markCompleted(job.idempotencyKey, result);
  return result;
}
