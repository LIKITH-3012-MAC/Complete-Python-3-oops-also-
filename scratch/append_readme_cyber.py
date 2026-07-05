import os

readme_path = "/Users/likithnaidu/Desktop/oops/README.md"

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. New Section to Append
new_section = """
---

## 7. Module 6: CyberSecurity OS Tooling Lab (001 - 010)

| Notebook | Topic | Difficulty | Prerequisite | Link |
|:---|:---|:---:|:---|:---|
| **001** | Port Scanner | ⭐⭐ | Socket API | [Open](CyberSecurity_OS/CYBERSECURITY_TOOLING_LAB/001_Port_Scanner.ipynb) |
| **002** | Password Strength Analyzer | ⭐ | None | [Open](CyberSecurity_OS/CYBERSECURITY_TOOLING_LAB/002_Password_Strength_Analyzer.ipynb) |
| **003** | Hash Generator & Verifier | ⭐ | None | [Open](CyberSecurity_OS/CYBERSECURITY_TOOLING_LAB/003_Hash_Generator_and_Verifier.ipynb) |
| **004** | File Integrity Checker | ⭐⭐ | Hash Verification | [Open](CyberSecurity_OS/CYBERSECURITY_TOOLING_LAB/004_File_Integrity_Checker.ipynb) |
| **005** | Log Analyzer Engine | ⭐⭐ | Regex patterns | [Open](CyberSecurity_OS/CYBERSECURITY_TOOLING_LAB/005_Log_Analyzer_Engine.ipynb) |
| **006** | Network Monitor Simulator | ⭐⭐⭐ | Socket API, Packets | [Open](CyberSecurity_OS/CYBERSECURITY_TOOLING_LAB/006_Network_Monitor_Simulator.ipynb) |
| **007** | Vulnerability Scanner Simulator | ⭐⭐ | Port Scanner | [Open](CyberSecurity_OS/CYBERSECURITY_TOOLING_LAB/007_Vulnerability_Scanner_Simulator.ipynb) |
| **008** | Encryption/Decryption Toolkit | ⭐⭐⭐ | PyCryptodome AES | [Open](CyberSecurity_OS/CYBERSECURITY_TOOLING_LAB/008_Encryption_Decryption_Toolkit.ipynb) |
| **009** | Secure Chat Simulator | ⭐⭐⭐⭐ | RSA/AES, Sockets | [Open](CyberSecurity_OS/CYBERSECURITY_TOOLING_LAB/009_Secure_Chat_Simulator.ipynb) |
| **010** | Token Generator System | ⭐⭐⭐ | Cryptography | [Open](CyberSecurity_OS/CYBERSECURITY_TOOLING_LAB/010_Token_Generator_System.ipynb) |
"""

# Let's insert before the How to study block
target_heading = "## 7. How to Study"
if target_heading in content:
    parts = content.split(target_heading)
    updated_content = parts[0] + new_section.strip() + "\n\n---\n\n## 8. How to Study" + parts[1]
    
    # 2. Update visual roadmap diagram
    # Existing graph ends with:
    #     D --> E[Module 5: Mathematics for AI Series 001-010]
    # Let's add:
    #     E --> F[Module 6: CyberSecurity OS Tooling Lab 001-010]
    old_graph = """    D --> E[Module 5: Mathematics for AI Series 001-010]"""
    new_graph = """    D --> E[Module 5: Mathematics for AI Series 001-010]
    E --> F[Module 6: CyberSecurity OS Tooling Lab 001-010]"""
    
    if old_graph in updated_content:
        updated_content = updated_content.replace(old_graph, new_graph)
        
    # 3. Update Directory structure representation
    old_dir = """└── Mathematics_for_AI/                # Module 5: Clickable Mathematics Notebooks (001-010)
    ├── 001_Number_Systems.ipynb
    └── ..."""
    
    new_dir = """├── Mathematics_for_AI/                # Module 5: Clickable Mathematics Notebooks (001-010)
│   ├── 001_Number_Systems.ipynb
│   └── ...
└── CyberSecurity_OS/                  # Module 6: Clickable CyberSecurity Notebooks (001-010)
    ├── CYBERSECURITY_TOOLING_LAB/
    │   ├── 001_Port_Scanner.ipynb
    │   └── ..."""
    
    if old_dir in updated_content:
        updated_content = updated_content.replace(old_dir, new_dir)
        
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print("Successfully appended CyberSecurity OS navigation to README.md")
else:
    # Fallback to appending
    with open(readme_path, "a", encoding="utf-8") as f:
        f.write(new_section)
    print("Heading not found; appended section to the end of README.md")
