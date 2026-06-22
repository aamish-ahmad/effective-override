"""Streamlit viewer for Agency Trajectory Benchmark Experiment 0."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).parent / "data" / "experiment0.csv"


def display_bool(value: object) -> str:
    if pd.isna(value) or str(value).strip() == "":
        return "Not labeled"
    return "Crossing present" if str(value).strip().lower() in {"true", "1", "yes"} else "No crossing"


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


st.set_page_config(page_title="Agency Trajectory Benchmark v0", layout="centered")
st.title("Agency Trajectory Benchmark v0")
st.caption("Detecting Loss of Effective Override in AI-Mediated Workflows")

data = load_data()
trajectory_id = st.selectbox("Trajectory", data["trajectory_id"].tolist())
row = data.loc[data["trajectory_id"] == trajectory_id].iloc[0]

st.write(f"**Pair:** {row['pair_id']}  |  **Condition:** {row['condition']}  |  **Domain:** {row['domain']}")
st.subheader("Steps")
for index, step in enumerate(json.loads(row["steps_json"]), start=1):
    st.markdown(f"**{index}.** {step}")

ground_truth = display_bool(row["ground_truth_crossing_present"])
blind_rater = display_bool(row["blind_rater_crossing_present"])
ground_step = "None" if pd.isna(row["ground_truth_crossing_step"]) else str(int(row["ground_truth_crossing_step"]))
blind_step = "None" if pd.isna(row["blind_rater_crossing_step"]) else str(int(row["blind_rater_crossing_step"]))

left, right = st.columns(2)
with left:
    st.subheader("Ground truth")
    st.write(ground_truth)
    st.write(f"Crossing step: {ground_step}")
with right:
    st.subheader("Blind rater")
    st.write(blind_rater)
    st.write(f"Crossing step: {blind_step}")
    st.write(f"Reason: {row['blind_rater_reason'] if pd.notna(row['blind_rater_reason']) else 'Not provided'}")

st.subheader("Agreement")
if blind_rater == "Not labeled":
    st.info("This trajectory has not been labeled by a blind rater.")
else:
    binary_match = ground_truth == blind_rater
    step_match = (
        pd.isna(row["ground_truth_crossing_step"])
        and pd.isna(row["blind_rater_crossing_step"])
    ) or (
        pd.notna(row["ground_truth_crossing_step"])
        and pd.notna(row["blind_rater_crossing_step"])
        and abs(row["ground_truth_crossing_step"] - row["blind_rater_crossing_step"]) <= 1
    )
    if binary_match and step_match:
        st.success("Agreement (crossing step is within one step when applicable).")
    elif binary_match:
        st.warning("Binary label agrees, but crossing step differs by more than one step.")
    else:
        st.error("Binary crossing label disagrees.")

