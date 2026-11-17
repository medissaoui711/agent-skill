package documents

import (
	"encoding/json"
	"net/http"
)

type Principal struct {
	UserID string
}

type Document struct {
	ID        string `json:"id"`
	ProjectID string `json:"projectId"`
	Body      string `json:"body"`
}

type Repository interface {
	FindDocument(projectID, documentID string) (Document, error)
}

type Handler struct {
	Repo Repository
}

func (h Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	principal, ok := r.Context().Value("principal").(Principal)
	if !ok || principal.UserID == "" {
		http.Error(w, "unauthorized", http.StatusUnauthorized)
		return
	}

	projectID := r.PathValue("projectID")
	documentID := r.PathValue("documentID")
	document, err := h.Repo.FindDocument(projectID, documentID)
	if err != nil {
		http.NotFound(w, r)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(document)
}
