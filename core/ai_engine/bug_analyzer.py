import os
import json
import anthropic
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class BugAnalyzer:
    def __init__(self, model: str = 'claude-opus-4-6'):
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = model
        prompt_path = Path('config/prompts/bug_analysis.txt')
        self.prompt_template = prompt_path.read_text(encoding='utf-8')

    def analyze(self, traceback: str, context: str = '') -> dict:
        prompt = self.prompt_template.format(
            traceback=traceback,
            context=context or 'Non spécifié'
        )
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[{'role': 'user', 'content': prompt}]
        )
        raw_text = response.content[0].text.strip()
        try:
            start = raw_text.find('{')
            end = raw_text.rfind('}') + 1
            return json.loads(raw_text[start:end])
        except:
            return {'root_cause': raw_text, 'severity': 'unknown'}

    def format_report(self, analysis: dict) -> str:
        sev = analysis.get('severity', 'unknown')
        return (
            f'\n{"="*50}\n'
            f'  BUG ANALYSIS REPORT\n'
            f'{"="*50}\n'
            f'  Severity   : [{sev.upper()}]\n'
            f'  Category   : {analysis.get("category", "N/A")}\n'
            f'  Root Cause : {analysis.get("root_cause", "N/A")}\n'
            f'  Fix        : {analysis.get("suggested_fix", "N/A")}\n'
            f'{"="*50}\n'
        )

if __name__ == '__main__':
    fake_traceback = '''
    FAILED test_petstore_api.py::TestPetAPI::test_get_pet_success
    AssertionError: assert 404 == 200
    '''
    analyzer = BugAnalyzer()
    result = analyzer.analyze(fake_traceback, context='Test API Petstore')
    print(analyzer.format_report(result))