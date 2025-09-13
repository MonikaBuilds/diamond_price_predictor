# Create a virtual environment

```bash
conda create -p env python=3.8 -y
source activate ./env

# Git commands
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin <your repo git url>
git push -u origin main
