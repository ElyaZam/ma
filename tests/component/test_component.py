import requests

task_manager_url = 'http://localhost:8000'
get_tasks_url = f'{task_manager_url}/get_tasks'
get_task_by_id_url = f'{task_manager_url}/get_task_by_id'
add_task_url = f'{task_manager_url}/add_task'
delete_task_url = f'{task_manager_url}/delete_task'

quote_url = 'http://localhost:8001'
random_quote_url = f'{quote_url}/'

new_task = {
    "id": 0,
    "task_name": "Complete the report",
    "description": "Finalize and submit the quarterly report",
    "importance": 5,
    "due_date": "2024-04-30T12:00:00"
}

def test_1_add_task():
    res = requests.post(f"{add_task_url}", json=new_task)
    assert res.status_code == 200

def test_2_get_tasks():
    res = requests.get(f"{get_tasks_url}").json()
    assert new_task in res

def test_3_get_task_by_id():
    res = requests.get(f"{get_task_by_id_url}?task_id=0").json()
    assert res == new_task

def test_4_delete_task():
    res = requests.delete(f"{delete_task_url}?task_id=0").json()
    assert res == "Success"

def test_5_random_quote():
    res = requests.get(f"{random_quote_url}")
    assert res.status_code == 200