package reports

import (
    "context"
    "net/http"
)

type Repository interface {
    Load(ctx context.Context, id string) ([]byte, error)
}
type Renderer interface {
    Render(ctx context.Context, input []byte) ([]byte, error)
}

type Handler struct {
    repository Repository
    renderer Renderer
}

func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    input, err := h.repository.Load(ctx, r.URL.Query().Get("id"))
    if err != nil {
        http.Error(w, "report unavailable", http.StatusBadGateway)
        return
    }
    output, err := h.renderer.Render(ctx, input)
    if err != nil {
        http.Error(w, "report unavailable", http.StatusBadGateway)
        return
    }
    w.Header().Set("Content-Type", "application/pdf")
    _, _ = w.Write(output)
}
