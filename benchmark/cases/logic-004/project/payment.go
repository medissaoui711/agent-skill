package payments

import (
	"encoding/json"
	"net/http"
)

type CaptureRequest struct {
	PaymentID string `json:"paymentId"`
}

type Provider interface {
	Capture(paymentID string) error
}

type Audit interface {
	RecordFailure(paymentID string, cause error)
}

type Handler struct {
	Provider Provider
	Audit    Audit
}

func (h Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	var input CaptureRequest
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		http.Error(w, "invalid request", http.StatusBadRequest)
		return
	}

	err := h.Provider.Capture(input.PaymentID)
	if err != nil {
		h.Audit.RecordFailure(input.PaymentID, err)
	}

	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte(`{"status":"captured"}`))
}
