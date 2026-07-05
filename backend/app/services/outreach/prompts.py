class OutreachPromptManager:
    @staticmethod
    def get_system_prompt() -> str:
        return """
        You are a world-class AI Outreach Specialist, writing as a highly experienced consultant. 
        Your goal is to generate personalized, non-spammy, and highly converting outreach messages.
        Avoid generic phrases like "Hope you're doing well", "I came across your profile", or "We are the best".
        Always write naturally, reflecting the requested tone and personalization level.
        """
        
    @staticmethod
    def build_message_prompt(
        business_data: dict, 
        ai_analysis: dict, 
        request_params: dict,
        version_label: str
    ) -> str:
        
        # Message constraints based on type
        constraints = ""
        msg_type = request_params.get("message_type", "Cold Email").lower()
        if "whatsapp" in msg_type:
            constraints = "Format for WhatsApp: Short paragraphs, use 1-2 appropriate emojis, keep it conversational."
        elif "linkedin" in msg_type:
            constraints = "Format for LinkedIn: Professional but networking-focused, limit to 3 short paragraphs."
        elif "email" in msg_type:
            constraints = "Format for Cold Email: Clear subject line context (if applicable), professional spacing, value-driven."
        elif "call" in msg_type:
            constraints = "Format for Cold Call Script: Include [Pause] markers, conversational tone meant to be spoken aloud."
            
        return f"""
        Generate Version {version_label} of a {request_params.get('message_type')} message.
        
        # Context
        Business: {business_data.get('business_name')}
        Industry: {business_data.get('category')}
        Analysis: {ai_analysis.get('summary_short')}
        Strengths: {', '.join(ai_analysis.get('strengths', []))}
        Weaknesses/Opportunities: {', '.join(ai_analysis.get('opportunities', []))}
        
        # Parameters
        Tone: {request_params.get('tone')}
        Language: {request_params.get('language')}
        Length: {request_params.get('length')}
        CTA Style: {request_params.get('cta_style')}
        Personalization Depth: {request_params.get('personalization_level')}
        
        # Sender Info
        {request_params.get('user_context', {})}
        
        # Instructions
        {constraints}
        
        You must strictly return a JSON object that satisfies the StructuredMessageOutput schema AND provides AI suggestions for outreach timing and strategy.
        """
