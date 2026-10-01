"""Create static and interactive visualizations for the separated data layers."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, StrMethodFormatter
import seaborn as sns
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "outputs" / "figures"


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")
    india = pd.read_csv(ROOT / "data/processed/india_national_clean.csv")
    states = pd.read_csv(ROOT / "data/processed/india_state_accidents_clean.csv")
    who = pd.read_csv(ROOT / "data/processed/who_road_death_rate_clean.csv")
    violations = pd.read_csv(ROOT / "data/processed/india_traffic_violations_clean.csv")

    fig, ax = plt.subplots(figsize=(9, 5))
    for metric, label in [("accidents", "Accidents"), ("fatalities", "Fatalities"),
                          ("persons_injured", "Persons injured")]:
        ax.plot(india["year"], india[metric], marker="o", label=label)
    ax.set(title="India: reported road accidents and casualties, 2020-2024",
           xlabel="Calendar year", ylabel="Reported count")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "india_national_trends.png", dpi=160)
    plt.close(fig)

    latest = states[states.year == states.year.max()].nlargest(12, "accidents")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=latest, y="state_ut", x="accidents", color="#2367a8", ax=ax)
    ax.set(title="State/UT reported accidents, 2024 (12 highest counts)",
           xlabel="Reported accidents", ylabel="State / UT")
    fig.tight_layout()
    fig.savefig(FIGURES / "india_state_accidents_2024.png", dpi=160)
    plt.close(fig)

    fatal_latest = states[states.year == states.year.max()].nlargest(12, "fatalities")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=fatal_latest, y="state_ut", x="fatalities", color="#b64b4b", ax=ax)
    ax.set(title="State/UT reported fatalities, 2024 (12 highest counts)",
           xlabel="Reported fatalities", ylabel="State / UT")
    fig.tight_layout()
    fig.savefig(FIGURES / "india_state_fatalities_2024.png", dpi=160)
    plt.close(fig)

    px.line(india, x="year", y="accidents", markers=True,
            title="India reported road accidents, 2020-2024").write_html(
                FIGURES / "india_accidents_interactive.html")
    px.bar(latest.sort_values("accidents"), x="accidents", y="state_ut", orientation="h",
           title="Reported accidents by state/UT, 2024").write_html(
                FIGURES / "india_state_accidents_interactive.html")
    px.scatter(fatal_latest, x="accidents", y="fatalities", size="fatalities",
               color="fatalities_per_100_accidents", hover_name="state_ut",
               title="State/UT accident burden and fatalities, 2024",
               labels={"accidents": "Reported accidents", "fatalities": "Reported fatalities",
                       "fatalities_per_100_accidents": "Fatalities per 100 accidents"}
               ).write_html(FIGURES / "india_accidents_fatalities_scatter.html")
    px.bar(violations.query("year == 2024").sort_values("accidents"),
           x="accidents", y="category", orientation="h", hover_data=["fatalities"],
           title="Reported accident counts by traffic-rule category, 2024",
           labels={"category": "Reported category", "accidents": "Reported accidents"}
           ).write_html(FIGURES / "india_traffic_categories.html")
    px.histogram(who, x="death_rate_per_100k", nbins=25,
                 title="WHO estimated road-traffic death rate by country, 2021",
                 labels={"death_rate_per_100k": "Estimated deaths per 100,000 population"}
                 ).write_html(FIGURES / "who_rate_distribution.html")
    px.choropleth(who.dropna(subset=["death_rate_per_100k"]), locations="location_code",
                  locationmode="ISO-3", color="death_rate_per_100k", hover_name="location",
                  title="WHO estimated road-traffic death rate per 100,000, 2021",
                  labels={"death_rate_per_100k": "Estimated deaths per 100,000"}
                  ).write_html(FIGURES / "who_rate_choropleth.html")
    selected_names = ["India", "China", "Nepal", "Bangladesh", "Thailand",
                      "United States of America", "Australia", "Japan"]
    selected = who[who.location.isin(selected_names)].sort_values("death_rate_per_100k")
    px.bar(selected, x="death_rate_per_100k", y="location", orientation="h",
           title="Selected WHO estimated road-traffic death rates, 2021",
           labels={"death_rate_per_100k": "Estimated deaths per 100,000"}
           ).write_html(FIGURES / "who_selected_country_comparison.html")
    px.box(states, x="year", y="accidents", points="all",
           title="Distribution of state/UT accident counts by year").write_html(
               FIGURES / "india_state_year_boxplot.html")
    panel = pd.read_csv(ROOT / "data/processed/india_state_model_features.csv")
    px.scatter(panel, x="previous_year_accidents", y="accidents", color="year",
               hover_name="state_ut", title="Prior-year versus current reported accident counts",
               labels={"previous_year_accidents": "Prior year accidents",
                       "accidents": "Current year accidents"}
               ).write_html(FIGURES / "india_lag_relationship.html")
    print(f"Saved static and interactive plots in {FIGURES}")


if __name__ == "__main__":
    main()
