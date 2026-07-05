class PromptManager:
    @staticmethod
    def build_analysis_prompt(business_data: dict) -> str:
        """
        Builds the prompt for business analysis.
        """
        return f"""
        You are an expert Business Analyst and Web Intelligence Strategist.
        I am going to provide you with raw data about a business.
        Your goal is to analyze this data and generate a structured JSON response evaluating 
        the business as a potential outreach prospect for a digital agency.
        
        # Business Data
        Name: {business_data.get('business_name')}
        Category: {business_data.get('category')}
        Website: {business_data.get('website')}
        Phone: {business_data.get('phone')}
        Email: {business_data.get('email')}
        Google Rating: {business_data.get('google_rating')}
        Reviews: {business_data.get('review_count')}
        Location: {business_data.get('city')}, {business_data.get('state')}, {business_data.get('country')}
        Website Status: {business_data.get('website_status')}
        Source Confidence: {business_data.get('confidence_score')}
        
        # Output Requirements
        You MUST return ONLY a valid JSON object matching the requested schema.
        1. summary_short: A 1-2 sentence quick summary of what they do.
        2. summary_medium: A 1-paragraph overview of their current digital presence.
        3. summary_long: A detailed 2-3 paragraph analysis covering strengths, weaknesses, and digital maturity.
        4. strengths: Top 3-5 positive aspects (array of strings).
        5. weaknesses: Top 3-5 negative or missing aspects (array of strings).
        6. opportunities: Top 3-5 potential growth areas (array of strings).
        7. opportunity_score: Integer from 0 to 100 representing how good of a lead they are.
        8. confidence_score: Float from 0.0 to 1.0 representing your confidence in this analysis based on provided data.
        9. ai_tags: Array of 4-6 short tags describing the business (e.g. "High Budget", "Needs SEO").
        10. estimated_budget: A string estimate (e.g., "$1k-$5k", "$10k+").
        11. recommended_services: Array of 3-5 digital services they likely need (e.g. "Website Redesign", "SEO").
        """
