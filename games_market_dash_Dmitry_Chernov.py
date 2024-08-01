import pandas as pd
import numpy as np
import dash
from dash import dcc, html

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
# Initialize the app
app = dash.Dash(__name__)

# Dashboard layout
app.layout = html.Div(
    [
        html.H1("Video Game Analysis Dashboard"),
        html.P(
            "This dashboard allows you to analyze video game data. Use the filters to customize the displayed data."
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
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
