import json

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def personalize_output(output, config):
    prefix = f"As a {config.get('Leadership_Archetype')} with a {config.get('Decision_Making_Style')} mindset, "
    style_note = "Here’s what matters most: " if config.get('Communication_Style') == 'Direct' else "You may want to consider the following: "
    return prefix + style_note + output.get('Purpose', '')

def smart_recommendation(variable_name):
    recommendations = {
        'Role_Specific_Functions': {
            'Action': "Review each team member's deliverables weekly.",
            'Prompt': "Is each role clearly contributing to our GTM goals?",
            'KPI': "Role-level output consistency"
        },
        'Insight_Generator': {
            'Action': "Schedule a monthly insight review using team submissions.",
            'Prompt': "What are the patterns that can be scaled?",
            'KPI': "Number of strategic insights applied"
        },
        'Alignment_Tracker': {
            'Action': "Map all activities to live campaign goals.",
            'Prompt': "Are we drifting from core objectives?",
            'KPI': "Alignment score across campaigns"
        }
    }
    return recommendations.get(variable_name, {
        'Action': "Apply based on situational leadership judgment.",
        'Prompt': "How can this be used to improve performance today?",
        'KPI': "Custom – Define based on use case"
    })

def performance_feedback(variable_name):
    feedbacks = {
        'Role_Specific_Functions': "Ensure each role has clear KPIs and documentation to remove ambiguity.",
        'Insight_Generator': "Review insights collaboratively and set action items to leverage key findings.",
        'Alignment_Tracker': "Implement weekly alignment checkpoints and dashboards to catch deviations early."
    }
    return feedbacks.get(variable_name, "Consider setting measurable goals and regular reviews to drive continuous improvement.")

def get_gtm_variable_details(gtm_data, config, runtime, tier, variable_name):
    base = gtm_data.get(tier, {}).get(variable_name, {})
    return {
        'Personalized Purpose': personalize_output(base, config),
        'Inputs': base.get('Inputs', ''),
        'Example': base.get('Example', ''),
        'Suggested Action': smart_recommendation(variable_name)['Action'],
        'Team Prompt': smart_recommendation(variable_name)['Prompt'],
        'Recommended KPI': smart_recommendation(variable_name)['KPI'],
        'Current Value': runtime.get(tier, {}).get(variable_name, 'No data'),
        'Performance Feedback': performance_feedback(variable_name)
    }
