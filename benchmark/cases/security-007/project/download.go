package files

import (
    "net/http"
    "path/filepath"
)

const storageRoot = "/srv/app/documents"

func Download(w http.ResponseWriter, r *http.Request) {
    name := r.URL.Query().Get("name")
    path := filepath.Join(storageRoot, name)
    http.ServeFile(w, r, path)
}
