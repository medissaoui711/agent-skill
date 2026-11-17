package example.audit;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class AuditLogger {
    private static final Logger log = LoggerFactory.getLogger(AuditLogger.class);

    public void record(String actorId, String action, String targetId) {
        log.info("audit actorId={} action={} targetId={}", actorId, action, targetId);
    }
}
