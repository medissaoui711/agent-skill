import type { Request, Response } from "express";

export async function handleWebhook(req: Request, res: Response) {
  try {
    await processWebhook(req.body);
    res.sendStatus(204);
  } catch (error) {
    logger.error("Webhook processing failed", {
      error,
      headers: req.headers,
    });
    res.sendStatus(500);
  }
}
