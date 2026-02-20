import numpy as np

CLEANING_CONFIGS = {
    "DRNKANY6": {
        "type": "np_select",
        "conditions": ["df['DRNKANY6'] == 1.0", "df['DRNKANY6'] == 2.0"],
        "choices": ["yes", "no"],
        "new_name": "did_you_have_at_least_1drink_in_last_30days",
        "dtypes": "str",
    },
    "DROCDY4_": {
        "type": "np_select",
        "conditions": ["df['DROCDY4_'] == 0.0", "df['DROCDY4_'].between(1.0, 899.0)"],
        "choices": ["no", "yes"],
        "new_name": "at_least_1drink_occasion_per_day",
        "dtypes": "str",
    },
    "_AGE65YR": {
        "type": "np_select",
        "conditions": ["df['_AGE65YR'] == 1.0", "df['_AGE65YR'] == 2.0"],
        "choices": ["18-64", "65-99"],
        "new_name": "age_in_2groups",
        "dtypes": "str",
    },
    "_AGE80": {"type": None, "new_name": "imputed_age", "dtypes": "Int64"},
    "_AGEG5YR": {
        "type": "np_select",
        "conditions": [
            "df['_AGEG5YR'] == 1.0",  # 18-24
            "df['_AGEG5YR'] == 2.0",  # 25-29
            "df['_AGEG5YR'] == 3.0",  # 30-34
            "df['_AGEG5YR'] == 4.0",  # 35-39
            "df['_AGEG5YR'] == 5.0",  # 40-44
            "df['_AGEG5YR'] == 6.0",  # 45-49
            "df['_AGEG5YR'] == 7.0",  # 50-54
            "df['_AGEG5YR'] == 8.0",  # 55-59
            "df['_AGEG5YR'] == 9.0",  # 60-64
            "df['_AGEG5YR'] == 10.0",  # 65-69
            "df['_AGEG5YR'] == 11.0",  # 70-74
            "df['_AGEG5YR'] == 12.0",  # 75-79
            "df['_AGEG5YR'] == 13.0",  # 80+
        ],
        "choices": [
            "18-24",
            "25-29",
            "30-34",
            "35-39",
            "40-44",
            "45-49",
            "50-54",
            "55-59",
            "60-64",
            "65-69",
            "70-74",
            "75-79",
            "80+",
        ],
        "new_name": "age_in_14groups",
        "dtypes": "str",
    },
    "_AGE_G": {
        "type": "np_select",
        "conditions": [
            "df['_AGE_G'] == 1.0",  # 18-24
            "df['_AGE_G'] == 2.0",  # 25-34
            "df['_AGE_G'] == 3.0",  # 35-44
            "df['_AGE_G'] == 4.0",  # 45-54
            "df['_AGE_G'] == 5.0",  # 55-64
            "df['_AGE_G'] == 6.0",  # 65+
        ],
        "choices": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
        "new_name": "imputed_age_in_6groups",
        "dtypes": "str",
    },
    "_ASTHMS1": {
        "type": "np_select",
        "conditions": [
            "df['_ASTHMS1'] == 1.0",  # Having asthma currently
            "df['_ASTHMS1'] == 2.0",  # Had asthma, but not anymore
            "df['_ASTHMS1'] == 3.0",  # Never had asthma
        ],
        "choices": ["currently", "formerly", "never"],
        "new_name": "do_you_have_asthma",
        "dtypes": "str",
    },
    "_CASTHM1": {
        "type": "np_select",
        "conditions": [
            "df['_CASTHM1'] == 1.0",  # No
            "df['_CASTHM1'] == 2.0",  # Yes
        ],
        "choices": ["no", "yes"],
        "new_name": "have_you_currently_been_told_to_have_asthma",
        "dtypes": "str",
    },
    "_CHLDCNT": {
        "type": "np_select",
        "conditions": [
            "df['_CHLDCNT'] == 1.0",  # 0 child
            "df['_CHLDCNT'] == 2.0",  # 1 child
            "df['_CHLDCNT'] == 3.0",  # 2 children
            "df['_CHLDCNT'] == 4.0",  # 3 children
            "df['_CHLDCNT'] == 5.0",  # 4 children
            "df['_CHLDCNT'] == 6.0",  # 5+ children
        ],
        "choices": ["0", "1", "2", "3", "4", "5+"],
        "new_name": "children_count_categories",
        "dtypes": "str",
    },
    "_CURECI3": {
        "type": "np_select",
        "conditions": [
            "df['_CURECI3'] == 1.0",  # No
            "df['_CURECI3'] == 2.0",  # Yes
        ],
        "choices": ["no", "yes"],
        "new_name": "are_you_currently_an_ecigars_user",
        "dtypes": "str",
    },
    "_DENVST3": {
        "type": "np_select",
        "conditions": [
            "df['_DENVST3'] == 1.0",  # Yes
            "df['_DENVST3'] == 2.0",  # No
        ],
        "choices": ["yes", "no"],
        "new_name": "have_you_ever_visited_for_dental_problems_within_last_year",
        "dtypes": "str",
    },
    "_DRNKWK3": {
        "type": "np_where",
        "condition": "df['_DRNKWK3'] == 99900.0",
        "true_value": np.nan,
        "new_name": "weekly_number_of_alcoholic_drinks",
        "dtypes": "Int64",
    },
    "_EDUCAG": {
        "type": "np_select",
        "conditions": [
            "df['_EDUCAG'] == 1.0",  # < High School
            "df['_EDUCAG'] == 2.0",  # High School
            "df['_EDUCAG'] == 3.0",  # < College / Technical School
            "df['_EDUCAG'] == 4.0",  # College / Technical School
        ],
        "choices": [
            "< high school",
            "high school",
            "< college / technical school",
            "college / technical school",
        ],
        "new_name": "education_level_completed",
        "dtypes": "str",
    },
    "_EXTETH3": {
        "type": "np_select",
        "conditions": [
            "df['_EXTETH3'] == 1.0",  # No
            "df['_EXTETH3'] == 2.0",  # Yes
        ],
        "choices": ["no", "yes"],
        "new_name": "have_you_had_permanent_teeth_extracted",
        "dtypes": "str",
    },
    "_HCVU654": {
        "type": "np_select",
        "conditions": [
            "df['_HCVU654'] == 1.0",  # Yes
            "df['_HCVU654'] == 2.0",  # No
        ],
        "choices": ["yes", "no"],
        "new_name": "have_you_any_health_insurance",
        "dtypes": "str",
    },
    "_HLTHPL2": {
        "type": "np_select",
        "conditions": [
            "df['_HLTHPL2'] == 1.0",  # Yes
            "df['_HLTHPL2'] == 2.0",  # No
        ],
        "choices": ["yes", "no"],
        "new_name": "had_you_any_health_insurance",
        "dtypes": "str",
    },
    "_INCOMG1": {
        "type": "np_select",
        "conditions": [
            "df['_INCOMG1'] == 1.0",  # < 15K
            "df['_INCOMG1'] == 2.0",  # [15K, 25K[
            "df['_INCOMG1'] == 3.0",  # [25K, 35K[
            "df['_INCOMG1'] == 4.0",  # [35K, 50K[
            "df['_INCOMG1'] == 5.0",  # [50K, 100K[
            "df['_INCOMG1'] == 6.0",  # [100K, 200K[
            "df['_INCOMG1'] == 7.0",  # >= 200K
        ],
        "choices": [
            "< 15k",
            "[15k, 25k[",
            "[25k, 35k[",
            "[35k, 50k[",
            "[50k, 100k[",
            "[100k, 200k[",
            ">= 200k",
        ],
        "new_name": "income_categories",
        "dtypes": "str",
    },
    "_LCSAGE": {
        "type": "np_select",
        "conditions": [
            "df['_LCSAGE'] == 1.0",  # 18-49
            "df['_LCSAGE'] == 2.0",  # 50-80
            "df['_LCSAGE'] == 3.0",  # 81+
        ],
        "choices": ["18-49", "50-80", "81+"],
        "new_name": "age_imputed_in_3groups",
        "dtypes": "str",
    },
    "_LTASTH1": {
        "type": "np_select",
        "conditions": [
            "df['_LTASTH1'] == 1.0",  # No
            "df['_LTASTH1'] == 2.0",  # Yes
        ],
        "choices": ["no", "yes"],
        "new_name": "have_you_formely_or_currently_been_told_to_have_asthma",
        "dtypes": "str",
    },
    "_MENT14D": {
        "type": "np_select",
        "conditions": [
            "df['_MENT14D'] == 1.0",  # 0days
            "df['_MENT14D'] == 2.0",  # 1-13days
            "df['_MENT14D'] == 3.0",  # 14+days
        ],
        "choices": ["0", "1-13", "14+"],
        "new_name": "bad_mental_health_days_categories",
        "dtypes": "str",
    },
    "_PHYS14D": {
        "type": "np_select",
        "conditions": [
            "df['_PHYS14D'] == 1.0",  # 0days
            "df['_PHYS14D'] == 2.0",  # 1-13days
            "df['_PHYS14D'] == 3.0",  # 14+days
        ],
        "choices": ["0", "1-13", "14+"],
        "new_name": "bad_physical_health_days_categories",
        "dtypes": "str",
    },
    "_RFBING6": {
        "type": "np_select",
        "conditions": [
            "df['_RFBING6'] == 1.0",  # No
            "df['_RFBING6'] == 2.0",  # Yes
        ],
        "choices": ["no", "yes"],
        "new_name": "are_you_a_binge_drinker",
        "dtypes": "str",
    },
    "_RFBMI5": {
        "type": "np_select",
        "conditions": [
            "df['_RFBMI5'] == 1.0",  # No
            "df['_RFBMI5'] == 2.0",  # Yes
        ],
        "choices": ["no", "yes"],
        "new_name": "are_you_overweight_or_obese",
        "dtypes": "str",
    },
    "_RFDRHV9": {
        "type": "np_select",
        "conditions": [
            "df['_RFDRHV9'] == 1.0",  # No
            "df['_RFDRHV9'] == 2.0",  # Yes
        ],
        "choices": ["no", "yes"],
        "new_name": "are_you_a_heavy_drinker",
        "dtypes": "str",
    },
    "_RFHLTH": {
        "type": "np_select",
        "conditions": [
            "df['_RFHLTH'] == 1.0",  # Good / Better
            "df['_RFHLTH'] == 2.0",  # Poor / Fair
        ],
        "choices": ["good / better", "poor / fair"],
        "new_name": "health_status",
        "dtypes": "str",
    },
    "_RFSMOK3": {
        "type": "np_select",
        "conditions": [
            "df['_RFSMOK3'] == 1.0",  # No
            "df['_RFSMOK3'] == 2.0",  # Yes
        ],
        "choices": ["no", "yes"],
        "new_name": "are_you_a_current_smoker",
        "dtypes": "str",
    },
    "_SEX": {
        "type": "np_select",
        "conditions": [
            "df['_SEX'] == 1.0",  # Male
            "df['_SEX'] == 2.0",  # Female
        ],
        "choices": ["man", "woman"],
        "new_name": "sex",
        "dtypes": "str",
    },
    "_SMOKER3": {
        "type": "np_select",
        "conditions": [
            "df['_SMOKER3'] == 1.0",  # Everyday smoker
            "df['_SMOKER3'] == 2.0",  # Someday smoker
            "df['_SMOKER3'] == 3.0",  # Former smoker
            "df['_SMOKER3'] == 4.0",  # Non-smoker
        ],
        "choices": ["everyday smoker", "someday smoker", "former smoker", "non-smoker"],
        "new_name": "smoker_categories",
        "dtypes": "str",
    },
    "_TOTINDA": {
        "type": "np_select",
        "conditions": [
            "df['_TOTINDA'] == 1.0",  # Yes
            "df['_TOTINDA'] == 2.0",  # No
        ],
        "choices": ["yes", "no"],
        "new_name": "have_you_exercised_during_last_30days",
        "dtypes": "str",
    },
    "DIABETE4": {
        "type": "np_select",
        "conditions": [
            "df['DIABETE4'] == 1.0",  # diabetes
            "df['DIABETE4'] == 3.0",  # No diabetes
            "df['DIABETE4'] == 4.0",  # prediabetes
        ],
        "choices": ["diabetes", "no diabetes", "prediabetes"],
        "new_name": "diabetic_status",
        "dtypes": "str",
    },
    "CHECKUP1": {
        "type": "np_select",
        "conditions": [
            "df['CHECKUP1'] == 1.0",  # < 1yr
            "df['CHECKUP1'] == 2.0",  # [1, 2yrs[
            "df['CHECKUP1'] == 3.0",  # [2, 5yrs[
            "df['CHECKUP1'] == 4.0",  # 5yrs+
            "df['CHECKUP1'] == 8.0",  # Never
        ],
        "choices": ["< 1yr", "[1, 2yrs[", "[2, 5yrs[", "5yrs+", "never"],
        "new_name": "how_long_since_your_last_doctor_visit",
        "dtypes": "str",
    },
    "MEDCOST1": {
        "type": "np_select",
        "conditions": [
            "df['MEDCOST1'] == 1.0",  # Yes
            "df['MEDCOST1'] == 2.0",  # No
        ],
        "choices": ["yes", "no"],
        "new_name": "could_you_not_afford_a_doctor_once_in_last_30days",
        "dtypes": "str",
    },
    "PERSDOC3": {
        "type": "np_select",
        "conditions": [
            "df['PERSDOC3'] == 1.0",  # 1
            "df['PERSDOC3'] == 2.0",  # 1+
            "df['PERSDOC3'] == 3.0",  # 0
        ],
        "choices": ["1", "1+", "0"],
        "new_name": "num_of_personal_health_care_providers",
        "dtypes": "str",
    },
    "PRIMINS2": {
        "type": "np_select",
        "conditions": [
            "df['PRIMINS2'] == 1.0",  # Union / Employer plan subscription
            "df['PRIMINS2'] == 2.0",  # Private plan subscription
            "df['PRIMINS2'] == 3.0",  # Medicare
            "df['PRIMINS2'] == 4.0",  # Medigap
            "df['PRIMINS2'] == 5.0",  # Medicaid
            "df['PRIMINS2'] == 6.0",  # Children health insurance program
            "df['PRIMINS2'] == 7.0",  # Military health care
            "df['PRIMINS2'] == 8.0",  # Indian health service
            "df['PRIMINS2'] == 9.0",  # State sponsored health plan
            "df['PRIMINS2'] == 10.0",  # Other government program
            "df['PRIMINS2'] == 88.0",  # No current coverage
        ],
        "choices": [
            "union / employer plan subscription",
            "private plan subscription",
            "medicare",
            "medigap",
            "medicaid",
            "children's health insurance program",
            "military health care",
            "indian health service",
            "state-sponsored health plan",
            "other government program",
            "no current coverage",
        ],
        "new_name": "current_main_healthcare_coverage",
        "dtypes": "str",
    },
    "GENHLTH": {
        "type": "np_select",
        "conditions": [
            "df['GENHLTH'] == 1.0",  # Excellent
            "df['GENHLTH'] == 2.0",  # Very good
            "df['GENHLTH'] == 3.0",  # Good
            "df['GENHLTH'] == 4.0",  # Fair
            "df['GENHLTH'] == 5.0",  # Poor
        ],
        "choices": ["excellent", "very good", "good", "fair", "poor"],
        "new_name": "general_health_status",
        "dtypes": "str",
    },
    "MENTHLTH": {
        "type": "np_where",
        "condition": "df['MENTHLTH'] >= 77.0",
        "true_value": np.nan,
        "new_name": "how_many_days_in_last_month_did_you_have_mental_health_issues",
        "dtypes": "Int64",
    },
    "PHYSHLTH": {
        "type": "np_where",
        "condition": "df['PHYSHLTH'] >= 77.0",
        "true_value": np.nan,
        "new_name": "how_many_days_in_last_month_that_did_you_have_physical_health_issues",
        "dtypes": "Int64",
    },
    "LASTDEN4": {
        "type": "np_select",
        "conditions": [
            "df['LASTDEN4'] == 1.0",  # < 1yr
            "df['LASTDEN4'] == 2.0",  # [1yr, 2yrs[
            "df['LASTDEN4'] == 3.0",  # [2yrs, 5yrs[
            "df['LASTDEN4'] == 4.0",  # 5yrs+
            "df['LASTDEN4'] == 8.0",  # No visit
        ],
        "choices": ["< 1yr", "[1yr, 2yrs[", "[2yrs, 5yrs[", "5yrs+", "no visit"],
        "new_name": "how_long_since_your_last_dentist_visit",
        "dtypes": "str",
    },
    "RMVTETH4": {
        "type": "np_select",
        "conditions": [
            "df['RMVTETH4'] == 1.0",  # 1-5
            "df['RMVTETH4'] == 2.0",  # 6+
            "df['RMVTETH4'] == 3.0",  # All
        ],
        "choices": ["1-5", "6+", "all"],
        "new_name": "num_of_removed_teeth",
        "dtypes": "str",
    },
    "DISPCODE": {
        "type": "np_select",
        "conditions": [
            "df['DISPCODE'] == 1100.0",  # Yes
            "df['DISPCODE'] == 1200.0",  # No
        ],
        "choices": ["yes", "no"],
        "new_name": "have_you_totally_completed_the_interview",
        "dtypes": "str",
    },
    "_STATE": {
        "type": "pd_map",
        "map": {
            1.0: "Alabama",
            2.0: "Alaska",
            4.0: "Arizona",
            5.0: "Arkansas",
            6.0: "California",
            8.0: "Colorado",
            9.0: "Connecticut",
            10.0: "Delaware",
            11.0: "District of Columbia",
            12.0: "Florida",
            13.0: "Georgia",
            15.0: "Hawaii",
            16.0: "Idaho",
            17.0: "Illinois",
            18.0: "Indiana",
            19.0: "Iowa",
            20.0: "Kansas",
            21.0: "Kentucky",
            22.0: "Louisiana",
            23.0: "Maine",
            24.0: "Maryland",
            25.0: "Massachusetts",
            26.0: "Michigan",
            27.0: "Minnesota",
            28.0: "Mississippi",
            29.0: "Missouri",
            30.0: "Montana",
            31.0: "Nebraska",
            32.0: "Nevada",
            33.0: "New Hampshire",
            34.0: "New Jersey",
            35.0: "New Mexico",
            36.0: "New York",
            37.0: "North Carolina",
            38.0: "North Dakota",
            39.0: "Ohio",
            40.0: "Oklahoma",
            41.0: "Oregon",
            42.0: "Pennsylvania",
            44.0: "Rhode Island",
            45.0: "South Carolina",
            46.0: "South Dakota",
            48.0: "Texas",
            49.0: "Utah",
            50.0: "Vermont",
            51.0: "Virginia",
            53.0: "Washington",
            54.0: "West Virginia",
            55.0: "Wisconsin",
            56.0: "Wyoming",
            66.0: "Guam",
            72.0: "Puerto Rico",
            78.0: "Virgin Islands",
        },
        "new_name": "state",
        "dtypes": "str",
    },
}
