from dashboard_utils.main_metrics import get_main_metrics
import streamlit as st
import wandb
import pandas as pd
import altair as alt
from streamlit_observable import observable

from dashboard_utils.bubbles import get_new_bubble_data

wandb.login(anonymous="must")

st.title("Training transformers together dashboard")
st.caption("Training Loss")

steps, losses, alive_peers = get_main_metrics()
source = pd.DataFrame({
  "steps": steps, "loss":losses, "alive participants":alive_peers
})

chart_loss = alt.Chart(source).mark_line().encode(
    x='steps',
    y='loss'
)
st.altair_chart(chart_loss,  use_container_width=True)

st.caption("Number of alive participants over time")
chart_alive_peer = alt.Chart(source).mark_line().encode(
    x='steps',
    y='alive participants'
)
st.altair_chart(chart_alive_peer,  use_container_width=True)

st.header("Collaborative training participants")
serialized_data, profiles = get_new_bubble_data()
with st.spinner('Wait for it...'):
    observers = observable(
        "Participants",
        notebook="d/9ae236a507f54046",  # "@huggingface/participants-bubbles-chart",
        targets=["c_noaws"],
        redefine={"serializedData": serialized_data, "profileSimple": profiles},
    )

