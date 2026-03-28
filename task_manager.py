#!/usr/bin/env python3
"""A simple command-line task manager with file persistence."""

import json
import os
import sys
from datetime import datetime


DATA_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(title, priority="medium"):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority,
        "done": False,
        "created": datetime.now().isoformat(),
        "completed": None,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {title} [{priority}]")


def list_tasks(show_all=False):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    pending = [t for t in tasks if not t["done"]]
    done = [t for t in tasks if t["done"]]
    if pending:
        print("\n--- Pending Tasks ---")
        for t in pending:
            marker = "[ ]"
            print(f"  {marker} #{t['id']} {t['title']} ({t['priority']})")
    if show_all and done:
        print("\n--- Completed Tasks ---")
        for t in done:
            marker = "[x]"
            print(f"  {marker} #{t['id']} {t['title']} ({t['priority']})")
    total = len(tasks)
    completed = len(done)
    print(f"\nTotal: {total} | Done: {completed} | Pending: {total - completed}")


def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            if t["done"]:
                print(f"Task #{task_id} is already completed.")
                return
            t["done"] = True
            t["completed"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Completed task #{task_id}: {t['title']}")
            return
    print(f"Task #{task_id} not found.")


def delete_task(task_id):
    tasks = load_tasks()
    filtered = [t for t in tasks if t["id"] != task_id]
    if len(filtered) == len(tasks):
        print(f"Task #{task_id} not found.")
        return
    save_tasks(filtered)
    print(f"Deleted task #{task_id}.")


def search_tasks(keyword):
    tasks = load_tasks()
    results = [t for t in tasks if keyword.lower() in t["title"].lower()]
    if not results:
        print(f"No tasks matching '{keyword}'.")
        return
    print(f"\nSearch results for '{keyword}':")
    for t in results:
        status = "[x]" if t["done"] else "[ ]"
        print(f"  {status} #{t['id']} {t['title']} ({t['priority']})")


def print_usage():
    print("Usage: python task_manager.py <command> [args]")
    print()
    print("Commands:")
    print("  add <title> [priority]  Add a task (priority: low/medium/high)")
    print("  list                    List pending tasks")
    print("  list all                List all tasks including completed")
    print("  done <id>               Mark a task as completed")
    print("  delete <id>             Delete a task")
    print("  search <keyword>        Search tasks by keyword")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    command = sys.argv[1].lower()
    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide a task title.")
            return
        title = sys.argv[2]
        priority = sys.argv[3] if len(sys.argv) > 3 else "medium"
        if priority not in ("low", "medium", "high"):
            print("Error: Priority must be low, medium, or high.")
            return
        add_task(title, priority)
    elif command == "list":
        show_all = len(sys.argv) > 2 and sys.argv[2].lower() == "all"
        list_tasks(show_all)
    elif command == "done":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
            return
        complete_task(int(sys.argv[2]))
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
            return
        delete_task(int(sys.argv[2]))
    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: Please provide a search keyword.")
            return
        search_tasks(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        print_usage()


if __name__ == "__main__":
    main()
