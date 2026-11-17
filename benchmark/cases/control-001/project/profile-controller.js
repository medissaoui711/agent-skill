import { updateProfile } from "./profile-service.js";

export async function patchMyProfile(req, res, repository) {
  const userId = req.user?.id;
  if (!userId) return res.status(401).end();
  const result = await updateProfile(userId, req.body ?? {}, repository);
  if (!result.ok) return res.status(result.status).end();
  return res.status(200).json(result.profile);
}
