# TODO: Napisz testy dla endpointow Task




def test_create_task(client, test_user, test_project, test_task):
    """Test tworzenia zadania."""
    # Najpierw utworz usera i projekt
    # Potem utworz zadanie


    assert test_user["username"] == "test_data_username"
    assert test_user["email"] == "example@exapmle.pl"

    
    assert test_project["name"] == "Test projekt numer jeden. "
    assert test_project["description"] == "Opis projektu. "
    assert test_project["owner_id"] == test_user["id"]
    
    project_id = test_project["id"]


    assert test_task["title"] == "Przykładowy tytuł zadania"
    assert test_task["description"] == "Przykładowy opis zadania"
    assert test_task["project_id"] == project_id








def test_filter_tasks_by_status(client, test_project, test_user, auth_token):
    """Test filtrowania zadan po statusie."""



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

    task_param_status = client.get("/tasks/", params={"status":"todo"})
    assert task_param_status.status_code == 200

    tasks = task_param_status.json()
    assert len(tasks["items"]) == 1
    assert tasks["items"][0]["status"] == "todo"








def test_update_task_status(client, test_project, test_user, auth_token):
    """Test zmiany statusu zadania."""


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

    update_status = {"status": "done"}
    task_status_update = client.patch(f"/tasks/{task_id}/status", json = update_status, headers={"Authorization": f"Bearer {auth_token}"})
    assert task_status_update.status_code == 200
    assert task_status_update.json()["status"] == "done"







def test_add_tag_to_task(client, test_project, test_user, auth_token):
    """Test dodawania taga do zadania."""

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



    tag_data = {
        "name": "Nowa nazwa tagu"
    }
    add_tag = client.post("/tags/", json = tag_data)
    assert add_tag.status_code == 201

    data_tag = add_tag.json()
    assert data_tag["name"] == "Nowa nazwa tagu"


    add_tag_to_task = client.post(f"/tags/tasks/{task_id}/tags", json = tag_data)
    assert add_tag_to_task.status_code == 200
    assert add_tag_to_task.json()["name"] == "Nowa nazwa tagu"
    







def test_filter_tasks_by_priority(client, test_project, test_user, auth_token):
    """Test filtrowania po priorytecie."""

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

    task_priority_filter = client.get("/tasks/", params={"priority": "medium"})
    assert task_priority_filter.status_code == 200

    tasks = task_priority_filter.json()
    assert len(tasks["items"]) == 1
    assert tasks["items"][0]["priority"] == "medium"



def test_delete_task(client, test_user, test_task, test_project, auth_token):
    assert test_user["username"] == "test_data_username"
    assert test_user["email"] == "example@exapmle.pl"

    
    assert test_project["name"] == "Test projekt numer jeden. "
    assert test_project["description"] == "Opis projektu. "
    assert test_project["owner_id"] == test_user["id"]
    
    project_id = test_project["id"]


    assert test_task["title"] == "Przykładowy tytuł zadania"
    assert test_task["description"] == "Przykładowy opis zadania"
    assert test_task["project_id"] == project_id


    delete_task = client.delete(f"/tasks/{test_task['id']}", headers={"Authorization": f"Bearer {auth_token}"})
    assert delete_task.status_code == 204

    find_task = client.get(f"/tasks/{test_task['id']}")
    assert find_task.status_code == 404