# How to deploy and start the App in EC2 server
1. Log into the EC2 server :\
`ssh -i "~/ManaDibetes.pem" ec2-user@35.166.154.192`
2. Go to projects folder and clone the git repo: \
`cd projects/` \
`rm -R type2diabetes` \
`git clone https://github.com/mmousom/type2diabetes.git`
3. Start tmux session: \
`tmux new -s StreamSession` \
In the editor - \
`streamlit run main.py`
>press ctrl+B and then D to come out of tmux session