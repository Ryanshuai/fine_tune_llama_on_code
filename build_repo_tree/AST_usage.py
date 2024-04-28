import ast
import inspect

#If the file is a python file, use AST to parse the file and generate tree Nodes

# Helper function to convert node to source code
def node_to_source(node, source_lines):
    return "".join(source_lines[node.lineno - 1:node.end_lineno])

# Function to parse a Python file and analyze its structure
def parse_python_file(filepath):
    with open(filepath, "r") as source_file:
        source_content = source_file.read()
        source_lines = source_content.splitlines(keepends=True)
        tree = ast.parse(source_content)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                parse_class_contents(node, source_lines)
            elif isinstance(node, ast.FunctionDef):
                print(f"Function {node.name}:")
                print(node_to_source(node, source_lines))
                print("-" * 40)

# Function to recursively parse elements within a class
def parse_class_contents(node, source_lines):
    print(f"Class {node.name}:")
    for subnode in ast.iter_child_nodes(node):
        if isinstance(subnode, ast.FunctionDef):
            print(f"  Method {subnode.name}:")
            print(node_to_source(subnode, source_lines))
        elif isinstance(subnode, ast.ClassDef):
            print(f"  Inner class {subnode.name}:")
            parse_class_contents(subnode, source_lines)  # Recurse into inner class
        elif isinstance(subnode, ast.Assign):
            # To simply display assignments as 'attributes'
            targets = [t.id for t in subnode.targets if isinstance(t, ast.Name)]
            print(f"  Attribute {' '.join(targets)}")
    print("-" * 40)


if __name__ == "__main__":
    parse_python_file("test_data/test_python_file_for_parsing.py")
