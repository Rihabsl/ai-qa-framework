import os
import anthropic
from playwright.sync_api import Page
from dotenv import load_dotenv

load_dotenv()

class SelfHealer:
    def __init__(self, model: str = 'claude-opus-4-6'):
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = model
        self.healed_selectors = {}

    def find_alternative_selector(
        self, page: Page, broken_selector: str, element_description: str
    ) -> str:
        print(f'[SelfHealer] Sélecteur cassé : {broken_selector}')
        html_snippet = page.content()[:6000]

        prompt = f'''
Le sélecteur CSS suivant ne fonctionne plus : {broken_selector}
Description de l'élément cible : {element_description}

HTML de la page :
{html_snippet}

Propose le meilleur sélecteur CSS alternatif.
Réponds avec UNIQUEMENT le sélecteur, rien d'autre.
'''
        response = self.client.messages.create(
            model=self.model,
            max_tokens=200,
            messages=[{'role': 'user', 'content': prompt}]
        )
        new_selector = response.content[0].text.strip()
        self.healed_selectors[broken_selector] = new_selector
        print(f'[SelfHealer] Nouveau sélecteur : {new_selector}')
        return new_selector

    def safe_click(self, page: Page, selector: str, description: str):
        try:
            page.click(selector, timeout=3000)
        except Exception:
            healed = self.find_alternative_selector(page, selector, description)
            page.click(healed)

    def safe_fill(self, page: Page, selector: str, value: str, description: str):
        try:
            page.fill(selector, value, timeout=3000)
        except Exception:
            healed = self.find_alternative_selector(page, selector, description)
            page.fill(healed, value)

    def get_healing_report(self) -> str:
        if not self.healed_selectors:
            return 'Aucun sélecteur réparé dans cette session.'
        lines = ['=== SELF-HEALING REPORT ===', '']
        for old, new in self.healed_selectors.items():
            lines.append(f'  CASSÉ  : {old}')
            lines.append(f'  RÉPARÉ : {new}')
            lines.append('')
        return '\n'.join(lines)