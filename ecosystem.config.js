module.exports = {
  apps: [{
    name: 'age_bot_py',
    cmd: 'age_bot/bin/age_bot',
    args: 'start',
    autorestart: false,
    watch: true,
    pid: '',
    instacnc
  }],
  deploy: {
    production : {
      user : 'SSH_USERNAME',
      host : 'SSH_HOSTMACHINE',
      ref  : 'origin/master',
      repo : 'GIT_REPOSITORY',
      path : 'DESTINATION_PATH',
      'pre-deploy-local': '',
      'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env production',
      'pre-setup': ''
    }
  }
};
