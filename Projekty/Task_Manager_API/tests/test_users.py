# TODO: Napisz testy dla endpointow User

# def test_create_user(client):
#     """Test tworzenia uzytkownika."""
#     response = client.post("/users/", json={
#         "username": "testuser",
#         "email": "test@example.com"
#     })
#     assert response.status_code == 201
#     data = response.json()
#     assert data["username"] == "testuser"
#     assert data["email"] == "test@example.com"
#     assert data["is_active"] == True

# def test_get_users(client):
#     """Test pobierania listy uzytkownikow."""
#     # Najpierw utworz uzytkownika
#     # Potem pobierz liste
#     pass

# def test_get_user_not_found(client):
#     """Test 404 dla nieistniejacego uzytkownika."""
#     response = client.get("/users/999")
#     assert response.status_code == 404

# def test_update_user(client):
#     """Test aktualizacji uzytkownika."""
#     pass

# def test_delete_user(client):
#     """Test usuwania uzytkownika."""
#     pass

# def test_create_duplicate_username(client):
#     """Test ze nie mozna utworzyc dwoch userow z tym samym username."""
#     pass
