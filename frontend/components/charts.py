import plotly.express as px


def line_chart(data):
    return px.line(data)


def heatmap(data):
    return px.imshow(data, text_auto=True)


def scatter(data):
    return px.scatter(data, x="Risk", y="Return", opacity=0.5)
