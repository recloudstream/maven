import asyncio
from json import load
from textwrap import dedent

repos = load(open("./repos.json", "r", encoding="utf-8"))

async def run_project(project, script):
    proc = await asyncio.create_subprocess_shell(f"cd {project}\n{script}",
     stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE)
    
    stdout, stderr = await proc.communicate()
    
    print(f"[{project} exited with {proc.returncode}]")
    if stdout:
        print(f"[{project}] stdout:\n{stdout.decode()}")
    if stderr:
        print(f"[{project}] stdout:\n{stderr.decode()}")

async def gradlew(project):
    # TODO: this needs to be done in a better way
    await run_project(project, dedent(f"""
        chmod +x gradlew
        ./gradlew publishToMavenLocal || \\
        ./gradlew install || \\
        ./gradlew installDebug || \\
        ./gradlew publishReleasePublicationToMavenLocal
    """))
                      
async def maven(project):
    await run_project(project, dedent(f"""
        mvn install -DskipTests
    """))
    
async def main():
    jobs = []
    jobs.extend([
        gradlew(repo) for repo in repos["gradlew"]
    ])
    jobs.extend([
        maven(repo) for repo in repos["maven"]
    ])
    await asyncio.gather(*jobs)
    
asyncio.run(main())
