import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

class MusicLLM:
    def __init__(self, temperature=0.7):
        self.llm = ChatGroq(
            temperature = temperature,
            groq_api_key = os.getenv("GROQ_API_KEY"),
            model_name="openai/gpt-oss-120b"
        )
        
    def generate_melody(self, user_input):
        """Whatever user enters based on that genearte melody for creating notes_list"""
        prompt = ChatPromptTemplate.from_template(
            "Generate a melody based on this input: {input}. Represent it as a space seperated notes (eg., C4 D4 E4)"
        )
        
        chain = prompt | self.llm
        return chain.invoke({"input": user_input}).content.strip()
    
    def generate_harmony(self, melody):
        """From the notes/melody created which are scattered sync them into an harmony for creating music"""
        prompt = ChatPromptTemplate.from_template(
            "Create harmony chords for this melody: {melody}. Format: C4-E4-G4 F4-A4-C5"
        )
        
        chain = prompt | self.llm
        return chain.invoke({"melody" : melody }).content.strip()
    
    def generate_rhythm(self,melody):
        """Create beats based on the melody"""
        prompt = ChatPromptTemplate.from_template(
            "Suggest rhythm durations (in beats) for this melody: {melody}. Format: 1.0 0.5 0.5 2.0"
        )

        chain = prompt | self.llm
        return chain.invoke({"melody" : melody }).content.strip()
        
    def adapt_style(self, style, melody, harmony, rhythm):
        """Based of style change the melody, harmony, rhythm"""
        prompt = ChatPromptTemplate.from_template(
            "Adapt to {style} style: \n Melody: {melody}\nHarmony: {harmony}\n Rhythm: {rhythm}\nOutput single string summary"
        )
        
        chain = prompt | self.llm
        
        return chain.invoke({
            "style" : style,
            "melody" : melody,
            "harmony" : harmony,
            "rhythm" :rhythm
        }).content.strip()
    
        
        