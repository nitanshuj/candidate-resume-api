"""
Utility script for swagger/OpenAPI specification operations.
This script can export the current FastAPI OpenAPI spec to a yaml file
and vice versa.
"""

import json
import yaml
import requests
from pathlib import Path

def export_openapi_to_yaml():
    """
    Exports the OpenAPI specification from a running FastAPI app to a YAML file.
    Requires the API to be running locally.
    """
    try:
        # Get the OpenAPI JSON from running FastAPI app
        response = requests.get("http://localhost:8000/openapi.json")
        response.raise_for_status()
        openapi_json = response.json()
        
        # Convert to YAML
        with open("swagger.yaml", "w") as yaml_file:
            yaml.dump(openapi_json, yaml_file, sort_keys=False)
        
        print("OpenAPI specification exported to swagger.yaml")
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not fetch OpenAPI spec. Make sure the API is running: {e}")
        print("Start the API with 'uvicorn app.main:app --reload' before running this script.")
    except Exception as e:
        print(f"Error: {e}")

def import_yaml_to_openapi():
    """
    Imports a YAML OpenAPI specification to create a JSON OpenAPI spec file.
    """
    try:
        # Read the YAML file
        with open("swagger.yaml", "r") as yaml_file:
            openapi_spec = yaml.safe_load(yaml_file)
        
        # Write to JSON file
        with open("openapi.json", "w") as json_file:
            json.dump(openapi_spec, json_file, indent=2)
        
        print("YAML specification imported to openapi.json")
    except FileNotFoundError:
        print("Error: swagger.yaml not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenAPI/Swagger specification utilities")
    parser.add_argument("--export", action="store_true", help="Export OpenAPI spec from running FastAPI app")
    parser.add_argument("--import", dest="import_yaml", action="store_true", help="Import from swagger.yaml to openapi.json")
    
    args = parser.parse_args()
    
    if args.export:
        export_openapi_to_yaml()
    elif args.import_yaml:
        import_yaml_to_openapi()
    else:
        print("No action specified. Use --export or --import")
