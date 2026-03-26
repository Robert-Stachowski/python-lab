# TODO: Napisz testy dla endpointow Project



def test_create_project(test_project, test_user):
    """Test tworzenia projektu."""
    # Najpierw utworz usera (owner)
    # Potem utworz projekt
       

    assert test_user["username"] == "test_data_username"
    assert test_user["email"] == "example@exapmle.pl"

    
    assert test_project["name"] == "Test projekt numer jeden. "
    assert test_project["description"] == "Opis projektu. "
    assert test_project["owner_id"] == test_user["id"]







def test_get_project_with_tasks(client, test_project, test_user, auth_token):
    """Test pobierania projektu z zadaniami."""


    task_data = {
        "title": "Moje zadanie przykładowe",
        "project_id": test_project["id"],
        "assignee_id": test_user["id"]
    }
    response = client.post("/tasks/", json = task_data, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Moje zadanie przykładowe"
    assert data["project_id"] == test_project["id"]
    assert data["assignee_id"] == test_user["id"]

    project_id = test_project["id"]
    project_with_tasks = client.get(f"/projects/{project_id}")
    assert project_with_tasks.status_code == 200

    data_project = project_with_tasks.json()
    assert data_project["tasks"][0]["title"] == "Moje zadanie przykładowe"
    assert len(data_project["tasks"]) == 1
    assert data_project["name"] == "Test projekt numer jeden. "
    assert data_project["owner_id"] == test_user["id"]

    






def test_delete_project_cascades_tasks(client, test_project, test_user, auth_token):
    """Test - usuwanie projektu kasuje też zadania."""

    task_data = {
        "title": "Moje zadanie przykładowe",
        "project_id": test_project["id"],
        "assignee_id": test_user["id"]
    }
    response = client.post("/tasks/", json = task_data, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201

    task_id = response.json()["id"]

    data = response.json()
    assert data["title"] == "Moje zadanie przykładowe"
    assert data["project_id"] == test_project["id"]
    assert data["assignee_id"] == test_user["id"]

    project_id = test_project["id"]
    project_with_tasks = client.get(f"/projects/{project_id}")
    assert project_with_tasks.status_code == 200

    data_project = project_with_tasks.json()
    assert data_project["tasks"][0]["title"] == "Moje zadanie przykładowe"
    assert len(data_project["tasks"]) == 1
    assert data_project["name"] == "Test projekt numer jeden. "
    assert data_project["owner_id"] == test_user["id"]

    delete_project = client.delete(f"/projects/{project_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert delete_project.status_code == 204

    find_project = client.get(f"/projects/{project_id}")
    assert find_project.status_code == 404

    find_tasks = client.get(f"/tasks/{task_id}")
    assert find_tasks.status_code == 404
