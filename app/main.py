import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


STYLE_GUIDANCE = {
    "Sad": "Use a minor or modal feel, a restrained contour, and spacious phrasing.",
    "Happy": "Use a bright major feel, an upbeat contour, and lively phrasing.",
    "Jazz": "Use jazzy seventh or extended chords, chromatic color, and a swing-friendly feel.",
    "Romantic": "Use a lyrical contour, warm harmonies, and expressive phrasing.",
    "Extreme": "Use bold chromatic choices, wide melodic leaps, and an unpredictable feel.",
}


class MusicLLM:
    def __init__(self, temperature=1.0):
        self.llm = ChatGroq(
            temperature=temperature,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="openai/gpt-oss-120b",
        )

    def generate_melody(self, user_input, style):
        """Generate a distinct, style-aware melody as a list of note names."""
        prompt = ChatPromptTemplate.from_template(
            "Compose an original 8-note melody for this request: {input}\n"
            "Style: {style}. Musical direction: {guidance}\n"
            "Give this result its own character: vary its contour and use a memorable "
            "motif rather than a generic scale. Return only 8 space-separated pitch "
            "names such as C4 D4 E4 F4 G4 A4 B4 C5."
        )

        chain = prompt | self.llm
        return chain.invoke(
            {
                "input": user_input,
                "style": style,
                "guidance": STYLE_GUIDANCE.get(style, "Use a distinctive musical character."),
            }
        ).content.strip()

    def generate_harmony(self, melody, style):
        """Generate style-aware chords that support the melody."""
        prompt = ChatPromptTemplate.from_template(
            "Create 8 style-appropriate harmony chords for this melody: {melody}\n"
            "Style: {style}. Musical direction: {guidance}\n"
            "Return only 8 space-separated chords, with notes separated by hyphens, "
            "for example C4-E4-G4 F4-A4-C5."
        )

        chain = prompt | self.llm
        return chain.invoke(
            {
                "melody": melody,
                "style": style,
                "guidance": STYLE_GUIDANCE.get(style, "Use a distinctive musical character."),
            }
        ).content.strip()

    def generate_rhythm(self, melody, style):
        """Generate a style-aware rhythmic pattern in beats."""
        prompt = ChatPromptTemplate.from_template(
            "Create an expressive rhythm in beats for this melody: {melody}\n"
            "Style: {style}. Musical direction: {guidance}\n"
            "Return exactly 8 positive beat durations as space-separated numbers. "
            "Use varied values between 0.25 and 2.0, such as 1.0 0.5 0.5 2.0."
        )

        chain = prompt | self.llm
        return chain.invoke(
            {
                "melody": melody,
                "style": style,
                "guidance": STYLE_GUIDANCE.get(style, "Use a distinctive musical character."),
            }
        ).content.strip()

    def adapt_style(self, style, melody, harmony, rhythm):
        """Summarize the style-aware musical choices."""
        prompt = ChatPromptTemplate.from_template(
            "Summarize this {style} composition in one sentence:\n"
            "Melody: {melody}\nHarmony: {harmony}\nRhythm: {rhythm}"
        )

        chain = prompt | self.llm

        return chain.invoke({
            "style": style,
            "melody": melody,
            "harmony": harmony,
            "rhythm": rhythm,
        }).content.strip()
        