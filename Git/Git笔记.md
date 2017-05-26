[toc]
# Git note
## Git delete file

> Use git rm:

>     git rm file1.txt
>     git commit -m "remove file1.txt"
> But if you want to remove the file only from the Git repository and not remove it from the filesystem, use:
> 
>     git rm --cached file1.txt
> And to push changes to remote repo
> 
>     git push origin branch_name  

