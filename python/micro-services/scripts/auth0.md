
const axios = require("axios");
exports.onExecutePostLogin = async (event, api) => {
  if(event.stats.logins_count== 1){
    // Registration to make it compatible with social and database login
    const remoteUser = await axios.post("https://api.einstonlabs.com/api/v1/register/",{
        "authorization" : event.authorization,
        "connection" : event.connection,
        "organization" : event.organization,
        "geo" : event.request.geoip,
        "loginCount" : event.stats.logins_count,
        "user" : event.user
    });
  }else{
    // Subsequent Logings
  }
};
