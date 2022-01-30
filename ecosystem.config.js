module.exports = {
  apps: [{
    name: 'age_bot_py',
    cmd: 'age_bot/bin/age_bot',
    args: 'start',
    autorestart: false,
    watch: true,
    ignore
    pid: '/home/ken/.age_bot_py.pid',
    instances: 1,
    env: {
      ENV: 'development'
    },
    env_production: {
      ENV: 'production'
    },
    interpreter: 'python3'
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
