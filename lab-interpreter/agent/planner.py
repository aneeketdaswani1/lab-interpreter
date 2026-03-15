"""
30-Day Action Plan Generator Module
Creates personalized health protocols using Google Gemini
"""
import os
from typing import List, Dict, Optional
import google.generativeai as genai


def generate_action_plan(biomarkers: List[Dict], user_profile: Dict, 
                        research_dict: Dict[str, List[Dict]]) -> str:
    """
    Generate a comprehensive 30-day personalized action plan.
    
    Args:
        biomarkers: Full list of biomarker dicts from parser
        user_profile: Dict with keys: age, sex, activity_level, dietary_preference, health_goals
                     activity_level: 'sedentary' | 'light' | 'moderate' | 'active'
                     dietary_preference: 'omnivore' | 'vegetarian' | 'vegan' | 'keto'
                     health_goals: list of strings (e.g., ["weight loss", "energy", "longevity"])
        research_dict: Dict mapping biomarker names to study lists
        
    Returns:
        Full 30-day action plan as markdown string
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: GOOGLE_API_KEY not set"
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    # Filter for flagged biomarkers
    flagged = [b for b in biomarkers if b.get('status') != 'normal']
    
    if not flagged:
        return "✅ All your biomarkers are normal! Maintain your current healthy habits and retest annually."
    
    # Build comprehensive context
    context = _build_plan_context(flagged, user_profile, research_dict)
    
    system_prompt = """You are a certified functional medicine nutritionist and fitness coach creating a personalised 30-day protocol. 
Base every recommendation on the research provided. Be specific: name exact foods, portion sizes, exercise types, durations. 
No generic advice. Structure the plan EXACTLY as:

## 🎯 Your Priority Areas
[3 bullet points — the most impactful changes based on their specific results]

## 🥗 Nutrition Protocol (Week 1–2)
[5–7 specific dietary changes with foods to ADD and foods to REDUCE. Reference which biomarker each addresses.]

## 🏃 Movement Protocol  
[Specific exercise prescription: type, frequency, duration, intensity — tailored to activity level]

## 💊 Supplement Considerations
[Only suggest if research-backed for their specific flags. Always say "discuss with doctor before starting".]

## 📅 Week-by-Week Milestones
Week 1 | Week 2 | Week 3–4 goals with specific checkpoints

## ⚠️ When to See Your Doctor Urgently
[Any values that warrant prompt medical attention — be clear and direct]

## 🔄 Suggested Re-test Timeline
[Which biomarkers to re-test and when]"""
    
    user_message = f"""Create a personalized 30-day action plan based on this patient profile and lab results:

{context}

Remember: Be specific with foods, portions, and exercises. Base all recommendations on the research provided."""
    
    # Generate response
    plan = ""
    
    try:
        # Combine system prompt with user message
        full_message = f"{system_prompt}\n\n{user_message}"
        response = model.generate_content(full_message)
        plan = response.text
    
    except Exception as e:
        plan = f"Error generating action plan: {str(e)}"
    
    return plan


def _build_plan_context(flagged_biomarkers: List[Dict], user_profile: Dict,
                       research_dict: Dict[str, List[Dict]]) -> str:
    """
    Build comprehensive context for Claude action plan generation.
    
    Args:
        flagged_biomarkers: List of abnormal biomarker dicts
        user_profile: User profile dict
        research_dict: Research studies dict
        
    Returns:
        Context string with all relevant information
    """
    # Patient profile section
    profile_text = f"""## Patient Profile
