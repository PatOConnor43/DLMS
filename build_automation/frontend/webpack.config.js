const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const webpack = require('webpack');

module.exports = env => {
    console.log(process.env.BASE_URL);
    process.env
    return {
    mode: 'development',
    devServer: {
       contentBase: './dist',
       headers: {
        "Access-Control-Allow-Origin": "*",
      },
    },
    entry: './src/js/index.js',
    node: {
        fs: 'empty'
    },
    module: {
        rules: [{
            test: /\.js$/,
            exclude: /node_modules/,
            use: {
                loader: 'babel-loader',
            }
        },{
            test: /\.css$/,
            use: [ 'style-loader', 'css-loader' ]
        },{
            test: /\.(png|svg|jpg|gif)$/,
            use: ['file-loader']
        }
      ]
    },
    plugins: [
        new CopyWebpackPlugin([{
                from: '**/*', context: 'html'
            },
            {
                from: 'css/**/*',
            },
            {
                from: 'images/**/*',
            },
        ], {
            context: 'src/'
        }),
        new webpack.EnvironmentPlugin({
            BASE_URL: JSON.stringify(process.env.BASE_URL) || ''
        })
    ],
    output: {
        filename: 'js/bundle.js',
        path: path.resolve(__dirname, 'static')
    },
}};
