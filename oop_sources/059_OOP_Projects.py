###############################################################################
# TOPIC: OOP Projects - Task scheduling and Execution Engine mini-project
#
# 1. DEFINITION & INTRODUCTION:
#    - This topic implements a complete, runnable OOP mini-project demonstrating clean
#      architectural design in Python.
#    - Project: **Distributed Task Scheduler and Execution Engine**
#    - Features:
#        - Abstract `Task` base class defining the job contract interface.
#        - Concrete Task implementations (`FileDownloadTask`, `DatabaseBackupTask`).
#        - Task runner context manager to track execution state, measure durations, and
#          rollback resources on failure.
#        - A centralized `TaskScheduler` class aggregating tasks, organizing queues, and executing
#          jobs polymorphically.
#
# 2. KEY PATTERNS INTEGRATED:
#    - Abstraction (abc.ABC contracts).
#    - Composition/Aggregation (scheduler aggregates tasks).
#    - Context Managers (tracking runtime metrics).
#    - Polymorphism (executing tasks through the uniform `execute()` method).
#
###############################################################################

import abc  # Standard module for interface definitions
import time  # Standard module to measure time offsets

# =============================================================================
# 1. THE TASK INTERFACE
# =============================================================================
class Task(abc.ABC):
    def __init__(self, name, priority=1):
        self.name = name
        self.priority = priority
        self.status = "PENDING"
        
    @abc.abstractmethod
    def execute(self) -> bool:
        """Run the core logic of the task. Return True if success, else False."""
        pass
        
    def __repr__(self):
        return f"Task(Name: {self.name}, Priority: {self.priority}, Status: {self.status})"

# =============================================================================
# 2. CONCRETE TASK IMPLEMENTATIONS
# =============================================================================
class FileDownloadTask(Task):
    def __init__(self, name, url, file_size_mb, priority=1):
        super().__init__(name, priority)
        self.url = url
        self.file_size = file_size_mb
        
    def execute(self) -> bool:
        print(f" -> Downloading data from URL: '{self.url}' ({self.file_size} MB)...")
        # Simulating download delay
        time.sleep(0.1)
        print(" -> Download completed successfully.")
        return True

class DatabaseBackupTask(Task):
    def __init__(self, name, db_name, fail_simulated=False, priority=1):
        super().__init__(name, priority)
        self.db_name = db_name
        self.fail_simulated = fail_simulated
        
    def execute(self) -> bool:
        print(f" -> Accessing database: '{self.db_name}'...")
        if self.fail_simulated:
            print(" -> [Error] Connection lost during backup!")
            raise RuntimeError("Database Connection Terminated")
        print(" -> Database backup snapshot created.")
        return True

# =============================================================================
# 3. RUNTIME MONITOR CONTEXT MANAGER
# =============================================================================
class TaskMonitor:
    def __init__(self, task: Task):
        self.task = task
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.perf_counter()
        self.task.status = "RUNNING"
        print(f"\n[MONITOR] Starting Task: '{self.task.name}'")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.perf_counter() - self.start_time
        if exc_type is not None:
            self.task.status = "FAILED"
            print(f"[MONITOR] Task '{self.task.name}' FAILED in {duration:.4f}s with error: {exc_val}")
            # We log the error but let it propagate (return False)
            return False
        self.task.status = "SUCCESS"
        print(f"[MONITOR] Task '{self.task.name}' completed SUCCESS in {duration:.4f}s.")
        return True

# =============================================================================
# 4. TASK SCHEDULER ENGINE
# =============================================================================
class TaskScheduler:
    def __init__(self):
        self.queue = []
        
    def add_task(self, task: Task):
        print(f"Adding task: {task.name} to scheduler queue.")
        self.queue.append(task)
        
    def run_all(self):
        # Sort tasks by priority (highest first)
        self.queue.sort(key=lambda t: t.priority, reverse=True)
        print(f"\n--- Starting Scheduler run (Queue length: {len(self.queue)}) ---")
        
        for task in self.queue:
            # Wrap execution inside the TaskMonitor context manager
            try:
                with TaskMonitor(task):
                    success = task.execute()
                    if not success:
                        raise RuntimeError("Task execution returned False")
            except Exception as e:
                # Catch propagation to ensure remaining queue runs
                print(f"[Scheduler Handler] Resuming execution queue after task failure.")

# =============================================================================
# 5. PROJECT EXECUTION RUN
# =============================================================================
if __name__ == "__main__":
    # Instantiate Scheduler
    scheduler = TaskScheduler()
    
    # Create Tasks (Different configurations and priorities)
    t1 = FileDownloadTask("Download_OS_Image", "https://ubuntu.com/download", 1200, priority=2)
    t2 = DatabaseBackupTask("Hourly_User_Backup", "Users_Production_DB", priority=3)
    t3 = DatabaseBackupTask("Staging_Data_Sync", "Users_Staging_DB", fail_simulated=True, priority=1)
    
    # Register Tasks
    scheduler.add_task(t1)
    scheduler.add_task(t2)
    scheduler.add_task(t3)
    
    # Execute Task Engine
    scheduler.run_all()
    
    # Verify final states
    print("\n--- Final Task Status Report ---")
    print(t1)
    print(t2)
    print(t3)
