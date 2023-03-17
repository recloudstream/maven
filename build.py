import asyncio
from json import load

repos = load(open("./repos.json", "r", encoding="utf-8"))

async def gradlew(project):
    proc = await asyncio.create_subprocess_shell(f"""
        cd {project}
        chmod +x gradlew
        ./gradlew publishToMavenLocal
    """)
    
async def main():
    await asyncio.gather(*[
        gradlew(repo) for repo in repos['gradlew']
    ])