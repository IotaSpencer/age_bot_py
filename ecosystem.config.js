module.exports = {
  apps: [{
    name: 'age_bot_py',
    cmd: 'age_bot/bin/age_bot',
    args: 'start',
    autorestart: false,
    watch: true,
    ignore_watch: [
      "discord.log"
    ],
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
      user : '',
      host : '',
      ref: 'origin/master',
      repo : 'github.com:IotaSpencer/age_bot_py',
      path : '',
      'pre-deploy-local': '',
      'pre-setup': ''
    }
  }
};
