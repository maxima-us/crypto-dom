from hypothesis import HealthCheck, Verbosity


DEADLINE = 10000
MAX_EXAMPLES = 5
SUPPRESS_HEALTH_CHECK = (HealthCheck.too_slow,)
VERBOSITY = Verbosity.verbose