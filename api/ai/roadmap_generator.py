
SKILL_LEARNING_PLANS = {
    "tableau": {
        "goal": "Learn dashboard design, calculated fields, filters, and interactive visualizations.",
        "practice": "Build an interactive business dashboard with KPI cards, filters, and at least three actionable insights."
    },
    "machine learning": {
        "goal": "Understand supervised learning, regression, classification, and model evaluation metrics.",
        "practice": "Build a small prediction project, evaluate it with appropriate metrics, and document its limitations."
    },
    "docker": {
        "goal": "Understand Docker images, containers, Dockerfiles, and application configuration.",
        "practice": "Containerize a small FastAPI analytics application and document how to run it locally."
    },
    "aws": {
        "goal": "Understand cloud storage, deployment fundamentals, access permissions, and basic cloud architecture.",
        "practice": "Create a small cloud deployment plan for an analytics application and document its security considerations."
    },
    "sql": {
        "goal": "Practice joins, subqueries, CTEs, window functions, and query optimization fundamentals.",
        "practice": "Analyze a business dataset using SQL and create queries for KPIs, trends, and customer or product performance."
    },
    "excel": {
        "goal": "Develop skills in lookup functions, PivotTables, conditional formulas, and data cleaning.",
        "practice": "Create an Excel reporting workbook with cleaned data, PivotTables, charts, and KPI summaries."
    },
    "python": {
        "goal": "Strengthen Python data manipulation, functions, error handling, and reusable analysis workflows.",
        "practice": "Build a reusable Python analysis script that cleans a dataset, calculates KPIs, and exports a report."
    },
    "statistics": {
        "goal": "Understand descriptive statistics, distributions, sampling, hypothesis testing, and correlation.",
        "practice": "Analyze a real dataset, test a clear hypothesis, and explain the findings and limitations."
    },
    "power bi": {
        "goal": "Practice data modeling, Power Query, DAX measures, and interactive dashboard design.",
        "practice": "Build a Power BI dashboard with a suitable data model, KPI measures, slicers, and business recommendations."
    },
    "pandas": {
        "goal": "Improve data cleaning, missing-value handling, grouping, merging, and transformation with Pandas.",
        "practice": "Create a reproducible ETL workflow that cleans raw data, validates records, and exports an analysis-ready dataset."
    },
    "numpy": {
        "goal": "Practice numerical arrays, vectorized operations, aggregations, and efficient numerical calculations.",
        "practice": "Use NumPy to perform calculations on a dataset and compare vectorized operations with a simple loop."
    },
    "data visualization": {
        "goal": "Learn how to select appropriate charts and communicate patterns, comparisons, and trends clearly.",
        "practice": "Create a visual report with at least four suitable charts and explain the key insights from each."
    },
    "data analysis": {
        "goal": "Practice data validation, exploratory analysis, KPI calculation, and evidence-based interpretation.",
        "practice": "Complete an end-to-end analysis that answers a business question and presents three evidence-based findings."
    },


    "power query": {
        "goal": "Learn data import, data cleaning, transformation steps, merging queries, and refreshable ETL workflows.",
        "practice": "Import a raw CSV dataset, clean missing values, merge two tables, and build a repeatable Power Query transformation workflow."
    },
    "dax": {
        "goal": "Learn DAX measures, calculated columns, filter context, CALCULATE, and time intelligence fundamentals.",
        "practice": "Create a Power BI report with measures for total sales, growth percentage, year-to-date performance, and category comparisons."
    },
    "data modeling": {
        "goal": "Understand fact and dimension tables, star schemas, relationships, and one-to-many cardinality.",
        "practice": "Design a star schema for a sales dataset, connect it to Power BI, and validate the relationships using business questions."
    },
    "query optimization": {
        "goal": "Learn to identify inefficient SQL queries, use indexes appropriately, and interpret query execution plans.",
        "practice": "Optimize several SQL queries against a sample dataset and document the changes in execution plans or query performance."
    },

}


def generate_learning_roadmap(missing_skills):
    """
    Generate a practical learning roadmap from a list of skills.
    Preserve the existing week, focus, goal, and practice response format.
    """

    roadmap = []
    seen_skills = set()

    for skill in missing_skills:
        normalized_skill = skill.strip().lower()

        if not normalized_skill or normalized_skill in seen_skills:
            continue

        seen_skills.add(normalized_skill)

        plan = SKILL_LEARNING_PLANS.get(
            normalized_skill,
            {
                "goal": (
                    f"Develop practical knowledge of {normalized_skill} "
                    "and understand how it applies to data analytics."
                ),
                "practice": (
                    f"Complete a small, relevant project using "
                    f"{normalized_skill} and document the results."
                ),
            },
        )

        roadmap.append({
            "week": len(roadmap) + 1,
            "focus": normalized_skill,
            "goal": plan["goal"],
            "practice": plan["practice"],
        })

        if len(roadmap) == 4:
            break

    if not roadmap:
        roadmap.append({
            "week": 1,
            "focus": "Advanced Analytics Project",
            "goal": "Apply existing skills to solve a realistic business problem.",
            "practice": (
                "Build an end-to-end analytics project with data cleaning, "
                "SQL analysis, visualizations, and documented recommendations."
            ),
        })

    return roadmap
