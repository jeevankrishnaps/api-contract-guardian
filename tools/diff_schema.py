import sys
import json
from typing import Optional
from dataclasses import dataclass,field

@dataclass
class Change:
    kind:str
    area:str
    message:str

@dataclass
class DiffResult:
    changes:list[Change]=field(default_factory=list)
    @property
    def breaking(self)->list[Change]:
        breaking_changes = []
        for c in self.changes:
            if c.kind == "breaking":
                breaking_changes.append(c)

        return breaking_changes
    

def load(path: str)->dict:
    with open(path) as f:
        return json.load(f)
    

def diff_paths(old: dict, new: dict, result: DiffResult):
    old_path=old.get("paths",{})
    new_path=new.get("paths",{})

    for path in old_path:
        if path not in new_path:
            result.changes.append(Change("breaking","Endpoint",f"Endpoint removed: {path}"))
            continue

        old_methods=old_path[path]
        new_methods=new_path[path]

        for method in old_methods:
            if method not in new_methods:
                result.changes.append(Change("breaking","endpoint",f"Method removed: {method.upper()} {path}"))
            else:
                diff_operation(path,method,old_methods[method],new_methods[method], result)

    for path in new_path:
        if path not in old_path:
            result.changes.append(Change("info","endpoint",f"Endpoint added: {path}"))
    

def diff_operation(path: str, method: str,old_op: dict,new_op: dict,result: DiffResult):
    old_codes = set(old_op.get("responses", {}).keys())
    new_codes = set(new_op.get("responses", {}).keys())

    for code in old_codes-new_codes:
        result.changes.append(Change("breaking","status_code",f"{method.upper()} {path}: response status {code} removed"))

    old_req_schema =extract_body_schema(old_op)
    new_req_schema =extract_body_schema(new_op)
    if old_req_schema and new_req_schema:
        old_required=set(old_req_schema.get("required",[]))
        new_required=set(new_req_schema.get("required",[]))
        for field in new_required-old_required:
            result.changes.append(Change("breaking","field",f"{method.upper()} {path}: new required field'{field}'in request body"))

        old_properties=set(old_req_schema.get("properties",[]))
        new_properties=set(new_req_schema.get("properties",[]))
        for removed in old_properties-new_properties:
            result.changes.append(Change("breaking","field",f"{method.upper()} {path}: field'{removed}'removed from request body"))


def extract_body_schema(op:dict)->Optional[dict]:
    try:
        content=op["requestBody"]["content"]["application/json"]
        return content.get("schema",{})
    except KeyError:
        return None
    

def diff_schemas_section(old:dict,new:dict,result:DiffResult):
    old_schemas=old.get("components",{}).get("schemas",{})
    new_schemas=new.get("components",{}).get("schemas",{})

    for name,old_schema in old_schemas.items():
        if name not in new_schemas:
            result.changes.append(Change("breaking","model",f"Model removed: {name}"))
            continue

        new_schema=new_schemas[name]
        old_props=set(old_schema.get("properties",{}).keys())
        new_props=set(new_schema.get("properties",{}).keys())
        for removed in old_props-new_props:
            result.changes.append(Change("breaking","model",f"Model '{name}' : field '{removed}' removed"))

        old_required = set(old_schema.get("required", []))
        new_required = set(new_schema.get("required", []))
        for newly_required in new_required-old_required:
            if newly_required in old_props:
                result.changes.append(Change("breaking","model",f"Model '{name}' : field '{newly_required}' became required"))


def run_diff(old_path:str,new_path:str)->DiffResult:
    old=load(old_path)
    new=load(new_path)
    result=DiffResult()
    diff_paths(old, new, result)
    diff_schemas_section(old,new,result)
    return result

def format_markdown(result:DiffResult)->str:
    lines=["## API Contract Diff Report\n"]

    if not result.changes:
        lines.append("No changes detected in the API contract.")
        return "\n".join(lines)
    
    if result.breaking:
        lines.append(f"### {len(result.breaking)} BREAKING CHANGES\n")
        for c in result.breaking:
            lines.append(f"- **[{c.area}]** {c.message}")
        lines.append("")

    info_changes = [c for c in result.changes if c.kind == "info"]
    if info_changes:
        lines.append(f"###  {len(info_changes)} NON BREAKING CHANGES\n")
        for c in info_changes:
            lines.append(f"- [{c.area}] {c.message}")

    return "\n".join(lines)


if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Usage: python diff_schema.py <old_schema.json> <new_schema.json>")
        sys.exit(1)

    result=run_diff(sys.argv[1],sys.argv[2])
    report=format_markdown(result)
    print(report)

    with open("diff_report.md", "w") as f:
        f.write(report)


    sys.exit(1 if result.breaking else 0)





