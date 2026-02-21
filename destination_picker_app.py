import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import streamlit as st
from collections import Counter

# Page configurations
st.set_page_config(page_title="Family Destination Picker", layout="wide")

st.title("✈️ Family Destination Draw Simulator")
st.markdown("Add your destinations and family members, then run the simulation!")

# Sidebar inputs
with st.sidebar:
    st.header("⚙️ Setup")

    destinations_input = st.text_area(
        "Destinations (one per line)",
        value="Madrid\nRim\nEdinbrough\nManchaster\nAmsterdam\nLisbona\nMalta\nSicilija\nSardinija\nValencija\nMalaga",
        height=220,
    )

    members_input = st.text_area(
        "Family members (one per line)", value="Suzi\nDavid\nMia\nVid", height=120
    )

    draws = st.slider(
        "Draws per person", min_value=10, max_value=1000, value=100, step=10
    )

    run = st.button("▶️ Run Simulation", use_container_width=True)

# Parse inputs
DESTINATIONS = [d.strip() for d in destinations_input.splitlines() if d.strip()]
FAMILY_MEMBERS = [m.strip() for m in members_input.splitlines() if m.strip()]

# Validate
if len(DESTINATIONS) < 2:
    st.warning("Please enter at least 2 destinations in the sidebar.")
    st.stop()
if len(FAMILY_MEMBERS) < 1:
    st.warning("Please enter at least 1 family member in the sidebar.")
    st.stop()


# Auto colors
def generate_colors(n):
    if n <= 20:
        colormap = plt.colormaps.get_cmap("tab20")
    else:
        colormap = plt.colormaps.get_cmap("hsv")
    return [colormap(i / n) for i in range(n)]


COLORS = generate_colors(len(DESTINATIONS))
COLOR_MAP = {dest: COLORS[i] for i, dest in enumerate(DESTINATIONS)}

# Run simulation on button press
if run:
    picks = {}
    all_picks = []

    for person in FAMILY_MEMBERS:
        person_picks = random.choices(DESTINATIONS, k=draws)
        picks[person] = person_picks
        all_picks.extend(person_picks)

    overall_counts = Counter(all_picks)
    person_counts = {p: Counter(v) for p, v in picks.items()}

    # Summary stats
    st.subheader("📊 Quick Summary")
    sorted_overall = sorted(overall_counts.items(), key=lambda x: -x[1])

    col_stats = st.columns(len(FAMILY_MEMBERS))
    for col, person in zip(col_stats, FAMILY_MEMBERS):
        top = person_counts[person].most_common(1)[0]
        col.metric(label=f"{person}'s top pick", value=top[0], delta=f"{top[1]} picks")

    st.divider()

    # Overall chart
    st.subheader(f"🌍 Overall picks — {draws * len(FAMILY_MEMBERS)} total draws")

    fig_overall, ax = plt.subplots(figsize=(14, 4))
    labels_o, vals_o = zip(*sorted_overall)
    bars = ax.bar(
        labels_o, vals_o, color=[COLOR_MAP[d] for d in labels_o], edgecolor="white"
    )
    ax.set_ylabel("Times picked")
    ax.set_ylim(0, max(vals_o) * 1.2)
    ax.tick_params(axis="x", rotation=30)
    for bar, val in zip(bars, vals_o):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            str(val),
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )
    plt.tight_layout()
    st.pyplot(fig_overall)
    plt.close(fig_overall)

    st.divider()

    # Individual charts
    st.subheader("👨‍👩‍👧‍👦 Individual picks")

    n_cols = 2
    rows = [
        FAMILY_MEMBERS[i : i + n_cols] for i in range(0, len(FAMILY_MEMBERS), n_cols)
    ]

    for row in rows:
        cols = st.columns(n_cols)
        for col, person in zip(cols, row):
            sorted_p = sorted(person_counts[person].items(), key=lambda x: -x[1])
            labels_p, vals_p = zip(*sorted_p)

            fig_p, ax_p = plt.subplots(figsize=(7, 4))
            bars_p = ax_p.bar(
                labels_p,
                vals_p,
                color=[COLOR_MAP[d] for d in labels_p],
                edgecolor="white",
            )
            ax_p.set_title(person, fontsize=12)
            ax_p.set_ylabel("Times picked")
            ax_p.set_ylim(0, max(vals_p) * 1.25)
            ax_p.tick_params(axis="x", rotation=30, labelsize=8)
            for bar, val in zip(bars_p, vals_p):
                ax_p.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.3,
                    str(val),
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )
            plt.tight_layout()
            col.pyplot(fig_p)
            plt.close(fig_p)

else:
    st.info(
        "👈 Configure your settings in the sidebar and press **Run Simulation** to start."
    )
