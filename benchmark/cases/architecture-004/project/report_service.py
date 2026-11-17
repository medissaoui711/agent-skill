class ReportApplicationService:
    def build_summary(self, request):
        account_id = request.user.account_id
        include_archived = request.GET.get("include_archived") == "1"
        return self.repository.fetch_summary(
            account_id=account_id,
            include_archived=include_archived,
        )
