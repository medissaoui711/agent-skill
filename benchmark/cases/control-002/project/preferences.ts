import { Router, Request, Response } from "express";

type Preference = "email" | "sms" | "none";
type AuthenticatedRequest = Request & { user: { id: string } };

const preferences = new Map<string, Preference>();
const allowed = new Set<Preference>(["email", "sms", "none"]);

export const router = Router();

router.patch("/me/notification-preference", (req: Request, res: Response) => {
  const authenticated = req as AuthenticatedRequest;
  const value: unknown = req.body?.preference;

  if (typeof value !== "string" || !allowed.has(value as Preference)) {
    return res.status(400).json({ error: "invalid preference" });
  }

  preferences.set(authenticated.user.id, value as Preference);
  return res.status(204).end();
});
