import os

this_dir = os.path.dirname(os.path.realpath(__file__))
this_dir = this_dir.replace(' ', '\ ')
print(this_dir)
docs_dir = os.path.join(this_dir, '..', 'docs')
html_dir = os.path.join(this_dir, '..', 'docs', 'html')
static_dir = os.path.join(this_dir, '..', 'docs', '_static')
sources_dir = os.path.join(this_dir, '..', 'docs', '_sources')
modules_dir = os.path.join(this_dir, '..', 'docs', '_modules')
buildinfo_dir = os.path.join(this_dir, '..', 'docs', '.buildinfo')

os.system('make html')
os.system('rm -rf {}'.format(static_dir))
os.system('rm -rf {}'.format(sources_dir))
os.system('rm -rf {}'.format(modules_dir))
# os.system('rm {}'.format(buildinfo_dir))
os.system('mv {html}/* {docs}/'.format(html=html_dir, docs=docs_dir))
os.system('rm -rf {html}'.format(html=html_dir))
