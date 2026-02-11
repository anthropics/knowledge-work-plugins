
import os
import json
import yaml
import sys

def validate_plugin_json(plugin_dir):
    path = os.path.join(plugin_dir, '.claude-plugin', 'plugin.json')
    if not os.path.exists(path):
        return False, "Missing .claude-plugin/plugin.json"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        required_fields = ['name', 'version', 'description', 'author']
        missing = [field for field in required_fields if field not in data]
        if missing:
            return False, f"Missing fields: {', '.join(missing)}"
        return True, "Valid"
    except Exception as e:
        return False, str(e)

def validate_mcp_json(plugin_dir):
    path = os.path.join(plugin_dir, '.mcp.json')
    if not os.path.exists(path):
        return False, "Missing .mcp.json"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'mcpServers' not in data:
            return False, "Missing 'mcpServers'"
        return True, "Valid"
    except Exception as e:
        return False, str(e)

def parse_frontmatter(content):
    if not content.startswith('---\n'):
        return None
    try:
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None
        return yaml.safe_load(parts[1])
    except:
        return None

def validate_skills(plugin_dir):
    skills_dir = os.path.join(plugin_dir, 'skills')
    if not os.path.isdir(skills_dir):
        return True, [] # Optional? Or empty skills allowed?
    
    errors = []
    for item in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, item)
        if os.path.isdir(skill_path):
            md_path = os.path.join(skill_path, 'SKILL.md')
            if not os.path.exists(md_path):
                errors.append(f"Skill '{item}' missing SKILL.md")
            else:
                try:
                    with open(md_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    fm = parse_frontmatter(content)
                    if not fm:
                        errors.append(f"Skill '{item}' invalid frontmatter")
                    elif 'description' not in fm:
                         errors.append(f"Skill '{item}' missing description")
                except Exception as e:
                    errors.append(f"Skill '{item}' error: {e}")
    return len(errors) == 0, errors

def main():
    root_dir = os.getcwd()
    plugins_found = 0
    errors_found = 0
    
    print("VALIDATION REPORT")
    print("=================")

    for item in os.listdir(root_dir):
        plugin_dir = os.path.join(root_dir, item)
        if not os.path.isdir(plugin_dir) or item.startswith('.'):
            continue
            
        if os.path.exists(os.path.join(plugin_dir, '.claude-plugin', 'plugin.json')):
            plugins_found += 1
            plugin_errors = []
            
            # Checks
            valid, msg = validate_plugin_json(plugin_dir)
            if not valid: plugin_errors.append(f"plugin.json: {msg}")
            
            valid, msg = validate_mcp_json(plugin_dir)
            if not valid: plugin_errors.append(f".mcp.json: {msg}")
            
            valid, msgs = validate_skills(plugin_dir)
            if not valid:
                for m in msgs: plugin_errors.append(f"Skill: {m}")
            
            if plugin_errors:
                print(f"\n[FAIL] {item}")
                for err in plugin_errors:
                    print(f"  - {err}")
                errors_found += 1
            else:
                print(f"[PASS] {item}")

    print("\nSUMMARY")
    print(f"Plugins Scanned: {plugins_found}")
    print(f"Plugins with Errors: {errors_found}")
    
    if errors_found > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
