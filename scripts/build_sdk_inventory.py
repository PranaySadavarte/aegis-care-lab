"""Version-specific public surface inventory; references are not execution proof."""
import ast,json,re
from pathlib import Path
from importlib.metadata import version
import guava
root=Path(__file__).resolve().parents[1]
sdk=Path(guava.__file__).parent
app=(root/'agent/harborcare.py').read_text()
test_sources={str(p.relative_to(root)):p.read_text(encoding='utf-8') for p in (root/'tests').rglob('*.py')}
rows=[]
for file,classes in [('agent.py',('Agent',)),('call.py',('Call',)),('client.py',('Client',)),('helpers/llm.py',('IntentRecognizer','DatetimeFilter','DateRangeParser')),('helpers/rag.py',('DocumentQA',)),('helpers/server_rag.py',('ServerRAG',))]:
    tree=ast.parse((sdk/file).read_text(encoding='utf-8'))
    seen=set()
    for node in tree.body:
        if isinstance(node,ast.ClassDef) and node.name in classes:
            for method in node.body:
                if not isinstance(method,(ast.FunctionDef,ast.AsyncFunctionDef)) or method.name.startswith('_') or method.name in seen:continue
                seen.add(method.name)
                pattern=r'\.'+re.escape(method.name)+r'\b'
                refs=[p for p,s in test_sources.items() if re.search(pattern,s)]
                rows.append({'surface':node.name+'.'+method.name,'source':file,'agent_reference':bool(re.search(pattern,app)),'test_references':refs,'execution_status':'NOT_INDIVIDUALLY_ATTESTED'})
payload={'sdk_version':version('guava-sdk'),'scope':'Public methods declared on selected core and helper classes, not every export, inherited method or optional provider. Static references are not runtime coverage.','features':rows}
(root/'dashboard/lab-sdk-inventory.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
print(len(rows),'unique public members inventoried (including properties)')
