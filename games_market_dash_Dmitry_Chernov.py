import pandas as pd
import numpy as np
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output

df0 = pd.read_csv("games.csv")
# print(df0.head(3))
# print(df0.info())

df = df0.dropna().query("2000 <= Year_of_Release <= 2022")
# print(df.info())
# print(df.describe())

# convert age rating from str to int using map
rating_map = {
    "E": 0,
    "E10+": 10,
    "T": 13,
    "M": 17,
    "AO": 18,
    "RP": 18,
}  # I decide to assign 'Rating Pending' the value 18 like the 'Adults Only' one for now
df["Rating"] = df["Rating"].map(rating_map).astype(int)

df["User_Score"] = (
    df["User_Score"].replace("tbd", np.nan).astype(float)
)  # I want to see the statistics of User_Score var too, I need numeric and nan for the rest
df["Year_of_Release"] = df["Year_of_Release"].astype(int)
# print(df.info())
# print(df.describe())


# DASHBOARD
# the app
app = dash.Dash(__name__)

# dashboard layout
app.layout = html.Div(
    [
        html.H2("Video Game Analysis Dashboard"),
        html.Div(
            [
                html.P("This dashboard allows you to analyze video game data."),
                html.P(
                    "Use the platform dropdown to select one or more gaming platforms. Select game genres using the genre dropdown. Adjust the year range slider to focus on specific periods. The  key metrics and charts update based on your selections. Hover over chart elements for more information."
                ),
            ],
            style={
                "marginBottom": "15px",
                "backgroundColor": "#f0f0f0",
                "padding": "10px",
                "borderRadius": "5px",
            },
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="platform-filter",
                            options=[
                                {"label": i, "value": i}
                                for i in df["Platform"].unique()
                            ],
                            multi=True,
                            placeholder="Select platforms",
                        )
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "marginRight": "2%",
                    },
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="genre-filter",
                            options=[
                                {"label": i, "value": i} for i in df["Genre"].unique()
                            ],
                            multi=True,
                            placeholder="Select genres",
                        )
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "marginRight": "2%",
                    },
                ),
                html.Div(
                    [
                        dcc.RangeSlider(
                            id="year-filter",
                            min=df["Year_of_Release"].min(),
                            max=df["Year_of_Release"].max(),
                            step=1,
                            marks={
                                str(year): str(year)
                                for year in range(
                                    int(df["Year_of_Release"].min()),
                                    int(df["Year_of_Release"].max()) + 1,
                                    5,
                                )
                            },
                            value=[
                                df["Year_of_Release"].min(),
                                df["Year_of_Release"].max(),
                            ],
                        )
                    ],
                    style={"width": "36%", "display": "inline-block"},
                ),
            ],
            style={"marginBottom": "20px"},
        ),
        # graphs
        html.Div(
            [
                # first row of graphs
                html.Div(
                    [
                        dcc.Graph(
                            id="total-games", style={"width": "30%", "height": "200px"}
                        ),
                        dcc.Graph(
                            id="avg-user-score",
                            style={"width": "30%", "height": "200px"},
                        ),
                        dcc.Graph(
                            id="avg-critic-score",
                            style={"width": "30%", "height": "200px"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-around",
                        "marginBottom": "20px",
                    },
                ),
                # second row of graphs
                html.Div(
                    [
                        dcc.Graph(id="games-by-year-platform", style={"width": "33%"}),
                        dcc.Graph(id="user-vs-critic-scores", style={"width": "33%"}),
                        dcc.Graph(id="avg-rating-by-genre", style={"width": "33%"}),
                    ],
                    style={"display": "flex", "justifyContent": "space-between"},
                ),
            ]
        ),
    ]
)


# callback function to update graphs
@app.callback(
    [
        Output("total-games", "figure"),
        Output("avg-user-score", "figure"),
        Output("avg-critic-score", "figure"),
        Output("games-by-year-platform", "figure"),
        Output("user-vs-critic-scores", "figure"),
        Output("avg-rating-by-genre", "figure"),
    ],
    [
        Input("platform-filter", "value"),
        Input("genre-filter", "value"),
        Input("year-filter", "value"),
    ],
)
def update_graphs(selected_platforms, selected_genres, year_range):
    filtered_df = df

    if selected_platforms:
        filtered_df = filtered_df[filtered_df["Platform"].isin(selected_platforms)]
    if selected_genres:
        filtered_df = filtered_df[filtered_df["Genre"].isin(selected_genres)]
    filtered_df = filtered_df[
        (filtered_df["Year_of_Release"] >= year_range[0])
        & (filtered_df["Year_of_Release"] <= year_range[1])
    ]

    # graph 1: total number of games
    total_games = len(filtered_df)
    fig1 = go.Figure(
        go.Indicator(
            mode="number",
            value=total_games,
            title={"text": "Total Games", "font": {"size": 20}},
            number={"font": {"size": 40}},
        )
    )
    fig1.update_layout(margin=dict(l=10, r=10, t=30, b=10))

    # graph 2: average user score
    avg_user_score = filtered_df["User_Score"].mean()
    fig2 = go.Figure(
        go.Indicator(
            mode="number",
            value=avg_user_score,
            title={"text": "Avg User Score", "font": {"size": 20}},
            number={"font": {"size": 40}, "valueformat": ".2f"},
        )
    )
    fig2.update_layout(margin=dict(l=10, r=10, t=30, b=10))

    # graph 3: average critic score
    avg_critic_score = filtered_df["Critic_Score"].mean()
    fig3 = go.Figure(
        go.Indicator(
            mode="number",
            value=avg_critic_score,
            title={"text": "Avg Critic Score", "font": {"size": 20}},
            number={"font": {"size": 40}, "valueformat": ".2f"},
        )
    )
    fig3.update_layout(margin=dict(l=10, r=10, t=30, b=10))

    # graph 4: stacked area plot
    fig4 = px.area(
        filtered_df.groupby(["Year_of_Release", "Platform"])
        .size()
        .reset_index(name="Count"),
        x="Year_of_Release",
        y="Count",
        color="Platform",
        title="Game Releases by Year and Platform",
    )
    fig4.update_layout(title_x=0.5)  # center the title

    # graph 5: scatter plot
    fig5 = px.scatter(
        filtered_df,
        x="User_Score",
        y="Critic_Score",
        color="Genre",
        title="User Scores vs Critic Scores",
    )
    fig5.update_layout(title_x=0.5)

    # graph 6: bar chart
    avg_rating_by_genre = filtered_df.groupby("Genre")["Rating"].mean().reset_index()
    fig6 = px.bar(
        avg_rating_by_genre,
        x="Genre",
        y="Rating",
        title="Average Age Rating by Genre",
    )
    fig6.update_layout(title_x=0.5)

    return fig1, fig2, fig3, fig4, fig5, fig6


if __name__ == "__main__":
    app.run_server(debug=True)
