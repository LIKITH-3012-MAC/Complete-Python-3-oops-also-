import os

readme_path = "/Users/likithnaidu/Desktop/oops/README.md"

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. New Section to Append
new_section = """
---

## 8. Module 7: CyberSecurity Python Security Engineering Core (001 - 010)

| Notebook | Topic | Difficulty | Prerequisite | Link |
|:---|:---|:---:|:---|:---|
| **001** | Secure Coding Principles | ⭐ | None | [Open](CyberSecurity_Python/SECURITY_ENGINEERING_CORE/001_Secure_Coding_Principles.ipynb) |
| **002** | Injection Prevention: SQL | ⭐⭐ | 001 | [Open](CyberSecurity_Python/SECURITY_ENGINEERING_CORE/002_Injection_Prevention_SQL.ipynb) |
| **003** | Injection Prevention: Command | ⭐⭐ | 001 | [Open](CyberSecurity_Python/SECURITY_ENGINEERING_CORE/003_Injection_Prevention_Command.ipynb) |
| **004** | Injection Prevention: XSS | ⭐⭐ | 001 | [Open](CyberSecurity_Python/SECURITY_ENGINEERING_CORE/004_Injection_Prevention_XSS.ipynb) |
| **005** | Safe Eval/Exec Alternatives | ⭐⭐ | 001 | [Open](CyberSecurity_Python/SECURITY_ENGINEERING_CORE/005_Safe_Eval_Exec_Alternatives.ipynb) |
| **006** | Secure Serialization | ⭐⭐⭐ | 001 | [Open](CyberSecurity_Python/SECURITY_ENGINEERING_CORE/006_Secure_Serialization.ipynb) |
| **007** | Secure File Handling | ⭐⭐ | 001 | [Open](CyberSecurity_Python/SECURITY_ENGINEERING_CORE/007_Secure_File_Handling.ipynb) |
| **008** | Secrets Management | ⭐ | None | [Open](CyberSecurity_Python/SECURITY_ENGINEERING_CORE/008_Secrets_Management.ipynb) |
| **009** | Logging Security Architecture | ⭐⭐ | 001 | [Open](CyberSecurity_Python/SECURITY_ENGINEERING_CORE/009_Logging_Security_Architecture.ipynb) |
| **010** | Error Handling Security | ⭐⭐ | 001 | [Open](CyberSecurity_Python/SECURITY_ENGINEERING_CORE/010_Error_Handling_Security.ipynb) |
"""

# Let's insert before the How to study block
target_heading = "## 8. How to Study"
if target_heading in content:
    parts = content.split(target_heading)
    updated_content = parts[0] + new_section.strip() + "\n\n---\n\n## 9. How to Study" + parts[1]
    
    # 2. Update visual roadmap diagram
    # Existing graph ends with:
    #     E --> F[Module 6: CyberSecurity OS Tooling Lab 001-010]
    # Let's add:
    #     F --> G[Module 7: CyberSecurity Python Security Engineering Core 001-010]
    old_graph = """    E --> F[Module 6: CyberSecurity OS Tooling Lab 001-010]"""
    new_graph = """    E --> F[Module 6: CyberSecurity OS Tooling Lab 001-010]
    F --> G[Module 7: CyberSecurity Python Security Engineering Core 001-010]"""
    
    if old_graph in updated_content:
        updated_content = updated_content.replace(old_graph, new_graph)
        
    # 3. Update Directory structure representation
    old_dir = """└── CyberSecurity_OS/                  # Module 6: Clickable CyberSecurity Notebooks (001-010)
    ├── CYBERSECURITY_TOOLING_LAB/
    │   ├── 001_Port_Scanner.ipynb
    │   └── ..."""
    
    new_dir = """├── CyberSecurity_OS/                  # Module 6: Clickable CyberSecurity Notebooks (001-010)
│   ├── CYBERSECURITY_TOOLING_LAB/
│   │   ├── 001_Port_Scanner.ipynb
│   │   └── ...
└── CyberSecurity_Python/              # Module 7: Clickable CyberSecurity Python Notebooks (001-010)
    ├── SECURITY_ENGINEERING_CORE/
    │   ├── 001_Secure_Coding_Principles.ipynb
    │   └── ..."""
    
    if old_dir in updated_content:
        updated_content = updated_content.replace(old_dir, new_dir)
        
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print("Successfully appended CyberSecurity Python navigation to README.md")
else:
    # Fallback to appending
    with open(readme_path, "a", encoding="utf-8") as f:
        f.write(new_section)
    print("Heading not found; appended section to the end of README.md")
