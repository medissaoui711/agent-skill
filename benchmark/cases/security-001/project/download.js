import path from "node:path";
import { readFile } from "node:fs/promises";
import { findDocument } from "./repository.js";

const DOCUMENT_ROOT = path.resolve(process.cwd(), "private-documents");

export async function downloadDocument(req, res) {
  const documentName = req.params.documentName;
  const document = await findDocument(documentName);

  if (!document || document.ownerId !== req.user.id) {
    return res.status(404).end();
  }

  const filePath = path.join(DOCUMENT_ROOT, documentName);
  const contents = await readFile(filePath);

  res.type("application/octet-stream").send(contents);
}
