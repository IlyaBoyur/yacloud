from .mixins import RepositoryDbLatencyMixin


class RepositoryStatistics(RepositoryDbLatencyMixin):
    pass


statistics_service = RepositoryStatistics()
