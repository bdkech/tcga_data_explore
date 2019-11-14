"""
@author: Bobak Kechavarzi (bdkech)
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# Data loading
SHAP_DAT = pandas.read_csv(
    open("data/staging/all_shap_melt_mod_log.txt", "r"), sep="\t"
)
FLD_CHNG_DAT = pandas.read_csv(
    open("data/staging/all_fld_chng_melt.txt", "r"), sep="\t"
)
CORR = pandas.read_csv(open("data/staging/correlations.txt", "r"), sep="\t")
ALL_PIVOT = pandas.read_csv(
    open("data/staging/all_merged_pivot.txt", "r"), sep="\t"
)


def get_gene_ids():
    return sorted(list(CORR["hgnc_symbol"].unique()))


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("TCGA Data Exploration"),
        html.Hr(),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Tabs(
                            id="content-tab",
                            value="what-is",
                            children=[
                                dcc.Tab(
                                    label="About",
                                    value="what-is",
                                    children=html.Div(
                                        [
                                            html.H4(
                                                className="what-is",
                                                children="About this tool",
                                            ),
                                            html.P(
                                                "This tool visualizes and provides exploration of the BRCA "
                                                "and OV datasets used in the deep model training, as well "
                                                "as the SHAP values that resulted."
                                            ),
                                            html.P(
                                                "You can use the filters on the following tab to identify genes "
                                                "from the data you may be interested in.  Clicking on a row will "
                                                "populate the figures with that genes signatures across all samples. "
                                                "If you have a gene of interest you can directly filter on that."
                                            ),
                                        ]
                                    ),
                                ),
                                dcc.Tab(
                                    id="filter-tab",
                                    label="Filters",
                                    value="filter",
                                    children=[
                                        html.H5("CNV Exp"),
                                        dcc.RangeSlider(
                                            count=1,
                                            id="cnv_exp",
                                            min=ALL_PIVOT["CNV_exp"].min(),
                                            max=ALL_PIVOT["CNV_exp"].max(),
                                            allowCross=False,
                                            step=0.25,
                                            value=[-3, 7],
                                        ),
                                        html.H5("mRNA Exp"),
                                        dcc.RangeSlider(
                                            count=1,
                                            id="mrna_exp",
                                            min=ALL_PIVOT["mRNA_exp"].min(),
                                            max=ALL_PIVOT["mRNA_exp"].max(),
                                            allowCross=False,
                                            step=0.25,
                                            value=[-3, 7],
                                        ),
                                        html.H5("Prot Exp"),
                                        dcc.RangeSlider(
                                            count=1,
                                            id="prot_exp",
                                            min=ALL_PIVOT["protein_exp"].min(),
                                            max=ALL_PIVOT["protein_exp"].max(),
                                            allowCross=False,
                                            step=0.25,
                                            value=[-3, 7],
                                        ),
                                        html.H5("CNV SHAP"),
                                        dcc.RangeSlider(
                                            count=1,
                                            id="cnv_shap",
                                            min=ALL_PIVOT["CNV_shap"].min(),
                                            max=ALL_PIVOT["CNV_shap"].max(),
                                            allowCross=False,
                                            step=0.25,
                                            value=[0, 1],
                                        ),
                                        html.H5("mRNA SHAP"),
                                        dcc.RangeSlider(
                                            count=1,
                                            id="mrna_shap",
                                            min=ALL_PIVOT["mRNA_shap"].min(),
                                            max=ALL_PIVOT["mRNA_shap"].max(),
                                            allowCross=False,
                                            step=0.25,
                                            value=[-3, 7],
                                        ),
                                        html.H5("Prot SHAP"),
                                        dcc.RangeSlider(
                                            count=1,
                                            id="prot_shap",
                                            min=ALL_PIVOT[
                                                "protein_shap"
                                            ].min(),
                                            max=ALL_PIVOT[
                                                "protein_shap"
                                            ].max(),
                                            allowCross=False,
                                            step=0.05,
                                            value=[0, 0.8],
                                        ),
                                        html.H5("mRNA v Prot Correlation"),
                                        dcc.RangeSlider(
                                            count=1,
                                            id="mrna_v_prot",
                                            min=ALL_PIVOT[
                                                "exp_v_prot_corr"
                                            ].min(),
                                            max=ALL_PIVOT[
                                                "exp_v_prot_corr"
                                            ].max(),
                                            allowCross=False,
                                            step=0.05,
                                            value=[0, 0.8],
                                        ),
                                        html.H5("mRNA v CNV Correlation"),
                                        dcc.RangeSlider(
                                            count=1,
                                            id="mrna_v_cnv",
                                            min=ALL_PIVOT[
                                                "exp_v_seg_corr"
                                            ].min(),
                                            max=ALL_PIVOT[
                                                "exp_v_seg_corr"
                                            ].max(),
                                            allowCross=False,
                                            step=0.05,
                                            value=[0, 0.8],
                                        ),
                                        html.H5("Prot v CNV Correlation"),
                                        dcc.RangeSlider(
                                            count=1,
                                            id="prot_v_cnv",
                                            min=ALL_PIVOT[
                                                "prot_v_seg_corr"
                                            ].min(),
                                            max=ALL_PIVOT[
                                                "prot_v_seg_corr"
                                            ].max(),
                                            allowCross=False,
                                            step=0.25,
                                            value=[-3, 7],
                                        ),
                                        dcc.Dropdown(
                                            id="input-1",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in get_gene_ids()
                                            ],
                                            value="Select gene",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        dash_table.DataTable(
                            id="datatable",
                            columns=[
                                {
                                    "name": i,
                                    "id": i,
                                    "deletable": True,
                                    "selectable": True,
                                }
                                for i in ALL_PIVOT.columns
                            ],
                            data=ALL_PIVOT.head(50).to_dict("records"),
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            row_selectable="single",
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            style_table={"overflowX": "scroll"},
                            page_size=10,
                        ),
                    ],
                    className="six columns",
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id="graph1")],
                            className="twelve columns",
                        ),
                        html.Div(
                            [dcc.Graph(id="graph2")],
                            className="twelve columns",
                        ),
                        html.Div(
                            [dcc.Graph(id="graph3")],
                            className="twelve columns",
                        ),
                    ],
                    className="six columns",
                ),
            ],
            className="row",
        ),
    ]
)


@app.callback(
    Output("input-1", "value"),
    [Input("datatable", "selected_rows")],
    [State("datatable", "data")],
)
def update_selector(selected_row, rows):
    print(selected_row)
    gene_idx = rows[selected_row[0]]["variable"]
    return gene_idx


@app.callback(
    Output("datatable", "data"),
    [
        Input("mrna_exp", "value"),
        Input("cnv_exp", "value"),
        Input("prot_exp", "value"),
        Input("cnv_shap", "value"),
        Input("prot_shap", "value"),
        Input("mrna_shap", "value"),
        Input("mrna_v_prot", "value"),
        Input("mrna_v_cnv", "value"),
        Input("prot_v_cnv", "value"),
    ],
)
def update_table(
    mrna_exp,
    cnv_exp,
    protein_exp,
    cnv_shap,
    protein_shap,
    mrna_shap,
    exp_v_prot,
    exp_v_seg,
    prot_v_seg,
):
    x = ALL_PIVOT[
        (ALL_PIVOT["CNV_exp"] >= cnv_exp[0])
        & (ALL_PIVOT["CNV_exp"] <= cnv_exp[1])
        & (ALL_PIVOT["mRNA_exp"] >= mrna_exp[0])
        & (ALL_PIVOT["mRNA_exp"] <= mrna_exp[1])
        & (ALL_PIVOT["protein_exp"] >= protein_exp[0])
        & (ALL_PIVOT["protein_exp"] <= protein_exp[1])
        & (ALL_PIVOT["CNV_shap"] >= cnv_shap[0])
        & (ALL_PIVOT["CNV_shap"] <= cnv_shap[1])
        & (ALL_PIVOT["mRNA_shap"] >= mrna_exp[0])
        & (ALL_PIVOT["mRNA_shap"] <= mrna_shap[1])
        & (ALL_PIVOT["protein_shap"] >= protein_exp[0])
        & (ALL_PIVOT["protein_shap"] <= protein_shap[1])
        & (ALL_PIVOT["exp_v_prot_corr"] >= exp_v_prot[0])
        & (ALL_PIVOT["exp_v_prot_corr"] <= exp_v_prot[1])
        & (ALL_PIVOT["exp_v_seg_corr"] >= exp_v_seg[0])
        & (ALL_PIVOT["exp_v_seg_corr"] <= exp_v_seg[1])
        & (ALL_PIVOT["prot_v_seg_corr"] >= prot_v_seg[0])
        & (ALL_PIVOT["prot_v_seg_corr"] <= prot_v_seg[1])
    ]
    return x.to_dict("records")


@app.callback(Output("graph1", "figure"), [Input("input-1", "value")])
def update_graph(gene_id):
    dat_brca = FLD_CHNG_DAT[
        (FLD_CHNG_DAT["variable"] == gene_id)
        & (FLD_CHNG_DAT["histology"] == "BRCA")
    ]
    dat_ov = FLD_CHNG_DAT[
        (FLD_CHNG_DAT["variable"] == gene_id)
        & (FLD_CHNG_DAT["histology"] == "OV")
    ]
    trace = {
        "x": dat_brca["type"].values,
        "y": dat_brca["value"].values,
        "type": "violin",
        "name": "BRCA",
    }
    trace2 = {
        "x": dat_ov["type"].values,
        "y": dat_ov["value"].values,
        "type": "violin",
        "name": "OV",
    }

    # trace = go.Box(y=dat['value'].values, x=dat['type'].values)
    data = [trace, trace2]
    return {
        "data": data,
        "layout": go.Layout(
            xaxis={"title": "Data Type"},
            yaxis={"title": "Log2 fold change"},
            title={"text": gene_id},
        ),
    }


@app.callback(Output("graph2", "figure"), [Input("input-1", "value")])
def update_graph2(gene_id):
    dat_brca = SHAP_DAT[
        (SHAP_DAT["variable"] == gene_id) & (SHAP_DAT["histology"] == "BRCA")
    ]
    dat_ov = SHAP_DAT[
        (SHAP_DAT["variable"] == gene_id) & (SHAP_DAT["histology"] == "OV")
    ]
    trace = {
        "x": dat_brca["type"].values,
        "y": dat_brca["value"].values,
        "type": "violin",
        "name": "BRCA",
    }
    trace2 = {
        "x": dat_ov["type"].values,
        "y": dat_ov["value"].values,
        "type": "violin",
        "name": "OV",
    }

    # trace = go.Box(y=dat['value'].values, x=dat['type'].values)
    data = [trace, trace2]
    return {
        "data": data,
        "layout": go.Layout(
            xaxis={"title": "Data Type"}, yaxis={"title": "Modified SHAP"}
        ),
    }


@app.callback(Output("graph3", "figure"), [Input("input-1", "value")])
def update_graph3(gene_id):
    dat_brca = CORR[
        (CORR["hgnc_symbol"] == gene_id) & (CORR["project"] == "TCGA-BRCA")
    ]
    dat_ov = CORR[
        (CORR["hgnc_symbol"] == gene_id) & (CORR["project"] == "TCGA-OV")
    ]
    trace = {
        "x": dat_brca["variable"].values,
        "y": dat_brca["value"].values,
        "type": "bar",
        "name": "BRCA",
    }
    trace2 = {
        "x": dat_ov["variable"].values,
        "y": dat_ov["value"].values,
        "type": "bar",
        "name": "OV",
    }

    # trace = go.Box(y=dat['value'].values, x=dat['type'].values)
    data = [trace, trace2]
    return {
        "data": data,
        "layout": go.Layout(
            xaxis={"title": "Data Type"}, yaxis={"title": "Correlation"}
        ),
    }


if __name__ == "__main__":
    app.run_server(host="0.0.0.0")
