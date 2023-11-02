# Common Ansible Role

This role copies files  and tarred archives on to a traget.

## Requirements
n/a
## Variables

The varibles that are passed to the role are a list of OS tools and libraries:

define following dictionaries as required.

common_files_to_copy:
   - source: "{{ installers }}/iam/files/DeploymentPlans/idm-server_Plan.xml"
     destination: "{{ oracle_home }}/server/"
     to_name: Plan.xml

common_archives_to_copy:
  - source: "{{ installers }}/iam/files/oim_ThirdParty/ThirdParty.tar"
     destination: "{{ oracle_home }}/server/"
     to_folder: ThirdParty



## Dependencies

n/a

## Example

n/a
