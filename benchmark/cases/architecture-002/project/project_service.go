package service

import (
    "errors"

    "github.com/gin-gonic/gin"
)

type ProjectRepository interface {
    ArchiveProject(ctx *gin.Context, projectID, actorID string) error
}

type ProjectService struct {
    repo ProjectRepository
}

func (s *ProjectService) ArchiveProject(ctx *gin.Context, projectID string) error {
    actorID := ctx.GetString("actorID")
    if actorID == "" {
        return errors.New("missing actor")
    }
    return s.repo.ArchiveProject(ctx, projectID, actorID)
}
