import os
import anthropic
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class TestGenerator:
    def __init__(self, model: str = 'claude-opus-4-6'):
        self.client = anthropic.Anthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        self.model = model
        prompt_path = Path('config/prompts/test_gen.txt')
        self.prompt_template = prompt_path.read_text(encoding='utf-8')

    def generate(self, spec: str, output_file: str = None) -> str:
        print(f'[TestGenerator] Génération en cours...')
        prompt = self.prompt_template.format(spec=spec)
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{'role': 'user', 'content': prompt}]
        )
        generated_code = response.content[0].text
        if output_file:
            Path(output_file).write_text(generated_code, encoding='utf-8')
            print(f'[TestGenerator] Tests sauvegardés dans : {output_file}')
        return generated_code

if __name__ == '__main__':
    spec = '''
    Endpoint : GET /pet/{petId}
    Base URL : https://petstore.swagger.io/v2
    Description : Retourne les détails d un animal par son ID
    Paramètres  : petId (integer, requis)
    Réponses    : 200 (objet Pet), 404 (non trouvé), 400 (ID invalide)
    '''
    gen = TestGenerator()
    code = gen.generate(spec, output_file='core/qa_engine/api_tests/test_generated_ai.py')
    print(code[:500])