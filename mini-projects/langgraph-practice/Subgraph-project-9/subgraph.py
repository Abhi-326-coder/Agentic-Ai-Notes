from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# ==================================================
# RESEARCH SUBGRAPH
# ==================================================

class ResearchState(TypedDict):

    topic: str
    sources: list[str]
    summaries: list[str]


def search_sources(state: ResearchState):

    return {
        "sources": [
            "Research Paper A",
            "Industry Report B",
            "Developer Survey C"
        ]
    }


def summarize_sources(state: ResearchState):

    return {
        "summaries": [
            f"Summary of {source}"
            for source in state["sources"]
        ]
    }


research_builder = StateGraph(ResearchState)

research_builder.add_node(
    "search",
    search_sources
)

research_builder.add_node(
    "summarize",
    summarize_sources
)

research_builder.add_edge(
    START,
    "search"
)

research_builder.add_edge(
    "search",
    "summarize"
)

research_builder.add_edge(
    "summarize",
    END
)

research_graph = research_builder.compile()


# ==================================================
# ANALYSIS SUBGRAPH
# ==================================================

class AnalysisState(TypedDict):

    summaries: list[str]
    findings: str


def analyze(state: AnalysisState):

    return {
        "findings": (
            f"Analyzed "
            f"{len(state['summaries'])} summaries."
        )
    }


analysis_builder = StateGraph(AnalysisState)

analysis_builder.add_node(
    "analyze",
    analyze
)

analysis_builder.add_edge(
    START,
    "analyze"
)

analysis_builder.add_edge(
    "analyze",
    END
)

analysis_graph = analysis_builder.compile()


# ==================================================
# REPORT SUBGRAPH
# ==================================================

class ReportState(TypedDict):

    findings: str
    report: str


def generate_report(state: ReportState):

    return {
        "report": (
            "AI Research Report\n\n"
            + state["findings"]
        )
    }


report_builder = StateGraph(ReportState)

report_builder.add_node(
    "generate",
    generate_report
)

report_builder.add_edge(
    START,
    "generate"
)

report_builder.add_edge(
    "generate",
    END
)

report_graph = report_builder.compile()


# ==================================================
# MAIN GRAPH
# ==================================================

class MainState(TypedDict):

    topic: str
    sources: list[str]
    summaries: list[str]
    findings: str
    report: str


main_builder = StateGraph(MainState)


main_builder.add_node(
    "research",
    research_graph
)

main_builder.add_node(
    "analysis",
    analysis_graph
)

main_builder.add_node(
    "report",
    report_graph
)


main_builder.add_edge(
    START,
    "research"
)

main_builder.add_edge(
    "research",
    "analysis"
)

main_builder.add_edge(
    "analysis",
    "report"
)

main_builder.add_edge(
    "report",
    END
)


main_graph = main_builder.compile()


# ==================================================
# RUN
# ==================================================

result = main_graph.invoke(
    {
        "topic": "Artificial Intelligence",
        "sources": [],
        "summaries": [],
        "findings": "",
        "report": ""
    }
)

print(result)