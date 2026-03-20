# TODO: Napisz testy dla endpointow User




def test_create_user(client):
    """Test tworzenia uzytkownika."""
    
    test_user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }

    response = client.post("/users/", json=test_user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["is_active"] == True






def test_get_users(client):
    """Test pobierania listy uzytkownikow."""
    # Najpierw utworz uzytkownika
    # Potem pobierz liste
    test_user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }

    response = client.post("/users/", json=test_user_data)
    assert response.status_code == 201

    get_users = client.get("/users/")
    assert get_users.status_code == 200
    data = get_users.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["username"] == "testuser"





def test_get_user_not_found(client):
    """Test 404 dla nieistniejacego uzytkownika."""
    response = client.get("/users/999")
    assert response.status_code == 404





def test_update_user(client):
    """Test aktualizacji uzytkownika."""

    test_user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }

    response = client.post("/users/", json=test_user_data)
    assert response.status_code == 201
    
    user_id = response.json()["id"]    

    update_data = {"username": "new_test_name"}
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["username"] == "new_test_name"






def test_delete_user(client):
    """Test usuwania uzytkownika."""

    test_user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }

    response = client.post("/users/", json=test_user_data)
    assert response.status_code == 201

    user_id = response.json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    get_id = client.get(f"/users/{user_id}")
    assert get_id.status_code == 404



def test_create_duplicate_username(client):
    """Test ze nie mozna utworzyc dwoch userow z tym samym username."""
    test_user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }

    first = client.post("/users/", json=test_user_data)
    assert first.status_code == 201   # pierwszy przechodzi

    second = client.post("/users/", json=test_user_data)
    assert second.status_code == 400  # drugi odpada — duplikat
