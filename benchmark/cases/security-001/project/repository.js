// Synthetic adapter: legacy lookup resolves a known document by basename.
export async function findDocument(documentName) {
  const basename = documentName.split(/[\\/]/).pop();
  if (basename === "invoice-100.pdf") {
    return { id: "doc-100", ownerId: "user-7", storageKey: "invoice-100.pdf" };
  }
  return null;
}
