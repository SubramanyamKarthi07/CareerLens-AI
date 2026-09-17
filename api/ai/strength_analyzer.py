def generate_strengths(skills):
    """
    Convert extracted skills into professional strengths.
    """

    skills = {skill.lower() for skill in skills}

    strengths = []

    programming = {
        "python",
        "fastapi",
        "flask",
        "git",
        "github"
    }

    data_analysis = {
        "sql",
        "excel",
        "pandas",
        "numpy"
    }

    visualization = {
        "power bi",
        "tableau",
        "matplotlib",
        "seaborn",
        "plotly",
        "data visualization"
    }

    machine_learning = {
        "machine learning",
        "scikit-learn",
        "tensorflow",
        "pytorch"
    }

    cloud = {
        "aws",
        "azure",
        "gcp",
        "docker"
    }

    if skills & programming:
        strengths.append("Programming & Software Development")

    if skills & data_analysis:
        strengths.append("Data Analysis & SQL")

    if skills & visualization:
        strengths.append("Business Intelligence & Visualization")

    if skills & machine_learning:
        strengths.append("Machine Learning Fundamentals")

    if skills & cloud:
        strengths.append("Cloud & Deployment")

    return strengths