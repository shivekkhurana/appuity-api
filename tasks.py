from invoke import task

@task
def dev(ctx):
    ctx.run("python server.py")
