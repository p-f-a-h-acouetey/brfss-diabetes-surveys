DATA_CONFIGS = {
    "bfrss_computed_vars": {
        "pattern": r"Section Name: Calculated Variables.*?SAS Variable Name:\s*(_?[A-Z0-9]+)",
        "vars_to_keep": ["_SEX", "_AGE80"],
    },
    "bfrss_record_identification_vars": {
        "pattern": r"Section Name: Record Identification.*?SAS Variable Name:\s*(_?[A-Z0-9]+)",
        "vars_to_keep": ["_STATE"],
    },
    "brfss_highly_imbalanced_vars": {"threshold": 0.995},
    "brfss_diabetes_vars": {
        "pattern": ".*DIAB.*",
        "var_to_keep": "DIABETE4",
        "values_map": {1.0: 2, 4.0: 1, 3.0: 0},
        "values_to_keep": [0, 1, 2],
    },
    "brfss_categorical_vars": {"threshold": 100},
    "brfss_vars_with_missing_values": {"threshold": 0.03},
}
