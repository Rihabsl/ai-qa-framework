"""
Fichier généré automatiquement par test_generator.py via Claude (Anthropic).
Spec donnée : GET /pet/{petId} — Petstore Swagger API
Date de génération : 2026-02-22
"""

import pytest
import allure
import requests

BASE_URL = "https://petstore.swagger.io/v2"


# ── FIXTURES ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def session():
    """Session HTTP réutilisée pour tous les tests du module."""
    s = requests.Session()
    s.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    return s


@pytest.fixture(scope="module")
def existing_pet_id(session):
    """
    Crée un animal avant les tests et retourne son ID.
    Garantit qu'on teste sur une donnée réelle et contrôlée.
    """
    pet = {
        "id": 112233,
        "name": "ClaudeGeneratedPet",
        "status": "available",
        "photoUrls": ["https://example.com/pet.jpg"]
    }
    session.post(f"{BASE_URL}/pet", json=pet)
    return pet["id"]


# ── TESTS NOMINAUX (cas qui doivent réussir) ──────────────────────────────────

@allure.feature("Pet API — GET /pet/{petId}")
@allure.title("GET /pet/{id} — Récupérer un animal existant → 200")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_pet_success(session, existing_pet_id):
    """
    Pourquoi ce test : vérifier le cas nominal — un animal existant
    doit retourner 200 avec les bonnes données.
    """
    response = session.get(f"{BASE_URL}/pet/{existing_pet_id}")

    # Vérification du code HTTP
    assert response.status_code == 200, (
        f"Attendu 200, reçu {response.status_code}"
    )

    # Vérification du body JSON
    data = response.json()
    assert data["id"] == existing_pet_id, "L'ID retourné ne correspond pas"
    assert data["name"] == "ClaudeGeneratedPet", "Le nom ne correspond pas"
    assert data["status"] == "available", "Le statut ne correspond pas"
    assert "photoUrls" in data, "Le champ photoUrls est manquant"


@allure.feature("Pet API — GET /pet/{petId}")
@allure.title("GET /pet/{id} — Vérifier la structure complète du body")
@allure.severity(allure.severity_level.NORMAL)
def test_get_pet_response_structure(session, existing_pet_id):
    """
    Pourquoi ce test : vérifier que tous les champs attendus
    sont présents dans la réponse — pas seulement le status code.
    """
    response = session.get(f"{BASE_URL}/pet/{existing_pet_id}")
    data = response.json()

    required_fields = ["id", "name", "status", "photoUrls"]
    for field in required_fields:
        assert field in data, f"Champ obligatoire manquant : {field}"


# ── TESTS D'ERREUR (cas qui doivent échouer) ──────────────────────────────────

@allure.feature("Pet API — GET /pet/{petId}")
@allure.title("GET /pet/{id} — Animal inexistant → 404")
@allure.severity(allure.severity_level.NORMAL)
def test_get_pet_not_found(session):
    """
    Pourquoi ce test : vérifier que l'API gère correctement
    une ressource inexistante — elle doit retourner 404, pas 500.
    """
    response = session.get(f"{BASE_URL}/pet/9999999999")

    assert response.status_code == 404, (
        f"Un animal inexistant doit retourner 404, reçu {response.status_code}"
    )


@allure.feature("Pet API — GET /pet/{petId}")
@allure.title("GET /pet/{id} — ID non numérique → 400")
@allure.severity(allure.severity_level.MINOR)
def test_get_pet_invalid_id_format(session):
    """
    Pourquoi ce test : vérifier que l'API rejette les requêtes mal formées.
    Un ID textuel n'est pas valide — l'API doit retourner 400.
    """
    response = session.get(f"{BASE_URL}/pet/not-a-valid-id")

    assert response.status_code in [400, 404], (
        f"Un ID invalide doit retourner 400 ou 404, reçu {response.status_code}"
    )


@allure.feature("Pet API — GET /pet/{petId}")
@allure.title("GET /pet/{id} — ID négatif → comportement défini")
@allure.severity(allure.severity_level.MINOR)
def test_get_pet_negative_id(session):
    """
    Pourquoi ce test : cas limite — un ID négatif est techniquement
    un entier mais ne devrait pas exister. L'API doit gérer ça proprement.
    """
    response = session.get(f"{BASE_URL}/pet/-1")

    assert response.status_code in [400, 404], (
        f"Un ID négatif doit retourner 400 ou 404, reçu {response.status_code}"
    )


# ── TEST DE PERFORMANCE BASIQUE ───────────────────────────────────────────────

@allure.feature("Pet API — GET /pet/{petId}")
@allure.title("GET /pet/{id} — Temps de réponse < 2 secondes")
@allure.severity(allure.severity_level.NORMAL)
def test_get_pet_response_time(session, existing_pet_id):
    """
    Pourquoi ce test : vérifier que l'API répond dans un délai acceptable.
    Une réponse > 2 secondes indique un problème de performance.
    """
    import time
    start = time.time()
    response = session.get(f"{BASE_URL}/pet/{existing_pet_id}")
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 2.0, (
        f"Temps de réponse trop lent : {elapsed:.2f}s (max: 2s)"
    )
