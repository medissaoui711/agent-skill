package worker

import "context"

type Job struct {
	ID string
}

type Processor interface {
	Process(context.Context, Job) error
}

type Worker struct {
	queue     Queue
	processor Processor
}

func (w *Worker) Run(ctx context.Context) error {
	for {
		job, err := w.queue.Next(ctx)
		if err != nil {
			return err
		}
		if err := w.processor.Process(context.Background(), job); err != nil {
			return err
		}
	}
}
