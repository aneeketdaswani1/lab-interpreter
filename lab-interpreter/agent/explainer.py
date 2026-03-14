"""
Claude AI Explanation Module
Uses Claude API to generate explanations and insights
"""
import os
from anthropic import Anthropic


class ClaudeExplainer:
    """Generate biomarker explanations using Claude AI"""
    
    def __init__(self, api_key: str = None):
        """Initialize Claude client"""
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
    
    def explain_biomarkers(self, biomarkers: list, context: str = "") -> str:
        """Generate explanation for biomarker results"""
        biomarker_text = "\n".join([
            f"- {b.get('name')}: {b.get('value')} {b.get('unit', '')} ({b.get('status', 'unknown')})"
            for b in biomarkers
        ])
        
        prompt = f"""You are a medical professional explaining lab results to a patient.
        
Biomarker Results:
{biomarker_text}

Additional Context: {context}

Provide:
1. Clear explanation of what these biomarkers mean
2. Health implications
3. When to be concerned
4. Recommendations for follow-up

Keep the explanation clear but comprehensive."""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error generating explanation: {str(e)}"
    
    def get_health_insights(self, biomarkers: list) -> str:
        """Generate personalized health insights"""
        prompt = f"""Based on these biomarker results, provide 3-5 key health insights:
{json.dumps(biomarkers, indent=2)}

Focus on actionable intelligence and patterns."""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error generating insights: {str(e)}"
