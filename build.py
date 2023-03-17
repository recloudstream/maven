import asyncio
from json import load
from textwrap import dedent

repos = load(open("./repos.json", "r", encoding="utf-8"))

async def gradlew(project):
    proc = await asyncio.create_subprocess_shell(dedent(f"""
        cd {project}
        chmod +x gradlew
        ./gradlew publishToMavenLocal
    """),
     stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE)
    
    stdout, stderr = await proc.communicate()
    
    print(f"[{project} exited with {proc.returncode}]")
    if stdout:
        print(f"[{project}] stdout:\n{stdout.decode()}")
    if stderr:
        print(f"[{project}] stdout:\n{stderr.decode()}")
    
async def main():
    await asyncio.gather(*[
        gradlew(repo) for repo in repos["gradlew"]
    ])