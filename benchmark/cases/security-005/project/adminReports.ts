import { Router, Request, Response, NextFunction } from "express";

const router = Router();

async function reportHandler(req: Request, res: Response) {
    const report = await reportRepository.findById(req.params.reportId);
    if (!report) return res.sendStatus(404);
    return res.json(report);
}

router.get("/admin/reports/:reportId", reportHandler);
router.use(authenticate);
router.use("/admin", requireRole("admin"));

export default router;
