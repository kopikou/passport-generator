import gzip
import os
from pathlib import Path
from pprint import pprint

from fabric import task, Connection

@task
def deploy(ctx):
    data = ctx['deploy']
    folder = data.get('folder')
    c = Connection(**data.get('connection', {}))

    with c.prefix("source ~/.zshrc"):
        with c.prefix("pyenv activate surp"):
            with c.cd(folder):
                c.run("git pull")
                c.run("pyenv versions")
                c.run("pip install -r requirements.txt")
            with c.cd(folder + "/client"):
                c.run("npm install")
                c.run("npm run build")
            with c.cd(folder):
                c.run("python manage.py collectstatic --noinput")
                c.run("pg_dump -c surp > \"/srv/surp/backups/surp_predeploy_$(date '+%Y%m%d_%H%M%S').sql\"")
                c.run("python manage.py migrate")
            c.run("systemctl restart --user surp.service")
