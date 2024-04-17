import csv
from google.oauth2 import service_account
from googleapiclient.discovery import build

def list_folders_and_projects(parent_folder_id, parent_folder_name, credentials):
    # Initialize the CSV data list
    csv_data = []

    # Connect to Cloud Resource Manager API
    crm_service = build('cloudresourcemanager', 'v3', credentials=credentials)
    
    # List projects in the current folder
    parent = f"folders/{parent_folder_id}"
    request = crm_service.projects().list(parent=parent)
    response = request.execute()
    projects = response.get('projects', [])

    # Iterate through projects
    for project in projects:
        project_id = project['projectId']
        project_name = project['displayName']
        
        # List instances in the project
        instances_data = list_vm_instances(credentials, project_id)
        
        # Add project data to CSV data
        project_data = {
            "Folder ID": parent_folder_id,
            "Folder Name": parent_folder_name,
            "Project ID": project_id,
            "Project Name": project_name,
            "Zone": "",
            "Instance Name": "",
            "Instance Status": "",
            "Instance OS": "",
            "Instance IP": ""
        }
        csv_data.append(project_data)

        # Add instance data to CSV data
        for instance in instances_data:
            instance_data = {
                "Folder ID": parent_folder_id,
                "Folder Name": parent_folder_name,
                "Project ID": project_id,
                "Project Name": project_name,
                "Zone": instance["zone"],
                "Instance Name": instance["name"],
                "Instance Status": instance["status"],
                "Instance OS": instance["os"],
                "Instance IP": instance["ip"]
            }
            csv_data.append(instance_data)

    # List subfolders under the current folder
    request = crm_service.folders().list(parent=parent)
    response = request.execute()
    subfolders = response.get('folders', [])

    # Iterate through subfolders
    for folder in subfolders:
        folder_id = folder['name'].split('/')[-1]
        folder_name = folder['displayName']
        
        # Recursively list projects and instances in the subfolder
        csv_data += list_folders_and_projects(folder_id, folder_name, credentials)

    return csv_data


def list_vm_instances(credentials, project_id):
    # Connect to Compute Engine API
    compute_service = build('compute', 'v1', credentials=credentials)
    
    # List instances in the project
    request = compute_service.instances().aggregatedList(project=project_id)
    response = request.execute()

    instance_data_list = []

    # Iterate through zones and instances
    for zone, instance_list in response['items'].items():
        if 'instances' in instance_list:
            for instance in instance_list['instances']:
                instance_data = {
                    "name": instance.get('name', ""),
                    "status": instance.get('status', ""),
                    "os": instance.get('disks', [{}])[0].get('licenses', [""])[0].split('/')[-1],
                    "ip": instance.get('networkInterfaces', [{}])[0].get('networkIP', ""),
                    "zone": zone.split('/')[-1]
                }
                instance_data_list.append(instance_data)

    return instance_data_list


def write_csv(csv_data, filename):
    # Writing data to CSV file
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ["Folder ID", "Folder Name", "Project ID", "Project Name", "Zone", "Instance Name", "Instance Status", "Instance OS", "Instance IP"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in csv_data:
            writer.writerow(data)


if __name__ == "__main__":
    credentials = service_account.Credentials.from_service_account_file(
        'credentials_file.json',
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    parent_folder_id = ''  # Provide the parent folder ID here
    parent_folder_name = ''  # Provide the parent folder name here

    csv_data = list_folders_and_projects(parent_folder_id, parent_folder_name, credentials)
    write_csv(csv_data, 'output.csv')
