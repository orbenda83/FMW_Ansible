# Common Ansible Role

This role installs OS packages that are required by subsequent roles. 

This is a base role so it is not called directly. It will be called by a higher role that has dependency on it. 

## Requirements

Other than having ansible installed and a directory, there are no other requirements

## Variables

The varibles that are passed to the role are a list of OS tools and libraries:
 - libselinux-python
  - curl
  - unzip
  - libXtst
  - libXrender.so.1
  - gcc-c++.x86_64
  - glibc.i686
  - glibc-devel.i686
  - libaio-devel.x86_64
  - libzip.i686
  - libgcc.i686
  - libstdc++.i686
  - libstdc++-devel.i686
  - libstdc++-devel.x86_64
  - sysstat 
  - iperf 
  - bind-utils
  
## Dependencies

n/a

## Example

n/a
