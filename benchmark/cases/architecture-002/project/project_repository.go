package service

import (
    "database/sql"

    "github.com/gin-gonic/gin"
)

type SQLProjectRepository struct {
    db *sql.DB
}

func (r *SQLProjectRepository) ArchiveProject(ctx *gin.Context, projectID, actorID string) error {
    _, err := r.db.ExecContext(ctx.Request.Context(), "UPDATE projects SET archived = TRUE WHERE id = ? AND owner_id = ?", projectID, actorID)
    return err
}
