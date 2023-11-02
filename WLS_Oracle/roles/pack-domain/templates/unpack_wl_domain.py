#=======================================================================================


domain_name='{{ domain_name }}'
domain_home= '{{ domain_base}}'+ domain_name +'/'
template_path='{{ domain_template }}'

readTemplate(template_path)
writeDomain(domain_home)
closeTemplate()
print 'successfully wrote domain '+ domain_name +' at '+domain_home
exit()
