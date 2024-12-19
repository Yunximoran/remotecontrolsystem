const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  configureWebpack:{
    resolve:{
      fallback:{
        "path": false
      }
    }    
  },
  devServer: {
    historyApiFallback: true,
    allowedHosts: "all"
  }
  // devServer:{
 
  //   historyApiFallback: true,
 
  //   allowedHosts: "all",
 
  // }

})
