from dataclasses import dataclass


@dataclass
class MLProblemDefinition:
    name: str
    target: str
    metric: str


def define_sales_forecast_problem() -> MLProblemDefinition:
    return MLProblemDefinition(
        name="30 günlük satış tahmini",
        target="next_30_day_sales",
        metric="MAE",
    )