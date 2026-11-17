package pricing

import "errors"

var ErrInvalidInput = errors.New("invalid input")

func CalculateSubtotal(unitPriceCents int64, quantity int64) (int64, error) {
	if unitPriceCents < 0 || quantity < 0 {
		return 0, ErrInvalidInput
	}
	return unitPriceCents * quantity, nil
}
