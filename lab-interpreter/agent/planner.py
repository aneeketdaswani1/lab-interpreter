"""
30-Day Action Plan Generator Module
Creates personalized 30-day health improvement plans
"""
import json
from typing import List, Dict


class ActionPlanner:
    """Generate 30-day personalized action plans"""
    
    def __init__(self):
        """Initialize planner"""
        self.plan_template = {
            "week_1": {"focus": "Assessment & Baseline", "actions": []},
            "week_2": {"focus": "Lifestyle Changes", "actions": []},
            "week_3": {"focus": "Optimization", "actions": []},
            "week_4": {"focus": "Consolidation & Monitoring", "actions": []}
        }
    
    def generate_plan(self, biomarkers: List[Dict], health_goals: List[str] = None) -> Dict:
        """Generate personalized 30-day action plan"""
        plan = self.plan_template.copy()
        
        # Analyze abnormalities
        abnormal = [b for b in biomarkers if b.get("status") != "normal"]
        
        # Week 1: Assessment
        plan["week_1"]["actions"] = [
            "Schedule consultation with healthcare provider",
            "Record baseline weight, blood pressure, sleep patterns",
            "Document current diet and exercise habits"
        ]
        
        # Week 2-3: Targeted interventions
        if abnormal:
            for biomarker in abnormal[:3]:  # Top 3 abnormalities
                plan["week_2"]["actions"].append(
                    f"Improve {biomarker['name']} - research dietary sources"
                )
        
        # Week 4: Consolidation
        plan["week_4"]["actions"] = [
            "Schedule follow-up lab tests",
            "Review progress and adjust plan",
            "Plan for continued monitoring"
        ]
        
        return plan
    
    def get_dietary_recommendations(self, biomarker_name: str) -> List[str]:
        """Get dietary recommendations for specific biomarker"""
        recommendations = {
            "Glucose": ["Reduce refined carbohydrates", "Increase fiber intake", "Stay hydrated"],
            "Total Cholesterol": ["Reduce saturated fats", "Increase omega-3 foods", "Add oats and beans"],
            "Triglycerides": ["Reduce alcohol", "Replace refined carbs with whole grains", "Increase exercise"],
            "HbA1c": ["Control portion sizes", "Add cinnamon", "Eat protein with carbs"],
            "TSH": ["Adequate iodine intake", "Selenium-rich foods", "Regular meal timing"],
        }
        
        return recommendations.get(biomarker_name, ["Consult healthcare provider for specific recommendations"])
