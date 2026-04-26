class ExpenseCalculatorService:

    @staticmethod
    def calculate_total(*x: float) -> float:
        return sum(x)

    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        if days <= 0:
            raise ValueError("Number of days must be greater than zero")
        return total / days
