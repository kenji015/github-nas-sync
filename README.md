# github-nas-mirror
Automatically mirrors all GitHub repositories from a user account to a  Network Attached Storage - NAS, keeping files up-to-date without cloning each repository manually.
> [!NOTE]
> ### Goal
>
>- A Docker container runs on your NAS.
>
>- Checks your GitHub repositories at regular intervals (e.g., every 10 minutes).
>
>- Automatically clones new repositories and pulls updates for existing ones.
>
>- Saves repository files (without .git) to your NAS folder.
>
>- Works for all current and future repositories—no manual configuration per repo needed.
> ### File Desc:
>| File | Purpose |
>|------|---------|
>| mirror.py | Clones and automatically updates all GitHub repositories to the NAS |
>| requirements.txt | Installs the Python dependencies |
>| docker-compose.yml | Starts and configures the container |
>| .env.example | Template for environment variables (username, token, intervals) |
>| FOLDER_STRUCTURE.md | Documents the project folder structure |

###
---
###

> [!WARNING]  
> # Please Note that the paths and details may be differ to your usecase and may need to be changed

## STEP by STEP installation:

### 1. Create NAS Folders & drop Files

>[!TIP]
>See: [Structure](docs/STRUCTURE.md)

### 2. Prepare GitHub Access

Create a Personal Access Token (classic) on GitHub → repo scope.

Record these credentials:
```
GITHUB_USERNAME
```
```
GITHUB_TOKEN
```
### 3. Create Project Files on NAS

Create a folder for Docker:
```your_volume_name```/docker/github-nas-mirror/

> [!IMPORTANT]
>Place the files in src inside your  ```github-nas-mirror```:
>
> [Open Docs folder](src/)

### 4. Start the Container

```CLI
sudo docker compose build
sudo docker compose up -d
sudo docker logs -f gh-nas-mirror
```
> [!NOTE]  
> - Repository files appear in /```your_volume_name```/github-save/github-mirror/<owner>/<repo>
> - Git cache is in /```your_volume_name```/github-save/github-cache/<owner>/<repo>

✅ This setup will automatically mirror all your GitHub repos to your NAS, and keep them up-to-date at the defined interval.
