package example.reports;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import org.springframework.stereotype.Service;

@Service
public class ReportExportService {
    private final ReportRepository repository;
    private final FileStore fileStore;

    public ReportExportService(ReportRepository repository, FileStore fileStore) {
        this.repository = repository;
        this.fileStore = fileStore;
    }

    public CompletableFuture<String> export(long reportId) {
        return CompletableFuture.supplyAsync(() -> {
            var rows = repository.loadRows(reportId);
            return fileStore.writeCsv(reportId, rows);
        });
    }
}
