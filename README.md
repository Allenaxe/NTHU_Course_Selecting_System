# NTHU Course Selecting System
A Course selecting system final project for Introduction to Artificial Intelligence (11210CS460100)

# 協作指南
1. 從 develop 分支使用 git switch -c {new branch name} 切出一個新分支
2. 做完一個 Part 之後作 git add {file name} 將檔案加入追蹤
3. 作 git commit 提交修改至本地提交庫 (記得寫簡短易懂的 commit message)
4. 推送到遠端之前先作 git merge develop 確保不會有 merge conflict 產生
5. 執行 git push origin {local branch name} 推送分支到遠端
6. 做完此分支或是自己的 Task 之後，發 pull request 到 develop
7. 可以在右側請人 review 或自己 merge branch
8. 在遠端刪除分支
9. 回到本地端切換回 develop ，並執行 git pull 將 develop 分支更新
10. 執行 git branch -d {local branch name in 8.} 刪除本地分支