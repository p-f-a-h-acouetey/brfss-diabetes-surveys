from src.main.scripts.loaders.data_loader import SurveyLoader
from pandas.testing import assert_frame_equal
import pandas as pd
import pytest


@pytest.fixture()
def expected_df():
    df = pd.DataFrame(
        {
            "is_your_blood_pressure_high": [0],
            "is_your_cholesterol_high": [1],
            "have_you_had_a_cholesterol_check_in_last_5years": [1],
            "your_bmi_value": [58.9],
            "have_you_ever_smoked_at_least_100cigs": [0],
            "have_you_ever_had_stroke": [0],
            "have_you_ever_had_coronary_heart_disease_or_myocardial_infarction": [0],
            "did_you_exercise_in_last_30days": [0],
            "do_you_eat_fruits_daily": [1],
            "do_you_eat_veggies_daily": [1],
            "are_you_a_man_with_at_least_14drinks_per_week_or_a_woman_with_at_least_7drinks_per_week": [
                0
            ],
            "are_you_covered_by_any_healthcare_insurance": [0],
            "was_there_a_time_in_last_12months_you_could_not_afford_a_doctor_because_of_cost": [
                1
            ],
            "your_health_level_in_general": [2],
            "how_many_days_during_last_30days_your_mental_health_was_bad": [15],
            "how_many_days_during_last_30days_your_physical_health_was_bad": [0],
            "have_you_serious_walking_difficulty": [0],
            "your_gender": [0],
            "your_age": [31],
            "your_education_level": [3],
            "your_income_level": [4],
            "have_you_diabetes_or_prediabetes": [0],
        }
    )
    # Force exact dtypes
    int_cols = [col for col in df.columns if col != "your_bmi_value"]
    df[int_cols] = df[int_cols].astype("int32")
    df["your_bmi_value"] = df["your_bmi_value"].astype("float32")
    df = df[sorted(df.columns)]
    return df


def test_load_df(expected_df):
    survey_loader = SurveyLoader(
        data_path="./src/tests/unit/loaders/fixtures/samples.parquet"
    )
    actual_df = survey_loader.load_df()
    print(actual_df.columns)
    print(expected_df.columns)
    assert_frame_equal(actual_df, expected_df)