- Age: {user_profile.get('age', 'Not specified')}
- Sex: {user_profile.get('sex', 'Not specified')}
- Activity Level: {user_profile.get('activity_level', 'moderate')}
- Dietary Preference: {user_profile.get('dietary_preference', 'omnivore')}
- Health Goals: {', '.join(user_profile.get('health_goals', ['general health']))}
"""
    
    # Flagged biomarkers section
    biomarkers_text = "\n## Flagged Biomarkers\n"
    
    for biomarker in flagged_biomarkers:
        name = biomarker.get('name', 'Unknown')
        value = biomarker.get('value', 'N/A')
        unit = biomarker.get('unit', '')
        status = biomarker.get('status', 'unknown')
        range_data = biomarker.get('sex_specific_range', [0, 100])
        percent = biomarker.get('percent_from_range', 0)
        
        # Status emoji
        if status == 'high':
            status_emoji = "🔴 HIGH"
        elif status == 'low':
            status_emoji = "🔴 LOW"
        elif status == 'borderline_high':
            status_emoji = "🟡 BORDERLINE HIGH"
        elif status == 'borderline_low':
            status_emoji = "🟡 BORDERLINE LOW"
        else:
            status_emoji = "⚪ " + status.upper()
        
        biomarkers_text += f"\n### {name} - {status_emoji}\n"
        biomarkers_text += f"- **Result**: {value} {unit}\n"
        biomarkers_text += f"- **Normal Range**: {range_data[0]}-{range_data[1]} {unit}\n"
        biomarkers_text += f"- **Position in Range**: {percent}%\n"
        
        # Add research context for this biomarker
        if name in research_dict and research_dict[name]:
            biomarkers_text += f"- **Research Context**:\n"
            for study in research_dict[name][:2]:  # Top 2 studies
                title = study.get('title', 'Unknown')
                snippet = study.get('abstract_snippet', 'No abstract')
                url = study.get('pubmed_url', '#')
                biomarkers_text += f"  - [{title}]({url})\n    {snippet}\n"
    
    return profile_text + biomarkers_text


def get_dietary_recommendations(biomarker_name: str, status: str) -> List[str]:
    """
    Get evidence-based dietary recommendations for a biomarker.
    
    Args:
        biomarker_name: Name of the biomarker
        status: Current status ('high', 'low', etc.)
        
    Returns:
        List of specific dietary recommendations
    """
    recommendations_db = {
        "Glucose": {
            "high": [
                "Reduce refined carbohydrates (white bread, sugar, pastries)",
                "Increase fiber intake (25-30g daily from vegetables, legumes, whole grains)",
                "Add cinnamon to meals (½ tsp daily may improve glucose control)",
                "Eat protein with every carb source (slows glucose spike)",
                "Limit fruit juice; eat whole fruit instead"
            ],
            "low": [
                "Eat balanced meals every 3-4 hours",
                "Include complex carbs at each meal (oats, sweet potato, beans)",
                "Combine carbs with fat/protein (bread with butter and eggs)"
            ]
        },
        "Total Cholesterol": {
            "high": [
                "Reduce saturated fat (limit red meat, full-fat dairy to 2-3x/week)",
                "Increase omega-3s (2-3 servings fatty fish weekly: salmon, mackerel, sardines)",
                "Add plant sterols (2g daily from oats, nuts, seeds)",
                "Increase soluble fiber (oats, beans, apples, citrus fruit)"
            ]
        },
        "Triglycerides": {
            "high": [
                "Reduce alcohol consumption",
                "Replace refined carbs with whole grains (quinoa, brown rice, barley)",
                "Limit added sugars and high-fructose foods",
                "Increase omega-3 fatty acids (fatty fish, walnuts, flax seeds)",
                "Add exercise (150 min/week can lower triglycerides 20-30%)"
            ]
        },
        "HDL": {
            "low": [
                "Increase aerobic exercise (most effective: 150-200 min/week can raise HDL 5-10%)",
                "Add omega-3 rich foods (salmon, mackerel, walnuts, chia seeds)",
                "Increase olive oil consumption (Mediterranean diet pattern)",
                "Moderate alcohol (1 glass red wine daily for women, 1-2 for men may help)"
            ]
        },
        "LDL": {
            "high": [
                "Reduce saturated fat (keep below 7% of calories)",
                "Eliminate trans fats (processed foods, fried items)",
                "Add plant-based foods rich in fiber (beans, lentils, vegetables)",
                "Include nuts and seeds (1 oz daily: almonds, walnuts)"
            ]
        },
        "TSH": {
            "high": [
                "Ensure adequate iodine intake (seaweed, iodized salt, fish, eggs)",
                "Eat selenium-rich foods (Brazil nuts - 2-3 daily, tuna, turkey)",
                "Include zinc sources (oysters, beef, pumpkin seeds)",
                "Reduce cruciferous vegetables cooking (steamed broccoli, cabbage, kale are fine - just not excessive raw)"
            ]
        },
        "Vitamin D": {
            "low": [
                "Increase sun exposure (15-20 min daily without sunscreen)",
                "Add fatty fish (salmon, mackerel, herring 2-3x weekly)",
                "Include egg yolks (1-2 daily)",
                "Consider mushrooms exposed to sunlight (shiitake, maitake have more D2)",
                "Fortified foods: milk, orange juice, yogurt"
            ]
        },
        "Iron": {
            "low": [
                "Red meat 2-3x weekly (beef, lamb: most absorbable form - heme iron)",
                "Pair iron sources with vitamin C (citrus, bell peppers, tomatoes enhance absorption)",
                "Avoid coffee/tea within 2 hours of iron-rich meals (inhibits absorption)",
                "Include beans, lentils, spinach, pumpkin seeds (non-heme iron, less absorbable)"
            ],
            "high": [
                "Limit red meat to 1-2x weekly",
                "Avoid iron supplements and fortified cereals",
                "Drink tea with meals (tannins reduce absorption)",
                "Limit vitamin C supplements (but food is ok)"
            ]
        },
        "CRP": {
            "high": [
                "Anti-inflammatory foods: fatty fish (EPA/DHA), berries, leafy greens, olive oil",
                "Reduce processed foods and refined carbs",
                "Add turmeric (with black pepper for absorption) to meals",
                "Ginger tea or fresh ginger",
                "Regular aerobic exercise (most effective: 150+ min/week)"
            ]
        },
        "HbA1c": {
            "high": [
                "Same as elevated Glucose - focus on reducing refined carbs",
                "Track portion sizes (use plate method: ½ vegetables, ¼ protein, ¼ carbs)",
                "Walk 10-15 min after meals (reduces post-meal glucose spike)"
            ]
        }
    }
    
    return recommendations_db.get(biomarker_name, {}).get(status, [
        "Consult with your healthcare provider and a registered dietitian for personalized recommendations"
    ])
