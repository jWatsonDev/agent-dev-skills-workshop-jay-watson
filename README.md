# Agent Dev Skills Workshop — Jay Watson

Workshop exercises building AI agents with Google's Agent Development Kit (ADK): function tools, callbacks and guardrails, multi-agent orchestration, session state, and multi-model support.

## Challenge 1 — Building an Agent with Custom Tools

`Challenge1_JayWatson.ipynb`

An ADK weather agent that:
- Uses a custom tool wrapping the National Weather Service API (lat/long → current forecast)
- Uses a custom tool wrapping the Google Maps Geocoding API (city/state → lat/long)
- Supports both Gemini and a third-party model (Claude Haiku via LiteLLM, routed through a SAIC gateway)
- Is tested against multiple US cities with both models
