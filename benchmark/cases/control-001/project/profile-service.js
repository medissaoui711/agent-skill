const ALLOWED_FIELDS = new Set(["displayName", "locale"]);

export async function updateProfile(userId, input, repository) {
  const entries = Object.entries(input);
  if (entries.some(([key]) => !ALLOWED_FIELDS.has(key))) {
    return { ok: false, status: 400 };
  }
  const changes = Object.fromEntries(entries);
  if (Object.keys(changes).length === 0) {
    return { ok: false, status: 400 };
  }
  const updated = await repository.updateByUserId(userId, changes);
  if (!updated) return { ok: false, status: 404 };
  return { ok: true, profile: updated };
}
