package proxy

import (
    "io"
    "net/http"
)

type Handler struct {
    client *http.Client
}

func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    upstream, err := http.NewRequestWithContext(r.Context(), http.MethodGet, r.URL.Query().Get("target"), nil)
    if err != nil {
        http.Error(w, "invalid request", http.StatusBadRequest)
        return
    }

    response, err := h.client.Do(upstream)
    if err != nil {
        http.Error(w, "upstream unavailable", http.StatusBadGateway)
        return
    }

    w.WriteHeader(response.StatusCode)
    _, _ = io.Copy(w, response.Body)
}
