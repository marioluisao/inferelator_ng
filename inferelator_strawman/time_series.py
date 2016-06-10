import pandas as pd

class ResponseParameters:

    """Container for time series data for a gene in a condition
    Which may be used to determine the response value
    for that gene in the condition.
    """

    def __init__(self, gene_name, condition,
        gene_level_before, gene_level, time_interval):
        self.gene_name = gene_name
        self.condition = condition
        # level for gene in previous condition (or None if first)
        self.gene_level_before = gene_level_before
        # level for gene in this condition
        self.gene_level = gene_level
        self.time_interval = time_interval

class TransitionResponse:

    """
    The "y" response value for a gene in a condition in a time series.
    """
    # XXXX This is my reading of Greenfield et al. p1062.
    # -- it doesn't seem to correspond exactly to calculations in
    # https://github.com/ChristophH/Inferelator/blob/master/R_scripts/design_and_response.R
    # Therefore the current code is probably wrong.

    def __init__(self, tau_half_life):
        assert tau_half_life > 0, 'half life must be positive'
        # XXXX other restrictions on tau?
        self.tau_half_life = tau_half_life

    def gene_response(self, parameters):
        gene_level = 1.0 * parameters.gene_level
        gene_level_before = parameters.gene_level_before
        if gene_level_before is None:
            # first condition is assumed to be in a steady state.
            return gene_level
        # otherwise compute finite difference
        tau = self.tau_half_life
        interval = parameters.time_interval
        assert interval > 0, "time interval must be positive."
        level_change = 1.0 * (gene_level - gene_level_before)
        # XXXX is this right?
        result = (level_change/interval) + (gene_level / tau)
        return result

class TimeSeries:

    """
    A time series is a sequence of conditions separated by time intervals.
    """

    def __init__(self, first_condition):
        first_condition_name = first_condition.name
        self.first_condition_name = first_condition_name
        self._condition_name_to_next_condition_name = {}
        self._conditions_by_name = {first_condition_name: first_condition}
        self._time_interval_before_condition = {}
        self._condition_name_order = None
        self._time_interval_order = None

    def get_response_parameters(self, condition_name, gene_name):
        names = self.get_condition_name_order()
        intervals = self.get_interval_order()
        condition = self._conditions_by_name[condition_name]
        index = names.index(condition_name)
        interval = intervals[index]
        gene_level = condition.response_scalar(gene_name)
        gene_level_before = None
        if index > 0:
            condition_before = self._conditions_by_name[names[index-1]]
            gene_level_before = condition_before.response_scalar(gene_name)
        return ResponseParameters(gene_name, condition_name,
            gene_level_before, gene_level, interval)
        
    def get_condition_name_order(self, force=False):
        if not force and self._condition_name_order is not None:
            return self._condition_name_order
        conditions_seen = set()
        this_condition = self.first_condition_name
        name_order = []
        next_condition = self._condition_name_to_next_condition_name
        interval_before = self._time_interval_before_condition
        interval_order = [0]  # no time elapsed before first condition (?)
        while this_condition is not None:
            conditions_seen.add(this_condition)
            name_order.append(this_condition)
            this_condition = next_condition.get(this_condition)
            assert this_condition not in conditions_seen, (
                "Cycle found in timeseries condition description. " + repr((name_order, this_condition)))
            if this_condition is not None:
                interval = interval_before[this_condition]   # raises KeyError if missing.
                interval_order.append(interval)
        assert set(self._conditions_by_name) == conditions_seen, (
            "not all conditions ordered:" + 
            repr((set(self._conditions_by_name), conditions_seen)))
        self._condition_name_order = name_order
        self._time_interval_order = interval_order
        return name_order

    def get_condition_order(self):
        cbn = self._conditions_by_name
        name_order = self.get_condition_name_order()
        return [cbn[name] for name in name_order]
        
    def get_interval_order(self):
        self.get_condition_name_order()
        return self._time_interval_order
        
    def add_condition(self, prev_condition_name, condition, time_interval_before_condition):
        assert self._condition_name_order is None, (
            "Cannot modify time series after it has been compiled into an ordered sequence."
        )
        name = condition.name
        assert name not in self._conditions_by_name, (
            "duplicate condition: " + repr(name)
        )
        self._conditions_by_name[name] = condition
        self._time_interval_before_condition[name] = time_interval_before_condition
        assert prev_condition_name not in self._condition_name_to_next_condition_name, (
            "duplicate following condition " + repr(prev_condition_name, name)
        )
        self._condition_name_to_next_condition_name[prev_condition_name] = name
 