import pytest
import allure

@allure.feature('Pet API — CRUD')
class TestPetAPI:

    @allure.title('POST /pet — Créer un animal')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_pet_success(self, session, base_url, sample_pet):
        response = session.post(f'{base_url}/pet', json=sample_pet)
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == sample_pet['name']
        assert data['status'] == 'available'

    @allure.title('GET /pet/{id} — Récupérer un animal existant')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_pet_success(self, session, base_url, sample_pet):
        session.post(f'{base_url}/pet', json=sample_pet)
        response = session.get(f'{base_url}/pet/{sample_pet["id"]}')
        assert response.status_code == 200
        assert response.json()['id'] == sample_pet['id']

    @allure.title('GET /pet/{id} — Animal inexistant → 404')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_pet_not_found(self, session, base_url):
        response = session.get(f'{base_url}/pet/9999999999')
        assert response.status_code == 404

    @allure.title('GET /pet/{id} — ID invalide → 400')
    @allure.severity(allure.severity_level.MINOR)
    def test_get_pet_invalid_id(self, session, base_url):
        response = session.get(f'{base_url}/pet/not-a-number')
        assert response.status_code in [400, 404]

    @allure.title('PUT /pet — Mettre à jour le statut')
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_pet_status(self, session, base_url, sample_pet):
        session.post(f'{base_url}/pet', json=sample_pet)
        updated_pet = {**sample_pet, 'status': 'sold'}
        response = session.put(f'{base_url}/pet', json=updated_pet)
        assert response.status_code == 200
        assert response.json()['status'] == 'sold'

    @allure.title('DELETE /pet/{id} — Supprimer un animal')
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_pet_success(self, session, base_url, sample_pet):
        session.post(f'{base_url}/pet', json=sample_pet)
        response = session.delete(f'{base_url}/pet/{sample_pet["id"]}')
        assert response.status_code == 200
        verify = session.get(f'{base_url}/pet/{sample_pet["id"]}')
        assert verify.status_code == 404