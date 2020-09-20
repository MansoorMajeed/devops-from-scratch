# Deploying a simple NodeJS based app (Hexo blog)

```
sudo apt-get install nodejs
sudo apt-get install npm

npm install -g hexo-cli

hexo init ~/hexo_blog
cd ~/hexo_blog
npm install
nano _config.yml 

hexo new first-post
hexo publish first-post 

hexo server
```